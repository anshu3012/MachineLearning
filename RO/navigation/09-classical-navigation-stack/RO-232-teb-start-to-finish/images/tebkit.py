"""Our Python version of teb_local_planner's algorithm, written from its code (branch ros2-master, commit e4562a62,
the branch Nav2 uses) with its parameter values. It is NOT the package running: it follows the same steps in the
same order, but with these simplifications (each is said in the Note):
- the solver: g2o's sparse Levenberg-Marquardt is replaced by our own NumPy Levenberg-Marquardt with derivatives by
  finite differences (same cost terms, same 4 passes of 5 steps);
- the costmap: a cell is lethal when an obstacle of the room covers it (no sensor, no inflation layer); the
  feasibility check tests every lethal cell inside the robot's disk (Nav2's critic tests the cells under its outline);
- the roadmap's random samples come from a seeded generator (the package seeds from std::random_device);
- planning takes no time: each cycle's command is applied at once for the next 0.1 s.
Everything else (pruning and cutting the plan, point obstacles, obstacle association, the edges and their penalties,
resizing, warm start, H-signatures, the roadmap and depth-first search, selection, the feasibility check, the
command and its saturation) follows the code; the function names say which C++ function each one copies.

No output when run on its own; run with any argument for the self-check."""
import math

import bandkit as bk
import numpy as np
from threadpoolctl import threadpool_limits

threadpool_limits(1)   # one BLAS thread: the solver's steps do not depend on the machine's thread count

# ---------------------------------------------------------------- parameters
# C++ defaults of TebConfig() in include/teb_local_planner/teb_config.h (ros2-master): what Nav2 gets when the
# parameter file sets nothing.
DEFAULTS = dict(
    dt_ref=0.3, dt_hysteresis=0.1, min_samples=3, max_samples=500, global_plan_overwrite_orientation=True,
    allow_init_with_backwards_motion=False, global_plan_viapoint_sep=-1.0, max_global_plan_lookahead_dist=1.0,
    global_plan_prune_distance=1.0, force_reinit_new_goal_dist=1.0, force_reinit_new_goal_angular=0.5 * math.pi,
    feasibility_check_no_poses=5, control_look_ahead_poses=1,
    max_vel_x=0.4, max_vel_x_backwards=0.2, max_vel_theta=0.3, acc_lim_x=0.5, acc_lim_theta=0.5,
    min_turning_radius=0.0, wheelbase=1.0, cmd_angle_instead_rotvel=False,
    xy_goal_tolerance=0.2, free_goal_vel=False,
    min_obstacle_dist=0.5, inflation_dist=0.6, costmap_obstacles_behind_robot_dist=1.5,
    obstacle_association_force_inclusion_factor=1.5, obstacle_association_cutoff_factor=5.0,
    no_inner_iterations=5, no_outer_iterations=4, penalty_epsilon=0.05,
    weight_max_vel_x=2.0, weight_max_vel_theta=1.0, weight_acc_lim_x=1.0, weight_acc_lim_theta=1.0,
    weight_kinematics_nh=1000.0, weight_kinematics_forward_drive=1.0, weight_kinematics_turning_radius=1.0,
    weight_optimaltime=1.0, weight_shortest_path=0.0, weight_obstacle=50.0, weight_inflation=0.1,
    weight_viapoint=1.0, weight_prefer_rotdir=50.0, weight_adapt_factor=2.0,
    enable_homotopy_class_planning=True, max_number_classes=5, selection_cost_hysteresis=1.0,
    selection_prefer_initial_plan=0.95, selection_obst_cost_scale=100.0, selection_viapoint_cost_scale=1.0,
    obstacle_heading_threshold=0.45, roadmap_graph_no_samples=15, roadmap_graph_area_width=6.0,
    h_signature_threshold=0.1, delete_detours_backwards=True, detours_orientation_tolerance=0.5 * math.pi,
    length_start_orientation_vector=0.4, max_ratio_detours_duration_best_duration=3.0,
    shrink_horizon_backup=True, shrink_horizon_min_duration=10.0, oscillation_recovery=True,
    oscillation_v_eps=0.1, oscillation_omega_eps=0.1, oscillation_recovery_min_duration=10.0,
    oscillation_filter_duration=10.0,
)
# Our robot and room, where they differ from the defaults (the Note gives the reason for each):
OURS = dict(
    max_global_plan_lookahead_dist=3.0,   # the ROS 1 cfg default and the package's Nav2 example file (C++: 1.0)
    max_vel_x=0.5, max_vel_theta=1.0,     # the largest box (v, omega) inside the wheel limit 0.6 m/s: 0.5 + 1.0 x 0.1
    acc_lim_x=0.5,                        # our robot's 0.5 m/s^2 (same as the default)
    acc_lim_theta=10.0,                   # our robot's model has no turn-rate limit; high enough not to bind
    min_obstacle_dist=0.1,                # RO-058's 0.1 m for the small room (default 0.5 m)
    xy_goal_tolerance=0.02,               # RO-058's arrival test (Nav2's goal checker passes its tolerance in)
)
CFG = dict(DEFAULTS, **OURS)
R_ROBOT = bk.R_BODY                       # footprint_model: circular, radius 0.25 m
COSTMAP_SIZE, COSTMAP_RES = 3.0, 0.05     # Nav2 bring-up local costmap: 3 m x 3 m rolling window, 0.05 m cells
CYCLE = 0.1                               # controller_frequency 10 Hz, as RO-058 and Roesmann et al. 2021
YAW_TOL = 0.05                            # RO-058's arrival test: heading within 0.05 rad, speed below 0.02 m/s
SEED = 7                                  # seeds the roadmap's random samples


def wrap(a):
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi


# ---------------------------------------------------------------- inputs: the global plan and the costmap
def global_plan(res=COSTMAP_RES):
    """The A* route of RO-034 with its first point moved to the robot and its last to the door pose (as RO-058's
    refine-once drive does, and as Nav2's planners start at the robot and end at the goal pose), one pose every
    0.05 m (a planner on 0.05 m cells gives one pose per cell). Rows (x, y, yaw); yaw along the route, the last one
    the door's 90 degrees."""
    pts = bk.ROUTE.copy()
    pts[0], pts[-1] = bk.START[:2], bk.GOAL[:2]
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = float(np.hypot(*(b - a)))
        k = max(1, int(round(L / res)))
        out += [a + (b - a) * (j / k) for j in range(1, k + 1)]
    P = np.array(out)
    yaw = np.arctan2(*np.diff(P, axis=0).T[::-1])
    yaw = np.append(yaw, bk.GOAL[2])
    return np.column_stack([P, yaw])


def plan_length(plan):
    return float(np.sum(np.hypot(*np.diff(plan[:, :2], axis=0).T)))


def costmap(center, person=None, size=COSTMAP_SIZE, res=COSTMAP_RES):
    """The local costmap: a rolling window of size x size m centred on the robot, origin snapped to the cell grid.
    Returns the centres of the lethal cells (an obstacle of the room covers the cell's centre or comes within half
    a cell of it), the window's lower-left corner and the cell count per side."""
    n = int(round(size / res))
    ox = math.floor((center[0] - size / 2) / res) * res
    oy = math.floor((center[1] - size / 2) / res) * res
    xs, ys = ox + (np.arange(n) + 0.5) * res, oy + (np.arange(n) + 0.5) * res
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    d = np.min([o(X, Y) for o in bk.obstacles(person)], axis=0)
    lethal = d <= res / 2
    return dict(cells=np.column_stack([X[lethal], Y[lethal]]), lethal=lethal, origin=(ox, oy), n=n, res=res)


def point_obstacles(cm, pose, behind=None):
    """updateObstacleContainerWithCostmap: every lethal cell becomes a point obstacle, except cells behind the
    robot and further than costmap_obstacles_behind_robot_dist (the loop skips the last row and column)."""
    behind = CFG["costmap_obstacles_behind_robot_dist"] if behind is None else behind
    n, res = cm["n"], cm["res"]
    L = cm["lethal"].copy()
    L[n - 1, :] = False
    L[:, n - 1] = False
    xs = cm["origin"][0] + (np.arange(n) + 0.5) * res
    ys = cm["origin"][1] + (np.arange(n) + 0.5) * res
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    pts = np.column_stack([X[L], Y[L]])
    d = pts - pose[:2]
    keep = ~(((d @ [math.cos(pose[2]), math.sin(pose[2])]) < 0) & (np.hypot(d[:, 0], d[:, 1]) > behind))
    return pts[keep]


def prune_plan(plan, xy, dist_behind=None):
    """pruneGlobalPlan: drop the plan's poses before the first one within dist_behind of the robot."""
    dist_behind = CFG["global_plan_prune_distance"] if dist_behind is None else dist_behind
    d = np.hypot(*(plan[:, :2] - xy).T)
    close = np.nonzero(d < dist_behind)[0]
    return plan[close[0]:] if len(close) else plan


def transform_plan(plan, xy, half=COSTMAP_SIZE / 2, lookahead=None):
    """transformGlobalPlan: from the plan's pose nearest the robot, keep poses until one lies more than 85 percent
    of half the costmap from the robot or the kept plan is longer than max_global_plan_lookahead_dist; that pose is
    included and is the local goal. Returns the kept poses and the local goal's index in the plan."""
    lookahead = CFG["max_global_plan_lookahead_dist"] if lookahead is None else lookahead
    thr2 = (0.85 * half) ** 2
    sq = 1e10
    i = 0
    reached = False
    for j in range(len(plan)):
        new = float(np.sum((xy - plan[j, :2]) ** 2))
        if new > thr2:
            break
        if reached and new > sq:
            break
        if new < sq:
            sq, i = new, j
            if sq < 0.05:
                reached = True
    out = []
    length = 0.0
    while i < len(plan) and sq <= thr2 and (lookahead <= 0 or length <= lookahead):
        out.append(plan[i].copy())
        sq = float(np.sum((xy - plan[i, :2]) ** 2))
        if i > 0 and lookahead > 0:
            length += float(np.hypot(*(plan[i, :2] - plan[i - 1, :2])))
        i += 1
    if not out:
        return plan[-1:].copy(), len(plan) - 1
    return np.array(out), i - 1


def via_points(tplan, sep):
    """updateViaPointsContainer: off when global_plan_viapoint_sep <= 0; otherwise the plan's points after the
    first, each at least sep from the last one kept."""
    if sep <= 0:
        return None
    out, prev = [], 0
    for i in range(1, len(tplan)):
        if np.hypot(*(tplan[i, :2] - tplan[prev, :2])) < sep:
            continue
        out.append(tplan[i, :2].copy())
        prev = i
    return np.array(out).reshape(-1, 2)


def local_goal_yaw(plan, goal_idx, avg=3):
    """estimateLocalGoalOrientation: near the end of the plan, the goal's own yaw; otherwise the average direction
    of the next avg pieces of the plan after the local goal."""
    n = len(plan)
    if goal_idx > n - avg - 2:
        return float(plan[-1, 2])
    avg = min(avg, n - goal_idx - 1)
    a = [math.atan2(plan[i + 1, 1] - plan[i, 1], plan[i + 1, 0] - plan[i, 0]) for i in range(goal_idx, goal_idx + avg)]
    return math.atan2(np.mean(np.sin(a)), np.mean(np.cos(a)))


# ---------------------------------------------------------------- the band and its cost terms (the g2o edges)
def fast_sigmoid(x):
    return x / (1 + np.abs(x))


def pen_interval(x, lo, hi, eps):
    """penaltyBoundToInterval: 0 inside [lo + eps, hi - eps], else the distance to that interval."""
    return np.maximum(0, (lo + eps) - x) + np.maximum(0, x - (hi - eps))


def pen_below(x, a, eps):
    """penaltyBoundFromBelow: 0 when x >= a + eps, else a + eps - x."""
    return np.maximum(0, (a + eps) - x)


def kinematics(P, DT):
    """Distances, signed speeds, turn rates and the pieces' projections on the first pose's heading (EdgeVelocity)."""
    d = np.diff(P[..., :2], axis=-2)
    dist = np.hypot(d[..., 0], d[..., 1])
    proj = d[..., 0] * np.cos(P[..., :-1, 2]) + d[..., 1] * np.sin(P[..., :-1, 2])
    dth = wrap(np.diff(P[..., 2], axis=-1))
    v = dist / DT * fast_sigmoid(100 * proj)
    w = dth / DT
    return d, dist, proj, dth, v, w


EDGE_NAMES = ("time", "arc rule", "forward", "speed", "turn rate", "acceleration", "turn acceleration",
              "obstacle", "inflation", "turning radius", "via-point", "turn direction")


def residuals(P, DT, ctx, mult=1.0, split=False):
    """Every edge's error times the square root of its weight, for a batch of bands P (B, n, 3), DT (B, n - 1).
    ctx: start velocity (v0, w0), goal velocity or None (free), the obstacle association, via-points, cfg."""
    c = ctx["cfg"]
    eps = c["penalty_epsilon"]
    d, dist, proj, dth, v, w = kinematics(P, DT)
    parts = {}
    parts["time"] = math.sqrt(c["weight_optimaltime"]) * DT
    c0, s0, c1, s1 = np.cos(P[..., :-1, 2]), np.sin(P[..., :-1, 2]), np.cos(P[..., 1:, 2]), np.sin(P[..., 1:, 2])
    parts["arc rule"] = math.sqrt(c["weight_kinematics_nh"]) * np.abs((c0 + c1) * d[..., 1] - (s0 + s1) * d[..., 0])
    if c["min_turning_radius"] == 0 or c["weight_kinematics_turning_radius"] == 0:     # EdgeKinematicsDiffDrive
        parts["forward"] = math.sqrt(c["weight_kinematics_forward_drive"]) * pen_below(proj, 0, 0)
    else:                                                                              # EdgeKinematicsCarlike
        r = np.where(dth == 0, np.inf, dist / np.maximum(np.abs(dth), 1e-12))
        parts["turning radius"] = math.sqrt(c["weight_kinematics_turning_radius"]) * np.where(
            dth == 0, 0.0, pen_below(r, c["min_turning_radius"], 0))
    parts["speed"] = math.sqrt(c["weight_max_vel_x"]) * pen_interval(v, -c["max_vel_x_backwards"], c["max_vel_x"], eps)
    parts["turn rate"] = math.sqrt(c["weight_max_vel_theta"]) * pen_interval(w, -c["max_vel_theta"], c["max_vel_theta"],
                                                                             eps)
    v0, w0 = ctx["vel_start"]
    acc = [(v[..., :1] - v0) / DT[..., :1], 2 * np.diff(v, axis=-1) / (DT[..., :-1] + DT[..., 1:])]
    acw = [(w[..., :1] - w0) / DT[..., :1], 2 * np.diff(w, axis=-1) / (DT[..., :-1] + DT[..., 1:])]
    if ctx["vel_goal"] is not None:                                                    # EdgeAccelerationGoal
        acc.append((ctx["vel_goal"][0] - v[..., -1:]) / DT[..., -1:])
        acw.append((ctx["vel_goal"][1] - w[..., -1:]) / DT[..., -1:])
    acc, acw = np.concatenate(acc, axis=-1), np.concatenate(acw, axis=-1)
    parts["acceleration"] = math.sqrt(c["weight_acc_lim_x"]) * pen_interval(acc, -c["acc_lim_x"], c["acc_lim_x"], eps)
    parts["turn acceleration"] = math.sqrt(c["weight_acc_lim_theta"]) * pen_interval(acw, -c["acc_lim_theta"],
                                                                                     c["acc_lim_theta"], eps)
    A = ctx.get("assoc")
    if A is not None and len(A[0]):                                                     # EdgeInflatedObstacle
        idx, O = A
        dd = np.hypot(P[..., idx, 0] - O[:, 0], P[..., idx, 1] - O[:, 1]) - ctx.get("radius", R_ROBOT)
        parts["obstacle"] = math.sqrt(c["weight_obstacle"] * mult) * pen_below(dd, c["min_obstacle_dist"], eps)
        if c["inflation_dist"] > c["min_obstacle_dist"]:
            parts["inflation"] = math.sqrt(c["weight_inflation"]) * pen_below(dd, c["inflation_dist"], 0)
    V = ctx.get("via")
    if V is not None and len(V[0]):                                                     # EdgeViaPoint
        idx, Q = V
        parts["via-point"] = math.sqrt(c["weight_viapoint"]) * np.hypot(P[..., idx, 0] - Q[:, 0], P[..., idx, 1] - Q[:, 1])
    if ctx.get("rotdir"):                                                               # EdgePreferRotDir
        k = min(3, P.shape[-2] - 1)
        sgn = 1.0 if ctx["rotdir"] == "left" else -1.0
        parts["turn direction"] = math.sqrt(c["weight_prefer_rotdir"]) * np.maximum(0, -sgn * dth[..., :k])
    if split:
        return parts
    return np.concatenate([parts[k] for k in EDGE_NAMES if k in parts], axis=-1)


class Band:
    """One timed elastic band: poses P (n, 3) with the time steps DT (n - 1) between them; the first pose and the
    last are fixed (TimedElasticBand)."""

    def __init__(self, P, DT, cfg=CFG):
        self.P, self.DT, self.cfg = np.array(P, float), np.array(DT, float), cfg
        self.vel_start, self.vel_goal = (0.0, 0.0), (0.0, 0.0)
        self.cost, self.optimized, self.hist = None, False, None

    @classmethod
    def from_plan(cls, plan, cfg=CFG):
        """initTrajectoryToGoal(plan): a pose at every plan point, yaw along the plan (estimate_orient), the time
        to each pose from estimateDeltaT (distance / max_vel_x or turn / max_vel_theta, the larger)."""
        P = [plan[0].copy()]
        DT = []
        for i in range(1, len(plan) - 1):
            yaw = math.atan2(plan[i + 1, 1] - plan[i, 1], plan[i + 1, 0] - plan[i, 0]) if \
                cfg["global_plan_overwrite_orientation"] else plan[i, 2]
            q = np.array([plan[i, 0], plan[i, 1], yaw])
            DT.append(_delta_t(P[-1], q, cfg))
            P.append(q)
        while len(P) < cfg["min_samples"] - 1:
            q = _average(P[-1], plan[-1])
            DT.append(_delta_t(P[-1], q, cfg))
            P.append(q)
        DT.append(_delta_t(P[-1], plan[-1], cfg))
        P.append(plan[-1].copy())
        return cls(P, DT, cfg)

    @classmethod
    def from_waypoints(cls, W, th0, th1, cfg=CFG):
        """initTrajectoryToGoal(waypoints) of the homotopy planner: a pose at every waypoint facing from the one
        before, each time step the larger of distance / max_vel_x and the time to cover it from rest at acc_lim_x."""
        P = [np.array([W[0][0], W[0][1], th0])]
        DT = []
        for q in W[1:-1]:
            dd = np.array(q) - P[-1][:2]
            L = float(np.hypot(*dd))
            DT.append(max(L / cfg["max_vel_x"], math.sqrt(2 * L / cfg["acc_lim_x"])) or 0.2)
            P.append(np.array([q[0], q[1], math.atan2(dd[1], dd[0])]))
        L = float(np.hypot(*(np.array(W[-1]) - P[-1][:2])))
        DT.append(max(L / cfg["max_vel_x"], math.sqrt(2 * L / cfg["acc_lim_x"])) or 0.2)
        P.append(np.array([W[-1][0], W[-1][1], th1]))
        b = cls(P, DT, cfg)
        while len(b.P) < cfg["min_samples"]:
            b.P = np.insert(b.P, len(b.P) - 1, _average(b.P[-2], b.P[-1]), axis=0)
            b.DT = np.append(b.DT[:-1], [b.DT[-1] / 2, b.DT[-1] / 2])
        return b

    def copy(self):
        b = Band(self.P, self.DT, self.cfg)
        b.vel_start, b.vel_goal, b.cost, b.optimized = self.vel_start, self.vel_goal, self.cost, self.optimized
        return b

    def update_and_prune(self, start, goal):
        """updateAndPruneTEB, the warm start: drop the poses the robot has passed (the nearest of the next
        min(n - min_samples, 10) poses becomes the new first one), then overwrite the first pose with the robot and
        the last with the local goal."""
        n = len(self.P)
        look = min(n - self.cfg["min_samples"], 10)
        best, k = float(np.hypot(*(start[:2] - self.P[0, :2]))), 0
        for i in range(1, look + 1):
            di = float(np.hypot(*(start[:2] - self.P[i, :2])))
            if di < best:
                best, k = di, i
            else:
                break
        if k > 0:
            self.P = np.delete(self.P, range(1, k + 1), axis=0)
            self.DT = np.delete(self.DT, range(1, k + 1))
        self.P[0] = start
        self.P[-1] = goal

    def auto_resize(self):
        """autoResize (ros2-master): halve a time step longer than dt_ref + dt_hysteresis (0.4 s) and put a pose in
        its middle; merge a step shorter than dt_ref - dt_hysteresis (0.2 s) into the next (the last into the one
        before), repeated until nothing changes."""
        c = self.cfg
        P, DT = [p for p in self.P], list(self.DT)
        for _rep in range(100):
            modified = False
            i = 0
            while i < len(DT):
                if DT[i] > c["dt_ref"] + c["dt_hysteresis"] and len(DT) < c["max_samples"]:
                    DT[i] *= 0.5
                    P.insert(i + 1, _average(P[i], P[i + 1]))
                    DT.insert(i + 1, DT[i])
                    modified = True
                elif DT[i] < c["dt_ref"] - c["dt_hysteresis"] and len(DT) > c["min_samples"]:
                    if i < len(DT) - 1:
                        DT[i + 1] += DT[i]
                        del DT[i]
                        del P[i + 1]
                    else:
                        DT[i - 1] += DT[i]
                        del DT[i]
                        del P[i]
                    modified = True
                i += 1
            if not modified:
                break
        self.P, self.DT = np.array(P), np.array(DT)

    def associate(self, obst):
        """AddEdgesObstacles: for every pose but the first and the last, the obstacles closer than
        force_inclusion_factor x min_obstacle_dist, and the nearest obstacle on its left and on its right within
        cutoff_factor x min_obstacle_dist. Returns (pose index, obstacle point) pairs."""
        c = self.cfg
        idx, O = [], []
        if obst is None or len(obst) == 0:
            return np.array(idx, int), np.zeros((0, 2))
        for i in range(1, len(self.P) - 1):
            x, y, th = self.P[i]
            d = np.hypot(obst[:, 0] - x, obst[:, 1] - y) - R_ROBOT
            force = d < c["min_obstacle_dist"] * c["obstacle_association_force_inclusion_factor"]
            for j in np.nonzero(force)[0]:
                idx.append(i)
                O.append(obst[j])
            cand = (~force) & (d <= c["min_obstacle_dist"] * c["obstacle_association_cutoff_factor"])
            left = (math.cos(th) * (obst[:, 1]) - math.sin(th) * (obst[:, 0])) > 0     # cross2d(heading, centroid)
            for side in (left, ~left):
                m = cand & side
                if m.any():
                    j = np.nonzero(m)[0][np.argmin(d[m])]
                    idx.append(i)
                    O.append(obst[j])
        return np.array(idx, int), np.array(O).reshape(-1, 2)

    def ctx(self, obst=None, via=None, rotdir=None):
        return dict(cfg=self.cfg, vel_start=self.vel_start, vel_goal=self.vel_goal, assoc=self.associate(obst),
                    via=self.via_assoc(via), rotdir=rotdir)

    def via_assoc(self, via):
        """AddEdgesViaPoints: each via-point pulls the band's pose nearest to it (never the first or last)."""
        if via is None or len(via) == 0 or len(self.P) < 3:
            return None
        idx, Q = [], []
        for q in via:
            i = int(np.argmin(np.hypot(*(self.P[:, :2] - q).T)))
            i = min(i, len(self.P) - 2)
            if i < 1:
                continue
            idx.append(i)
            Q.append(q)
        return np.array(idx, int), np.array(Q).reshape(-1, 2)

    def optimise(self, obst=None, via=None, rotdir=None, keep=False):
        """optimizeTEB: no_outer_iterations passes; each resizes the band, builds the graph (the obstacle association
        is made here), takes no_inner_iterations Levenberg-Marquardt steps, and then multiplies the obstacle weight
        by weight_adapt_factor. After the last pass, the selection cost (computeCurrentCost)."""
        c = self.cfg
        mult = 1.0
        self.hist = [] if keep else None
        for p in range(c["no_outer_iterations"]):
            self.auto_resize()
            ctx = self.ctx(obst, via, rotdir)
            if keep:
                self.hist.append(dict(P=self.P.copy(), DT=self.DT.copy(), step=0, outer=p, mult=mult))
            _lm(self, ctx, mult, c["no_inner_iterations"], keep)
            if p == c["no_outer_iterations"] - 1:
                self.cost = selection_cost(self, ctx, mult)
            mult *= c["weight_adapt_factor"]
        self.optimized = True
        return self

    def command(self):
        """getVelocityCommand with control_look_ahead_poses 1, then saturateVelocity: the speed and turn rate of the
        band's first piece, each cut back to its limit."""
        c = self.cfg
        _, dist, proj, dth, _, _ = kinematics(self.P[:2], self.DT[:1])
        v = float(np.sign(proj[0]) * dist[0] / self.DT[0])
        w = float(dth[0] / self.DT[0])
        v = min(v, c["max_vel_x"]) if v > 0 else max(v, -c["max_vel_x_backwards"])
        w = float(np.clip(w, -c["max_vel_theta"], c["max_vel_theta"]))
        return v, w

    def feasible(self, cells, radius=R_ROBOT):
        """isTrajectoryFeasible: the robot's footprint at poses 0 to feasibility_check_no_poses (and at extra poses
        in between when neighbours are further apart than the inscribed radius) must not touch a lethal cell.
        Returns (True, None) or (False, index of the first pose that fails)."""
        k = min(self.cfg["feasibility_check_no_poses"], len(self.P) - 1)
        for i in range(k + 1):
            if len(cells) and np.min(np.hypot(*(cells - self.P[i, :2]).T)) < radius:
                return False, i
            if i < k:
                dd = self.P[i + 1, :2] - self.P[i, :2]
                m = int(math.ceil(np.hypot(*dd) / radius)) - 1
                for s in range(1, m + 1):
                    q = self.P[i, :2] + dd * s / (m + 1)
                    if len(cells) and np.min(np.hypot(*(cells - q).T)) < radius:
                        return False, i + s / (m + 1)
        return True, None

    def duration(self):
        return float(np.sum(self.DT))


def _delta_t(a, b, cfg):
    dt = 0.1
    if cfg["max_vel_x"] > 0:
        dt = float(np.hypot(*(b[:2] - a[:2]))) / cfg["max_vel_x"]
    if cfg["max_vel_theta"] > 0:
        dt = max(dt, abs(float(wrap(b[2] - a[2]))) / cfg["max_vel_theta"])
    return dt


def _average(a, b):
    """PoseSE2::average: the middle position and the middle heading."""
    return np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, a[2] + float(wrap(b[2] - a[2])) / 2])


def _pack(b):
    return np.concatenate([b.P[1:-1].ravel(), b.DT])


def _unpack(Z, b):
    n = len(b.P)
    B = len(Z)
    Pb = np.broadcast_to(b.P, (B, n, 3)).copy()
    Pb[:, 1:-1] = Z[:, :3 * (n - 2)].reshape(B, n - 2, 3)
    return Pb, Z[:, 3 * (n - 2):]


def _lm(b, ctx, mult, iters, keep):
    """Levenberg-Marquardt on the band's free numbers (all poses but the first and last, and every time step), with
    g2o's rule (OptimizationAlgorithmLevenberg::solve): at the start of each pass lambda = 1e-5 x the largest
    diagonal entry of J^T J; each step solves (J^T J + lambda I) dx = -J^T r; a step that lowers the cost is kept and
    lambda is multiplied by max(1/3, min(2/3, 1 - (2 rho - 1)^3)), rho being the cost drop over the predicted drop;
    a step that does not is undone, lambda is multiplied by nu and nu doubles (nu starts at 2), up to 10 tries.
    J comes from central differences (g2o also differentiates TEB's edges numerically). Time steps stay at 0.01 s
    or more."""
    z = _pack(b)
    m = len(z)

    def res(Z):
        Pb, Db = _unpack(Z, b)
        return residuals(Pb, Db, ctx, mult)

    r = res(z[None])[0]
    cst = float(r @ r)
    nT = 3 * (len(b.P) - 2)
    lam, nu = None, 2.0
    for s in range(iters):
        e = 1e-6
        F = res(np.vstack([z + e * np.eye(m), z - e * np.eye(m)]))
        J = ((F[:m] - F[m:]) / (2 * e)).T
        H, g = J.T @ J, J.T @ r
        if lam is None:
            lam = 1e-5 * float(np.max(np.abs(np.diag(H))))
        stop = True
        for _try in range(10):
            dx = -np.linalg.solve(H + lam * np.eye(m), g)
            zn = z + dx
            zn[nT:] = np.maximum(zn[nT:], 0.01)
            rn = res(zn[None])[0]
            cn = float(rn @ rn)
            rho = (cst - cn) / (float(dx @ (lam * dx - g)) + 1e-3)
            if rho > 0 and np.isfinite(cn):
                lam *= max(1 / 3, min(2 / 3, 1 - (2 * rho - 1) ** 3))
                nu = 2.0
                z, r, cst = zn, rn, cn
                stop = False
                break
            lam *= nu
            nu *= 2
        b.P, b.DT = [a[0] for a in _unpack(z[None], b)]
        if keep:
            b.hist.append(dict(P=b.P.copy(), DT=b.DT.copy(), step=s + 1, mult=mult))
        if stop:
            break


def selection_cost(b, ctx, mult):
    """computeCurrentCost: the sum of every edge's weighted squared error, the obstacle edges times
    selection_obst_cost_scale and the via-point edges times selection_viapoint_cost_scale."""
    c = b.cfg
    parts = residuals(b.P[None], b.DT[None], ctx, mult, split=True)
    tot = 0.0
    for k, r in parts.items():
        s = float(np.sum(r ** 2))
        if k in ("obstacle", "inflation"):
            s *= c["selection_obst_cost_scale"]
        elif k == "via-point":
            s *= c["selection_viapoint_cost_scale"]
        tot += s
    return tot


def band_cost(b, obst=None, mult=1.0):
    """The band's own cost with the set weights (no selection scaling), and each edge type's share."""
    parts = residuals(b.P[None], b.DT[None], b.ctx(obst), mult, split=True)
    return {k: float(np.sum(r ** 2)) for k, r in parts.items()}


# ---------------------------------------------------------------- homotopy classes
def h_signature(P, DT, obst, steps=10, t_end=120.0):
    """HSignature3d::calculateHSignature: one number per obstacle. The band is a line in (x, y, time); each static
    obstacle is a vertical line from time 0 to 120 s; the band's segments are cut into 10 steps and the Biot-Savart
    field of the obstacle's line is summed along them, then divided by 4 pi. For a static obstacle each step adds
    the angle the band turns through as seen from the obstacle, times a weight between 1 and 2, so the sign says
    on which side the band passes: positive when the obstacle is on the band's left."""
    if obst is None or len(obst) == 0:
        return np.zeros(0)
    t = np.concatenate([[0], np.cumsum(DT)])
    H = np.zeros(len(obst))
    for k in range(len(P) - 1):
        z1, z2 = P[k, :2], P[k + 1, :2]
        dv = np.array([z2[0] - z1[0], z2[1] - z1[1], t[k + 1] - t[k]])
        if np.linalg.norm(dv) < 1e-15:
            continue
        dl = dv / steps
        for s in range(steps):
            r = np.array([z1[0], z1[1], t[k]]) + s * dl
            a, bb = obst[:, 0] - r[0], obst[:, 1] - r[1]                       # d = (a, b, 0): r to the obstacle
            rho2 = a * a + bb * bb
            c1, c2 = -r[2], t_end - r[2]
            n1, n2 = np.sqrt(rho2 + c1 * c1), np.sqrt(rho2 + c2 * c2)
            H += (bb * dl[0] - a * dl[1]) / rho2 * (c2 / n2 - c1 / n1)
    return H / (4 * math.pi)


def same_class(h1, h2, thr=None):
    """HSignature3d::isEqual: the same class when, for every obstacle that both bands pass closely enough to give a
    value of at least h_signature_threshold, the two values have the same sign."""
    thr = CFG["h_signature_threshold"] if thr is None else thr
    m = (np.abs(h1) >= thr) & (np.abs(h2) >= thr)
    return bool(np.all(np.sign(h1[m]) == np.sign(h2[m])))


def roadmap(start, goal, obst, cfg, rng):
    """ProbRoadmapGraph::createGraph: roadmap_graph_no_samples random points in a rectangle from start to goal,
    roadmap_graph_area_width wide; an edge joins two points when it heads forward (its direction's dot product with
    the start-to-goal direction is above obstacle_heading_threshold) and passes no obstacle closer than
    min_obstacle_dist. Returns the vertices (start first, goal last) and the edge list."""
    diff = goal[:2] - start[:2]
    L = float(np.hypot(*diff))
    u = diff / L
    nrm = np.array([-u[1], u[0]])
    W = cfg["roadmap_graph_area_width"]
    S = [start[:2] + rng.uniform(0, L) * u + (rng.uniform(0, W) - W / 2) * nrm
         for _ in range(cfg["roadmap_graph_no_samples"])]
    V = np.array([start[:2]] + S + [goal[:2]])
    E = []
    for i in range(len(V) - 1):
        for j in range(len(V)):
            if i == j:
                continue
            e = V[j] - V[i]
            if np.dot(e / np.hypot(*e), u) <= cfg["obstacle_heading_threshold"]:
                continue
            if obst is not None and len(obst) and _seg_hits(V[i], V[j], obst, cfg["min_obstacle_dist"]):
                continue
            E.append((i, j))
    return V, E


def _seg_hits(a, b, obst, dmin):
    """PointObstacle::checkLineIntersection: the segment passes closer than dmin to a point obstacle."""
    e = b - a
    t = np.clip(((obst - a) @ e) / (e @ e), 0, 1)
    q = a + t[:, None] * e
    return bool(np.any(np.hypot(*(obst - q).T) < dmin))


def depth_first(V, E, cap=400):
    """GraphSearchInterface::DepthFirst: every path from the start (vertex 0) to the goal (the last vertex), in the
    order the recursion finds them (goal first among the neighbours, then deeper). Our cap of 400 paths keeps the
    pure-Python search short; the C++ search stops when max_number_classes bands exist."""
    adj = {i: [j for (a, j) in E if a == i] for i in range(len(V))}
    goal = len(V) - 1
    out = []

    def go(visited):
        if len(out) >= cap:
            return
        last = visited[-1]
        if goal in adj[last]:
            out.append(visited + [goal])
        for j in adj[last]:
            if j in visited or j == goal:
                continue
            go(visited + [j])

    go([0])
    return out


# ---------------------------------------------------------------- the homotopy class planner
class Planner:
    """HomotopyClassPlanner: keeps up to max_number_classes bands, one per homotopy class, from cycle to cycle."""

    def __init__(self, cfg=CFG, seed=SEED):
        self.cfg, self.rng = cfg, np.random.default_rng(seed)
        self.tebs, self.best = [], None
        self.initial_h = None

    def plan(self, tplan, vel, obst, via=None, rotdir=None, keep=False):
        """plan(): the steps in the order the code runs them. Returns a record of every step."""
        c = self.cfg
        start, goal = tplan[0], tplan[-1]
        rec = dict(start=start.copy(), goal=goal.copy())
        # 1. updateAllTEBs: start again if the local goal jumped, else the warm start of every band
        if self.tebs and (np.hypot(*(goal[:2] - self.tebs[0].P[-1, :2])) >= c["force_reinit_new_goal_dist"] or
                          abs(float(wrap(goal[2] - self.tebs[0].P[-1, 2]))) >= c["force_reinit_new_goal_angular"]):
            self.tebs, self.best = [], None
            rec["reinit"] = True
        for b in self.tebs:
            b.update_and_prune(start, goal)
            b.vel_start = vel
        rec["warm"] = [b.copy() for b in self.tebs]
        # 2. renewAndAnalyzeOldTebs: the best band first; drop a band whose class is already taken
        if self.best in self.tebs:
            self.tebs.remove(self.best)
            self.tebs.insert(0, self.best)
        classes, kept = [], []
        for b in self.tebs:
            h = h_signature(b.P, b.DT, obst)
            if any(same_class(h, g) for g in classes):
                continue
            classes.append(h)
            kept.append(b)
        self.tebs = kept
        rec["dropped_duplicates"] = len(rec["warm"]) - len(kept)
        n_before = len(self.tebs)
        if c["delete_detours_backwards"]:
            self._delete_detours(classes)
        rec["dropped_detours"] = n_before - len(self.tebs)
        # 3. the band from the global plan (addAndInitNewTeb(initial_plan)), if its class is new
        b0 = Band.from_plan(tplan, c)
        b0.vel_start = vel
        h0 = h_signature(b0.P, b0.DT, obst)
        self.initial_h = h0
        rec["plan_band"] = b0.copy()
        init_band = None                                    # getInitialPlanTEB: the band in the plan's class
        if len(self.tebs) < c["max_number_classes"] and not any(same_class(h0, g) for g in classes):
            self.tebs.append(b0)
            classes.append(h0)
            init_band = b0
            rec["plan_band_added"] = True
        else:
            rec["plan_band_added"] = False
            match = [b for b, g in zip(self.tebs, classes) if same_class(h0, g)]
            init_band = match[0] if match else None
        # 4. explore new classes: the roadmap and depth-first search
        rec["roadmap"] = None
        if len(self.tebs) < c["max_number_classes"]:
            if np.hypot(*(goal[:2] - start[:2])) < c["xy_goal_tolerance"]:
                pass
            else:
                V, E = roadmap(start, goal, obst, c, self.rng)
                paths = depth_first(V, E)
                new, verdicts = [], []
                for path in paths:
                    if len(self.tebs) >= c["max_number_classes"]:
                        break
                    b = Band.from_waypoints([V[k] for k in path], start[2], goal[2], c)
                    b.vel_start = vel
                    h = h_signature(b.P, b.DT, obst)
                    if any(same_class(h, g) for g in classes):
                        verdicts.append((path, "taken"))
                        continue
                    self.tebs.append(b)
                    classes.append(h)
                    new.append((path, b.copy()))
                    verdicts.append((path, "new"))
                rec["roadmap"] = dict(V=V, E=E, paths=paths, new=new, verdicts=verdicts)
        rec["candidates_init"] = [b.copy() for b in self.tebs]
        # 5. optimizeAllTEBs: every band, 4 passes of 5 steps
        for b in self.tebs:
            b.optimise(obst, via, rotdir, keep=keep)
        rec["hist"] = [b.hist for b in self.tebs] if keep else None
        # 6. selectBestTeb: the lowest cost; the last best's cost times selection_cost_hysteresis, the band in the
        #    global plan's class times selection_prefer_initial_plan
        costs = []
        for b in self.tebs:
            cst = b.cost
            if b is self.best:
                cst *= c["selection_cost_hysteresis"]
            elif b is init_band:
                cst *= c["selection_prefer_initial_plan"]
            costs.append(cst)
        k = int(np.argmin(costs))
        last_best = self.best
        self.best = self.tebs[k]
        rec.update(candidates=[b.copy() for b in self.tebs], costs=costs, best=k,
                   init_idx=next((i for i, b in enumerate(self.tebs) if b is init_band), None),
                   last_best_idx=next((i for i, b in enumerate(self.tebs) if b is last_best), None),
                   classes=[h_signature(b.P, b.DT, obst) for b in self.tebs])
        return rec

    def _delete_detours(self, classes):
        """deletePlansDetouringBackwards: drop a band that starts off more than 90 degrees from the best band's
        direction, or takes more than 3 times as long."""
        c = self.cfg
        if len(self.tebs) < 2 or self.best not in self.tebs:
            return
        a0 = _start_dir(self.best, c["length_start_orientation_vector"])
        if a0 is None:
            return
        dur = max(self.best.duration(), 1.0)
        keep = []
        for b, h in zip(self.tebs, classes):
            if b is self.best:
                keep.append((b, h))
                continue
            a = _start_dir(b, c["length_start_orientation_vector"])
            if a is None or abs(float(wrap(a - a0))) > c["detours_orientation_tolerance"] or \
                    b.duration() / dur > c["max_ratio_detours_duration_best_duration"]:
                continue
            keep.append((b, h))
        self.tebs = [b for b, _ in keep]
        classes[:] = [h for _, h in keep]

    def clear(self):
        self.tebs, self.best = [], None


def _start_dir(b, L):
    for p in b.P:
        d = b.P[0, :2] - p[:2]
        if np.hypot(*d) > L:
            return math.atan2(d[1], d[0])
    return None


# ---------------------------------------------------------------- one controller cycle, and the drive
def oscillating(cmds, cfg=CFG):
    """FailureDetector::detect: over the buffered commands (filled at least half), each speed divided by its limit;
    oscillating when the mean speed and the mean turn rate are both below 0.1 and the turn rate changed sign more
    than once."""
    cap = int(round(cfg["oscillation_filter_duration"] / CYCLE))
    if len(cmds) < cap / 2:
        return False
    v = np.array([c[0] / (cfg["max_vel_x"] if c[0] > 0 else cfg["max_vel_x_backwards"]) for c in cmds])
    w = np.array([c[1] / cfg["max_vel_theta"] for c in cmds])
    flips = int(np.sum(np.sign(w[1:]) != np.sign(w[:-1])))
    return abs(v.mean()) < cfg["oscillation_v_eps"] and abs(w.mean()) < cfg["oscillation_omega_eps"] and flips > 1


def drive_step(x, v, w, cmd, h=CYCLE, sub=20):
    """Our robot (RO-058) for one cycle with the command held: the speed changes by at most 0.5 m/s^2, both wheels
    stay within 0.6 m/s; the turn rate follows at once within the wheel limit."""
    for _ in range(sub):
        dt = h / sub
        v = float(np.clip(v + np.clip(cmd[0] - v, -bk.A_MAX * dt, bk.A_MAX * dt), -bk.V_WHEEL, bk.V_WHEEL))
        lim = (bk.V_WHEEL - abs(v)) / (bk.L_AXLE / 2)
        w = float(np.clip(cmd[1], -lim, lim))
        x = x + dt * np.array([v * math.cos(x[2] + w * dt / 2), v * math.sin(x[2] + w * dt / 2), w])
    return x, v, w


def run_drive(person=bk.PERSON, t_person=bk.T_PERSON, t_end=20.0, cfg=CFG, keep_at=(), seed=SEED, homotopy=True):
    """The whole drive, one controller cycle every 0.1 s (computeVelocityCommands): measure; prune and cut the plan;
    point obstacles from the costmap; the planner; the feasibility check; the command. keep_at: cycle times (s)
    whose solver steps are stored for the animations. Returns the cycle records."""
    cfg = dict(cfg, enable_homotopy_class_planning=homotopy, max_number_classes=cfg["max_number_classes"] if homotopy
               else 1)
    plan = global_plan()
    x = np.array(bk.START[:3], float)
    v = w = 0.0
    planner = Planner(cfg, seed)
    out = []
    t = 0.0
    n_infeasible, t_infeasible = 0, -1e9
    buf, t_osc, pref = [], -1e9, None
    while t < t_end - 1e-9:
        seen = person if (person is not None and t >= t_person - 1e-9) else None
        rec = dict(t=t, x=x.copy(), v=v, w=w, person=seen)
        # Nav2's goal checker, with RO-058's tolerances
        if np.hypot(*(x[:2] - bk.GOAL[:2])) < cfg["xy_goal_tolerance"] and abs(float(wrap(x[2] - bk.GOAL[2]))) < YAW_TOL \
                and abs(v) < 0.02:
            rec["arrived"] = True
            out.append(rec)
            break
        plan = prune_plan(plan, x[:2], cfg["global_plan_prune_distance"])
        tplan, gidx = transform_plan(plan, x[:2], lookahead=cfg["max_global_plan_lookahead_dist"])
        # configureBackupModes: the shorter horizon after an infeasible plan
        if cfg["shrink_horizon_backup"] and gidx < len(plan) - 1 and (
                n_infeasible > 0 or t - t_infeasible < cfg["shrink_horizon_min_duration"]):
            red = gidx // 2 if n_infeasible <= 9 else gidx // 4
            new = len(tplan) - red - 1
            if new > 0 and gidx - red >= 0:
                tplan, gidx = tplan[:new], gidx - red
            rec["shrunk"] = True
        # configureBackupModes: oscillation recovery (FailureDetector on the last 10 s of commands)
        rotdir = None
        if cfg["oscillation_recovery"] and buf:
            osc = oscillating(buf[-int(round(cfg["oscillation_filter_duration"] / CYCLE)):], cfg)
            recent = t - t_osc < cfg["oscillation_recovery_min_duration"]
            if osc:
                if not recent:
                    pref = "left" if w > 0 else "right"
                t_osc = t
                rec["oscillating"] = True
            elif not recent:
                pref = None
            rotdir = pref
        goal = tplan[-1].copy()
        goal[2] = local_goal_yaw(plan, gidx) if cfg["global_plan_overwrite_orientation"] else goal[2]
        tplan = np.vstack([x, tplan[1:-1], goal]) if len(tplan) >= 2 else np.vstack([x, goal])
        via = via_points(tplan, cfg["global_plan_viapoint_sep"])
        cm = costmap(x, seen)
        obst = point_obstacles(cm, x, cfg["costmap_obstacles_behind_robot_dist"])
        keep = any(abs(t - k) < 1e-6 for k in keep_at)
        r = planner.plan(tplan, (v, w), obst, via=via, rotdir=rotdir, keep=keep)
        best = planner.best
        ok, bad = best.feasible(cm["cells"])
        rec.update(plan=plan.copy(), tplan=tplan, goal=goal, n_lethal=len(cm["cells"]), n_obst=len(obst),
                   cm=cm if keep else None, obst=obst if keep else None, planner=r, feasible=ok, bad_pose=bad)
        if ok:
            cmd = best.command()
            n_infeasible = 0
        else:                                           # clearPlanner, count, and an exception to the server
            cmd = (0.0, 0.0)
            planner.clear()
            n_infeasible += 1
            t_infeasible = t
        rec["cmd"] = cmd
        buf.append(cmd)
        out.append(rec)
        x, v, w = drive_step(x, v, w, cmd)
        t = round(t + CYCLE, 10)
    return out


def arrival(run):
    return run[-1]["t"] if run[-1].get("arrived") else None


def results():
    """Every run the Note quotes, computed once and cached by this file's and bandkit's text."""
    import hashlib
    import pickle
    import tempfile
    from pathlib import Path
    here = Path(__file__).parent
    key = hashlib.sha1((here / "tebkit.py").read_bytes() + (here / "bandkit.py").read_bytes()).hexdigest()[:12]
    f = Path(tempfile.gettempdir()) / "ro232_cache" / f"teb_{key}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    R = {}
    R["person"] = run_drive(keep_at=(0.0, 2.4))
    R["clear"] = run_drive(person=None)
    R["left"] = run_drive(person=bk.PERSON_LEFT, keep_at=(2.4, 2.5))
    for w in (1.0, 50.0):                     # via-points every 0.3 m (the package's Nav2 example file uses weight 50)
        R[f"via{w:g}"] = run_drive(cfg=dict(CFG, global_plan_viapoint_sep=0.3, weight_viapoint=w))
    f.parent.mkdir(exist_ok=True)
    f.write_bytes(pickle.dumps(R))
    return R


# ---------------------------------------------------------------- car-like robots
# RO-055's car: wheelbase 2.5 m, tightest circle 5 m. TEB's car-like set-up: min_turning_radius > 0 swaps the
# forward-drive edge for the turning-radius edge (buildGraph); cmd_angle_instead_rotvel turns omega into a steering
# angle. Speeds as in Roesmann et al. 2017's test: -1 <= v <= 1 m/s, dt_ref 0.2 s; the turn rate is limited only by
# the turning radius (max_vel_theta set out of the way).
CAR = dict(CFG, min_turning_radius=5.0, wheelbase=2.5, cmd_angle_instead_rotvel=True, max_vel_x=1.0,
           max_vel_x_backwards=1.0, max_vel_theta=10.0, dt_ref=0.2)
CAR_START, CAR_GOAL = np.array([2.0, 0.0, 0.0]), np.array([-2.0, 0.0, math.pi])   # Roesmann et al. 2017, Table I


def steering_angle(v, w, cfg=CAR):
    """convertTransRotVelToSteeringAngle: the radius v / omega, never below 0.95 x min_turning_radius, gives the
    front wheels' angle atan(wheelbase / radius)."""
    if v == 0 or w == 0:
        return 0.0
    r = v / w
    if abs(r) < 0.95 * cfg["min_turning_radius"]:
        r = math.copysign(0.95 * cfg["min_turning_radius"], r)
    return math.atan(cfg["wheelbase"] / r)


def car_turn(rho=5.0, acc=False, from_plan=False, cycles=25):
    """Turn the car round from CAR_START to CAR_GOAL with no obstacles. from_plan False: the paper's test, a band
    through 5 equidistant waypoints on the straight line, no acceleration limits. from_plan True: the band starts
    from the shortest Reeds-Shepp path (what a car's global planner would give), poses 0.25 m apart, headings kept.
    acc: TEB's default acceleration limits (0.5 m/s^2, 0.5 rad/s^2), stopping at the goal. Each cycle is one
    optimizeTEB call (4 passes of 5 steps) on the same problem. Returns the band after every cycle."""
    import carpaths as cp
    cfg = dict(CAR, min_turning_radius=rho)
    if not acc:
        cfg.update(weight_acc_lim_x=0.0, weight_acc_lim_theta=0.0)
    if from_plan:
        S = np.array(cp.sample(tuple(CAR_START), cp.reeds_shepp(tuple(CAR_START), tuple(CAR_GOAL), rho), rho, ds=0.25))
        b = Band.from_plan(S, dict(cfg, global_plan_overwrite_orientation=False))
    else:
        W = [CAR_START[:2] + (CAR_GOAL[:2] - CAR_START[:2]) * k / 4 for k in range(5)]
        b = Band.from_waypoints(W, CAR_START[2], CAR_GOAL[2], cfg)
    b.cfg = cfg
    b.vel_goal = (0.0, 0.0) if acc else None
    hist = [b.copy()]
    for _ in range(cycles):
        b.optimise()
        hist.append(b.copy())
    return hist


def band_shape(b):
    """Length, duration, number of direction changes and the tightest turning radius of a band."""
    d = np.hypot(*np.diff(b.P[:, :2], axis=0).T)
    proj = np.diff(b.P[:, 0]) * np.cos(b.P[:-1, 2]) + np.diff(b.P[:, 1]) * np.sin(b.P[:-1, 2])
    s = np.sign(proj)[d > 1e-3]
    dth = np.abs(wrap(np.diff(b.P[:, 2])))
    r = np.where(dth > 1e-9, d / np.maximum(dth, 1e-12), np.inf)[d > 1e-3]
    return dict(length=float(d.sum()), T=b.duration(), reversals=int(np.sum(s[1:] * s[:-1] < 0)), r_min=float(r.min()),
                n=len(b.P))


def car_results():
    """The car runs the Note quotes (cached like results())."""
    import hashlib
    import pickle
    import tempfile
    from pathlib import Path
    here = Path(__file__).parent
    key = hashlib.sha1((here / "tebkit.py").read_bytes() + (here / "carpaths.py").read_bytes()).hexdigest()[:12]
    f = Path(tempfile.gettempdir()) / "ro232_cache" / f"car_{key}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    C = dict(A=car_turn(5.0), B=car_turn(5.0, acc=True, from_plan=True),
             table={rho: band_shape(car_turn(rho)[-1]) for rho in (0.75, 1.75, 3.0, 4.25, 6.75, 8.0)})
    f.parent.mkdir(exist_ok=True)
    f.write_bytes(pickle.dumps(C))
    return C


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # a straight band to a goal 1.5 m ahead on an empty floor: the speed settles just inside max_vel_x
        b = Band.from_plan(np.array([[0, 0, 0], [0.75, 0, 0], [1.5, 0, 0]], float))
        b.optimise()
        v = np.diff(b.P[:, 0]) / b.DT
        assert 0.5 < v.max() < 0.6 and abs(b.P[:, 1]).max() < 1e-6, (v, b.P)
        # the H-signature: passing an obstacle on the left and on the right gives opposite signs
        o = np.array([[0.75, 0.0]])
        hl = h_signature(np.array([[0, 0, 0], [0.75, 0.4, 0], [1.5, 0, 0]]), np.array([1.0, 1.0]), o)
        hr = h_signature(np.array([[0, 0, 0], [0.75, -0.4, 0], [1.5, 0, 0]]), np.array([1.0, 1.0]), o)
        assert hl[0] < 0 < hr[0] and not same_class(hl, hr), (hl, hr)
        print("self-check passed", v.round(3), hl, hr)
