"""Nav2's DWB controller and the dynamic window approach, re-written in Python (no output when imported; run it to
check itself).

This is our own Python version of DWB's algorithm, written from the navigation2 code on `main`
(commit 3286119, read 2026-10-12) with its parameter values. It is not Nav2's software running. Files followed:
- nav2_controller/src/controller_server.cpp, parameter_handler.cpp, plugins/feasible_path_handler.cpp,
  plugins/simple_goal_checker.cpp, plugins/simple_progress_checker.cpp: the 20 Hz loop, plan pruning, goal check;
- nav2_dwb_controller/dwb_core/src/dwb_local_planner.cpp: computeVelocityCommands, coreScoringAlgorithm,
  scoreTrajectory (sum of scale x raw score, lowest total wins, illegal trajectories dropped);
- dwb_plugins: standard_traj_generator.cpp, limited_accel_generator.cpp, xy_theta_iterator.cpp,
  one_d_velocity_iterator.hpp, kinematic_parameters.hpp (the velocity samples and the rollouts);
- dwb_critics: base_obstacle, map_grid (+ costmap_queue), path_dist, path_align, goal_dist, goal_align,
  rotate_to_goal, oscillation, prefer_forward, twirling, obstacle_footprint;
- nav2_costmap_2d inflation_layer.hpp (computeCost) and cost_values.hpp.

Parameters: the DWB example of the Nav2 configuration guide (docs.nav2.org, rolling), which nav2_system_tests on main
also uses, with our robot's limits in place of the TurtleBot's (see PARAMS). Simplifications, all listed in the Note:
- the local costmap is built from the exact room geometry (every obstacle in the 3 m window is known, the person
  from 2.4 s), and a cell's cost comes from the exact distance from its centre to the nearest obstacle, not from
  the laser's marked cells;
- localisation is perfect (the map and odom frames agree), odometry gives the true speed;
- the global plan is made once (RO-034's A* route), as in RO-058; Nav2's behaviour tree would replan at 1 Hz;
- the robot base follows each command within 0.5 m/s^2 (speed) and 3.2 rad/s^2 (turn rate) and 0.6 m/s per wheel.

Contents: the room and robot (map data copied from RO-058), the costmap, the velocity samples (dynamic window), the
rollouts, the critics, one controller cycle, and the whole drive. W16 copies this file for RO-080."""
import math

import numpy as np

# ---------------------------------------------------------------- the room and the robot (RO-058's map data, copied)
W_ROOM, H_ROOM, DOOR = 7.0, 4.0, (3.0, 4.2)
TABLE = np.array([(3.0, 1.0), (5.0, 1.0), (5.5, 2.5), (3.5, 3.0)])   # counter-clockwise corners
CAB = [(5.6, 7.0, 3.4, 4.0), (6.4, 7.0, 2.4, 4.0)]                    # cabinet: two rectangles (x0, x1, y0, y1)
POLES = [(1.0, 3.0), (6.0, 0.8)]
POLE_R = 0.1
WALLS = [((0, 0), (W_ROOM, 0)), ((W_ROOM, 0), (W_ROOM, H_ROOM)), ((0, H_ROOM), (0, 0)),
         ((0, H_ROOM), (DOOR[0], H_ROOM)), ((DOOR[1], H_ROOM), (W_ROOM, H_ROOM))]
L_AXLE, V_WHEEL, A_MAX, R_BODY = 0.2, 0.6, 0.5, 0.25                  # RO-001 / RO-054 robot
START = np.array([2.0, 1.0, math.radians(30)])
GOAL = np.array([3.6, 3.5, math.radians(90)])
# RO-034's A* route on 0.5 m cells (3.414 m between cell centres) with the robot's position in place of the start
# cell's centre and the door pose in place of the goal cell's centre, points on a straight piece dropped (RO-058)
ROUTE_PTS = np.array([START[:2], (2.75, 1.75), (2.75, 3.25), (3.25, 3.75), GOAL[:2]])
ROUTE_CELLS = np.array([(2.25, 1.25), (2.75, 1.75), (2.75, 2.25), (2.75, 2.75), (2.75, 3.25), (3.25, 3.75),
                        (3.75, 3.75)])
PERSON = np.array([2.90, 2.75])
PERSON_R = 0.2
T_PERSON = 2.4

# ---------------------------------------------------------------- parameters (name in Nav2: value)
PARAMS = dict(
    controller_frequency=20.0,          # controller_server (default and bring-up)
    failure_tolerance=0.3,              # controller_server, bring-up nav2_params.yaml
    min_x_velocity_threshold=0.001,     # bring-up
    min_theta_velocity_threshold=0.001,
    prune_distance=2.0,                 # FeasiblePathHandler default
    xy_goal_tolerance=0.25, yaw_goal_tolerance=0.25,   # SimpleGoalChecker defaults, stateful
    path_length_tolerance=1.0,
    required_movement_radius=0.5, movement_time_allowance=10.0,   # SimpleProgressChecker
    # local costmap (bring-up): rolling 3 m x 3 m window, 0.05 m cells, updated at 5 Hz
    costmap_size=3.0, resolution=0.05, update_frequency=5.0,
    robot_radius=R_BODY,                # ours (bring-up: 0.22 m, a TurtleBot)
    inflation_radius=0.70, cost_scaling_factor=3.0,   # bring-up local costmap
    # DWB (configuration-guide example; our robot's limits marked "ours")
    trajectory_generator="standard",    # dwb_plugins::StandardTrajectoryGenerator (the default)
    sim_time=1.7, discretize_by_time=False, time_granularity=0.5,
    linear_granularity=0.05, angular_granularity=0.025,
    vx_samples=20, vy_samples=5, vtheta_samples=20,
    min_vel_x=0.0, max_vel_x=V_WHEEL,   # ours (example: 0.26 m/s)
    max_vel_theta=1.0,                  # example; also our robot's turn limit at 0.5 m/s (it spins at 6 rad/s at rest)
    max_speed_xy=V_WHEEL, min_speed_xy=0.0, min_speed_theta=0.0,
    acc_lim_x=A_MAX, decel_lim_x=-A_MAX,  # ours (example: 2.5 / -2.5)
    acc_lim_theta=3.2, decel_lim_theta=-3.2,   # example (our robot had no stated limit)
    critics=["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"],
    scales=dict(RotateToGoal=32.0, Oscillation=1.0, BaseObstacle=0.02, GoalAlign=24.0, PathAlign=32.0,
                PathDist=32.0, GoalDist=24.0, PreferForward=1.0, Twirling=0.0),
    forward_point_distance=0.1,         # PathAlign and GoalAlign in the example (code default 0.325)
    slowing_factor=5.0, trans_stopped_velocity=0.25,
    oscillation_reset_dist=0.05, oscillation_reset_angle=0.2, x_only_threshold=0.05,
)
LETHAL, INSCRIBED, NO_INFO = 254, 253, 255
EPS = 1e-5


# ---------------------------------------------------------------- geometry
def _seg_dist(px, py, a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]
    t = np.clip(((px - a[0]) * ex + (py - a[1]) * ey) / (ex * ex + ey * ey), 0, 1)
    return np.hypot(px - a[0] - t * ex, py - a[1] - t * ey)


def _poly_dist(px, py, P):
    """Signed distance to a convex polygon given counter-clockwise: positive outside, negative inside."""
    best = np.full(np.shape(px), np.inf)
    inside = np.ones(np.shape(px), bool)
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        best = np.minimum(best, _seg_dist(px, py, a, b))
        inside &= ((b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0])) >= 0
    return np.where(inside, -best, best)


def obstacle_dist(px, py, person=None):
    """Distance from points to the nearest obstacle surface (negative inside one): table, cabinet, poles, walls,
    and the person when given."""
    px, py = np.asarray(px, float), np.asarray(py, float)
    d = [_poly_dist(px, py, TABLE)]
    for x0, x1, y0, y1 in CAB:
        d.append(_poly_dist(px, py, np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])))
    d += [np.hypot(px - c[0], py - c[1]) - POLE_R for c in POLES]
    d += [_seg_dist(px, py, a, b) for a, b in WALLS]
    if person is not None:
        d.append(np.hypot(px - person[0], py - person[1]) - PERSON_R)
    return np.min(d, axis=0)


def gap(px, py, person=None):
    """Gap between the robot's disk and the nearest obstacle (negative: overlap)."""
    return obstacle_dist(px, py, person) - R_BODY


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


# ---------------------------------------------------------------- the global plan
def make_plan(pts=ROUTE_PTS, goal_yaw=GOAL[2], res=PARAMS["resolution"]):
    """The global plan as Nav2 receives it: poses about one costmap cell apart, each facing along the plan, the
    last facing the goal heading."""
    P = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / res)))
        P += [a + (b - a) * k / n for k in range(1, n + 1)]
    P = np.array(P)
    d = np.diff(P, axis=0)
    yaw = np.arctan2(d[:, 1], d[:, 0])
    return np.column_stack([P, np.append(yaw, goal_yaw)])


CELL = 0.5


def blocked_cells(person=None):
    """RO-034's grid: a 0.5 m cell is blocked when it overlaps an obstacle (the person too, once seen)."""
    from shapely.geometry import Point, Polygon, box as sbox
    from shapely.ops import unary_union
    parts = [Polygon(TABLE)] + [sbox(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB] + \
            [Point(p).buffer(POLE_R, quad_segs=64) for p in POLES]
    if person is not None:
        parts.append(Point(person).buffer(PERSON_R, quad_segs=64))
    u = unary_union(parts)
    nx, ny = int(W_ROOM / CELL), int(H_ROOM / CELL)
    return {(i, j) for i in range(nx) for j in range(ny)
            if sbox(i * CELL, j * CELL, (i + 1) * CELL, (j + 1) * CELL).intersection(u).area > 0}


def astar(start, goal, person=None):
    """RO-034's A* (copied from RO-058): 8 neighbours, octile heuristic, no cutting the corner of a blocked cell.
    Returns the cell centres from the start cell to the goal cell."""
    import heapq
    B = blocked_cells(person)
    nx, ny = int(W_ROOM / CELL), int(H_ROOM / CELL)
    free = lambda c: 0 <= c[0] < nx and 0 <= c[1] < ny and c not in B
    s2 = math.sqrt(2) * CELL
    h = lambda c: s2 * min(abs(c[0] - goal[0]), abs(c[1] - goal[1])) + CELL * abs(
        abs(c[0] - goal[0]) - abs(c[1] - goal[1]))
    g, came, openl, closed = {start: 0.0}, {}, [(h(start), h(start), start)], set()
    while openl:
        _, _, c = heapq.heappop(openl)
        if c in closed:
            continue
        if c == goal:
            break
        closed.add(c)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (c[0] + dx, c[1] + dy)
                if (dx, dy) == (0, 0) or not free(n):
                    continue
                if dx and dy and not (free((c[0] + dx, c[1])) and free((c[0], c[1] + dy))):
                    continue
                gn = g[c] + (s2 if dx and dy else CELL)
                if gn < g.get(n, np.inf) - 1e-12:
                    g[n], came[n] = gn, c
                    heapq.heappush(openl, (gn + h(n), h(n), n))
    path = [goal]
    while path[-1] != start:
        path.append(came[path[-1]])
    return np.array([((i + 0.5) * CELL, (j + 0.5) * CELL) for i, j in path[::-1]]), g[goal]


def global_plan(xy, person=None):
    """The planner server's answer from the robot's position: A* cell centres with the robot's position in place
    of its cell's centre and the door pose in place of the goal cell's centre, points on a straight piece dropped
    (as RO-058 did for the first plan), then poses one costmap cell apart."""
    s = (int(xy[0] // CELL), int(xy[1] // CELL))
    g = (7, 7)                                           # RO-034's goal cell (the door pose lies on its edge)
    cells, _ = astar(s, g, person)
    pts = [np.array(xy[:2], float)] + [c for c in cells[1:-1]] + [GOAL[:2]]
    keep = [pts[0]]
    for k in range(1, len(pts) - 1):                     # drop points on a straight piece
        a, b, c = keep[-1], pts[k], pts[k + 1]
        if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 1e-9:
            keep.append(b)
    keep.append(pts[-1])
    return make_plan(np.array(keep))


def path_length(P):
    return float(np.sum(np.hypot(*np.diff(P[:, :2], axis=0).T))) if len(P) > 1 else 0.0


def first_after_integrated_distance(P, i0, dist):
    """Index of the first pose after the plan from pose i0 has run `dist` m (len(P) if never)."""
    acc = 0.0
    for i in range(i0 + 1, len(P)):
        acc += math.hypot(P[i, 0] - P[i - 1, 0], P[i, 1] - P[i - 1, 1])
        if acc > dist:
            return i
    return len(P)


# ---------------------------------------------------------------- the local costmap
class Costmap:
    """Rolling-window costmap around the robot: LETHAL inside an obstacle, INSCRIBED within the robot's radius of
    one, then 252 exp(-3 (d - 0.25)) out to the inflation radius (nav2_costmap_2d InflationLayer::computeCost),
    0 beyond. The cost of a cell is computed from the exact distance d from its centre to the nearest obstacle."""

    def __init__(self, center, person=None, p=PARAMS):
        self.res = p["resolution"]
        self.n = int(round(p["costmap_size"] / self.res))
        self.ox = math.floor((center[0] - p["costmap_size"] / 2) / self.res) * self.res
        self.oy = math.floor((center[1] - p["costmap_size"] / 2) / self.res) * self.res
        cx = self.ox + (np.arange(self.n) + 0.5) * self.res
        cy = self.oy + (np.arange(self.n) + 0.5) * self.res
        X, Y = np.meshgrid(cx, cy)                          # cost[j, i]: row j is y, column i is x
        d = obstacle_dist(X, Y, person)
        self.dist = d
        r_in = p["robot_radius"]
        c = np.where(d <= 0, LETHAL, np.where(d <= r_in, INSCRIBED, 0))
        mid = (d > r_in) & (d <= p["inflation_radius"])
        c = np.where(mid, (252 * np.exp(-p["cost_scaling_factor"] * (d - r_in))).astype(int), c)
        self.cost = c.astype(np.int16)

    def world_to_map(self, x, y):
        """Cell indices (i, j) and whether each point lies on the map."""
        i = np.floor((np.asarray(x) - self.ox) / self.res).astype(int)
        j = np.floor((np.asarray(y) - self.oy) / self.res).astype(int)
        ok = (i >= 0) & (i < self.n) & (j >= 0) & (j < self.n) & (np.asarray(x) >= self.ox) & \
             (np.asarray(y) >= self.oy)
        return i, j, ok


def inflation_cost(d, p=PARAMS):
    """The cost a cell gets at distance d (m) from the nearest obstacle (for the Note's worked numbers)."""
    if d <= 0:
        return LETHAL
    if d <= p["robot_radius"]:
        return INSCRIBED
    if d > p["inflation_radius"]:
        return 0
    return int(252 * math.exp(-p["cost_scaling_factor"] * (d - p["robot_radius"])))


# ---------------------------------------------------------------- the map-grid critics' distance grids
def adjust_plan_resolution(P, res):
    """nav_2d_utils::adjustPlanResolution: fill gaps longer than two cells with evenly spaced poses."""
    out = [P[0]]
    last = P[0]
    for q in P[1:]:
        sq = (q[0] - last[0]) ** 2 + (q[1] - last[1]) ** 2
        if sq > 4 * res * res:
            steps = int((math.sqrt(sq) - 2 * res) / res) - 1
            for j in range(1, steps):
                out.append(last + (q - last) * j / steps)
        out.append(q)
        last = q
    return np.array(out)


def manhattan_grid(cm, sources):
    """costmap_queue + MapGridCritic::propagateManhattanDistances: from the source cells, spread over the whole
    grid through 4 neighbours, in order of distance (ties: last in, first out); a cell keeps the Manhattan
    distance, in cells, to the source of the neighbour that reached it first."""
    n = cm.n
    val = np.full((n, n), n * n + 1.0)                  # unreachable_score
    seen = np.zeros((n, n), bool)
    bins = {}
    for (i, j) in sources:
        if not seen[j, i]:
            seen[j, i] = True
            val[j, i] = 0.0
            bins.setdefault(0, []).append((i, j, i, j))
    d = 0
    while bins:
        if d not in bins or not bins[d]:
            bins.pop(d, None)
            d = min(bins) if bins else 0
            continue
        i, j, si, sj = bins[d].pop()
        val[j, i] = abs(si - i) + abs(sj - j)
        for a, b in ((i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)):
            if 0 <= a < n and 0 <= b < n and not seen[b, a]:
                seen[b, a] = True
                dd = abs(si - a) + abs(sj - b)
                bins.setdefault(dd, []).append((a, b, si, sj))
                d = min(d, dd)
    return val


def plan_cells(cm, P):
    """The cells of the plan's poses on the costmap, in order, until the plan leaves it (PathDistCritic::prepare)."""
    A = adjust_plan_resolution(P, cm.res)
    cells, started = [], False
    for x, y in A[:, :2]:
        i, j, ok = cm.world_to_map(x, y)
        if ok and cm.cost[j, i] != NO_INFO:
            cells.append((int(i), int(j)))
            started = True
        elif started:
            break
    return cells


# ---------------------------------------------------------------- the velocity samples: the dynamic window
def project_velocity(v0, acc, decel, dt, target):
    """one_d_velocity_iterator.hpp projectVelocity: move from v0 towards target at the limits for dt seconds."""
    if v0 < target:
        return min(target, v0 + acc * dt)
    return max(target, v0 + decel * dt)


def samples_1d(current, vmin, vmax, acc, decel, dt, n):
    """OneDVelocityIterator: n evenly spaced values from the lowest to the highest velocity reachable from the
    current one in dt seconds, within [vmin, vmax]; 0 is added when the range crosses it."""
    current = min(max(current, vmin), vmax)
    hi = project_velocity(current, acc, decel, dt, vmax)
    lo = project_velocity(current, acc, decel, dt, vmin)
    if abs(lo - hi) < EPS:
        return [lo], (lo, hi)
    n = max(2, n)
    inc = (hi - lo) / (n - 1)
    out, cur, ret_zero = [], lo, True
    while cur <= hi + EPS:
        out.append(cur)
        if ret_zero and cur < 0 and cur + inc > 0 and cur + inc <= hi + EPS:
            out.append(0.0)
            ret_zero = False
        cur += inc
    return out, (lo, hi)


def wheel_ok(v, w):
    """Our robot's limit: each wheel at most 0.6 m/s (RO-001: wheel speeds v -/+ w L / 2)."""
    return abs(v) + abs(w) * L_AXLE / 2 <= V_WHEEL + 1e-9


def window(v0, w0, dt, p=PARAMS):
    """XYThetaIterator: every (v, w) pair from the two 1-D sample lists that isValidSpeed keeps (not both 0, speed
    at most max_speed_xy) and, for our robot, both wheels within 0.6 m/s. Returns the pairs and the window."""
    vs, vwin = samples_1d(v0, p["min_vel_x"], p["max_vel_x"], p["acc_lim_x"], p["decel_lim_x"], dt, p["vx_samples"])
    ws, wwin = samples_1d(w0, -p["max_vel_theta"], p["max_vel_theta"], p["acc_lim_theta"], p["decel_lim_theta"],
                          dt, p["vtheta_samples"])
    pairs = [(v, w) for v in vs for w in ws
             if not (v == 0.0 and w == 0.0) and v * v <= p["max_speed_xy"] ** 2 + 1e-7 and wheel_ok(v, w)]
    return pairs, vwin, wwin, vs, ws


# ---------------------------------------------------------------- the rollouts
def time_steps(v, w, p=PARAMS):
    """StandardTrajectoryGenerator::getTimeSteps: split sim_time so that the robot moves at most
    linear_granularity m or turns at most angular_granularity rad per step, at the sampled velocity."""
    if p["discretize_by_time"]:
        n = math.ceil(p["sim_time"] / p["time_granularity"])
    else:
        n = math.ceil(max(abs(v) * p["sim_time"] / p["linear_granularity"],
                          abs(w) * p["sim_time"] / p["angular_granularity"]))
    n = max(n, 1)
    return n, p["sim_time"] / n


def rollout(pose, vel, cmd, p=PARAMS):
    """generateTrajectory: from the robot's pose and measured velocity, each step first moves the velocity towards
    the sampled one at the acceleration limits (StandardTrajectoryGenerator; the LimitedAccelGenerator holds the
    sampled velocity from the start), then moves the pose with it. Returns the poses, (n + 1, 3)."""
    n, dt = time_steps(*cmd, p)
    k = np.arange(1, n + 1)

    def ramp(v0, acc, decel, target):                    # project_velocity applied k times, in one go
        if v0 < target:
            return np.minimum(target, v0 + acc * dt * k)
        return np.maximum(target, v0 + decel * dt * k)

    if p["trajectory_generator"] == "standard":
        vv = ramp(vel[0], p["acc_lim_x"], p["decel_lim_x"], cmd[0])
        ww = ramp(vel[1], p["acc_lim_theta"], p["decel_lim_theta"], cmd[1])
    else:
        vv, ww = np.full(n, float(cmd[0])), np.full(n, float(cmd[1]))
    th = np.empty(n + 1)
    th[0] = pose[2]
    th[1:] = pose[2] + np.cumsum(ww * dt)
    x = np.empty(n + 1)
    y = np.empty(n + 1)
    x[0], y[0] = pose[0], pose[1]
    x[1:] = pose[0] + np.cumsum(vv * np.cos(th[:-1]) * dt)
    y[1:] = pose[1] + np.cumsum(vv * np.sin(th[:-1]) * dt)
    return np.column_stack([x, y, th])


# ---------------------------------------------------------------- the critics
class Critics:
    """The seven critics of the example configuration, with their state between cycles (RotateToGoal's latches,
    Oscillation's sign flags). Each returns a raw score or None for an illegal trajectory, with the reason."""

    def __init__(self, p=PARAMS):
        self.p = p
        self.in_window = self.rotating = False
        self.trend = {"x": [0, False, False], "theta": [0, False, False]}   # sign, positive_only, negative_only
        self.prev_stationary = None

    # -- called once per cycle, before scoring (TrajectoryCritic::prepare)
    def prepare(self, cm, pose, vel, goal, plan):
        p = self.p
        res = cm.res
        self.cm, self.pose, self.goal, self.plan = cm, pose, goal, plan
        # PathDist and PathAlign: distance from the plan's cells
        cells = plan_cells(cm, plan)
        self.path_grid = manhattan_grid(cm, cells)
        # GoalDist: distance from the last plan pose on the costmap
        self.goal_cell = cells[-1]
        self.goal_grid = manhattan_grid(cm, [cells[-1]])
        # GoalAlign: the same, with the plan's last pose pushed forward_point_distance further along the direction
        # from the robot to the goal (the nose is drawn to where it will be)
        ang = math.atan2(goal[1] - pose[1], goal[0] - pose[0])
        shifted = plan.copy()
        shifted[-1, 0] += p["forward_point_distance"] * math.cos(ang)
        shifted[-1, 1] += p["forward_point_distance"] * math.sin(ang)
        ga = plan_cells(cm, shifted)
        self.goal_align_cell = ga[-1]
        self.goal_align_grid = manhattan_grid(cm, [ga[-1]])
        # PathAlign switches itself off within forward_point_distance of the goal
        self.path_align_on = math.hypot(pose[0] - goal[0], pose[1] - goal[1]) > p["forward_point_distance"]
        # RotateToGoal's latches
        dxy2 = (pose[0] - goal[0]) ** 2 + (pose[1] - goal[1]) ** 2
        self.in_window = self.in_window or (dxy2 <= p["xy_goal_tolerance"] ** 2 and
                                            path_length(plan) <= p["path_length_tolerance"])
        self.cur_speed2 = vel[0] ** 2
        self.rotating = self.rotating or (self.in_window and self.cur_speed2 <= p["trans_stopped_velocity"] ** 2)
        self.map_scale = res * 0.5                       # MapGridCritic::getScale = resolution * 0.5 * scale

    def scale(self, name):
        s = self.p["scales"][name]
        if name in ("GoalAlign", "PathAlign", "PathDist", "GoalDist"):
            s *= self.map_scale
        if name == "PathAlign" and not self.path_align_on:
            s = 0.0
        return s

    def _grid_at(self, grid, x, y):
        i, j, ok = self.cm.world_to_map(x, y)
        if not np.all(ok):
            return None
        return grid[j, i]

    def score(self, name, traj, cmd):
        """Raw score of one trajectory, or (None, reason) when the critic rejects it."""
        p = self.p
        last = traj[-1]
        if name == "BaseObstacle":
            i, j, ok = self.cm.world_to_map(traj[:, 0], traj[:, 1])
            if not np.all(ok):
                return None, "goes off the costmap"
            c = self.cm.cost[j, i]
            if np.any((c == LETHAL) | (c == INSCRIBED) | (c == NO_INFO)):
                return None, "hits an obstacle"
            return float(c[-1]), ""
        if name in ("PathDist", "GoalDist"):
            grid = self.path_grid if name == "PathDist" else self.goal_grid
            v = self._grid_at(grid, traj[:, 0], traj[:, 1])
            if v is None:
                return None, "goes off the costmap"
            return float(v[-1]), ""
        if name in ("PathAlign", "GoalAlign"):
            grid = self.path_grid if name == "PathAlign" else self.goal_align_grid
            fx = last[0] + p["forward_point_distance"] * math.cos(last[2])
            fy = last[1] + p["forward_point_distance"] * math.sin(last[2])
            v = self._grid_at(grid, fx, fy)
            if v is None:
                return None, "goes off the costmap"
            return float(v), ""
        if name == "RotateToGoal":
            if not self.in_window:
                return 0.0, ""
            yaw_err = abs(wrap(self.goal[2] - last[2]))
            if not self.rotating:
                if cmd[0] ** 2 >= self.cur_speed2:
                    return None, "not slowing down near the goal"
                return cmd[0] ** 2 * p["slowing_factor"] + yaw_err, ""
            if abs(cmd[0]) > 0:
                return None, "drives instead of turning near the goal"
            return yaw_err, ""
        if name == "Oscillation":
            for key, val in (("x", cmd[0]), ("theta", cmd[1])):
                _, pos_only, neg_only = self.trend[key]
                if (pos_only and val < 0) or (neg_only and val > 0):
                    return None, "oscillates"
            return 0.0, ""
        if name == "PreferForward":
            if cmd[0] < 0:
                return 1.0, ""
            if cmd[0] < 0.1 and abs(cmd[1]) < 0.2:
                return 1.0, ""
            return abs(cmd[1]) * 10.0, ""
        if name == "Twirling":
            return abs(cmd[1]), ""
        raise KeyError(name)

    # -- called once per cycle, after the choice (TrajectoryCritic::debrief): Oscillation's flags
    def debrief(self, cmd):
        p = self.p

        def update(key, val):
            t = self.trend[key]
            flag = False
            if val < 0:
                if t[0] == 1:
                    t[2] = True
                    flag = True
                t[0] = -1
            elif val > 0:
                if t[0] == -1:
                    t[1] = True
                    flag = True
                t[0] = 1
            return flag

        flag = update("x", cmd[0])
        if abs(cmd[0]) <= p["x_only_threshold"]:
            flag |= update("theta", cmd[1])
        if flag:
            self.prev_stationary = self.pose.copy()
        if any(self.trend[k][1] or self.trend[k][2] for k in self.trend) and self.prev_stationary is not None:
            q = self.prev_stationary
            if math.hypot(self.pose[0] - q[0], self.pose[1] - q[1]) > p["oscillation_reset_dist"] or \
                    abs(wrap(self.pose[2] - q[2])) > p["oscillation_reset_angle"]:
                self.trend = {"x": [0, False, False], "theta": [0, False, False]}


# ---------------------------------------------------------------- one controller cycle
def compute_velocity(crit, cm, pose, vel, goal, plan, p=PARAMS, keep=False):
    """DWBLocalPlanner::computeVelocityCommands: prepare the critics, sample the window, roll out and score every
    pair, keep the lowest total. Returns the command and a record (all rollouts and scores when keep)."""
    crit.prepare(cm, pose, vel, goal, plan)
    dt_win = p["sim_time"] if p["trajectory_generator"] == "standard" else 1.0 / p["controller_frequency"]
    pairs, vwin, wwin, vs, ws = window(vel[0], vel[1], dt_win, p)
    best, best_total = None, -1.0
    rec = dict(pairs=pairs, vwin=vwin, wwin=wwin, vs=vs, ws=ws, n_legal=0)
    if keep:
        rec.update(trajs=[], totals=[], raw=[], reasons=[])
    for cmd in pairs:
        traj = rollout(pose, vel, cmd, p)
        total, raws, reason = 0.0, {}, ""
        for name in p["critics"]:
            s = crit.scale(name)
            if s == 0.0 and name != "Oscillation":
                raws[name] = 0.0
                continue
            r, why = crit.score(name, traj, cmd)
            if r is None:
                total, reason = None, f"{name}: {why}"
                break
            raws[name] = r
            total += r * s
        if keep:
            rec["trajs"].append(traj)
            rec["totals"].append(total)
            rec["raw"].append(raws)
            rec["reasons"].append(reason)
        if total is None:
            continue
        rec["n_legal"] += 1
        if best_total < 0 or total < best_total:
            best, best_total, best_traj, best_raw = cmd, total, traj, raws
    if best is None:
        crit.debrief((0.0, 0.0))
        rec.update(cmd=None, total=None)
        return None, rec
    crit.debrief(best)
    rec.update(cmd=best, total=best_total, traj=best_traj, raw_best=best_raw)
    return best, rec


# ---------------------------------------------------------------- the whole drive
def run(person=PERSON, t_person=T_PERSON, p=PARAMS, t_end=30.0, keep_times=(), replan_hz=None):
    """The controller server's loop at controller_frequency: update the costmap (at update_frequency), prune and
    cut the plan, check the goal, call DWB, send the command; the robot follows it within its limits.
    replan_hz: None keeps the first global plan (as RO-058 did); 1.0 remakes it once a second from where the robot
    is, with what the sensors have seen (Nav2's default behaviour tree, RateController hz="1.0"); a new plan resets
    the critics and the goal checker (newPathReceived, setPlannerPath).
    Returns dict(cycles=[...], plans=[(t, plan)], arrived, t_arrive, reason)."""
    dt_c = 1.0 / p["controller_frequency"]
    n_sub = 20
    plan = global_plan(START[:2])
    plans = [(0.0, plan.copy())]
    goal = plan[-1].copy()
    crit = Critics(p)
    x = START.copy()
    v = w = 0.0
    cm, t_cm = None, -1.0
    check_xy = True
    last_valid = 0.0
    prog_pose, prog_t = x.copy(), 0.0
    out = []
    t = 0.0
    keep_steps = {int(round(k / dt_c)) for k in keep_times}
    step = 0
    result = dict(arrived=False, t_arrive=None, reason="time out")
    while t < t_end - 1e-9:
        seen = person if (person is not None and t >= t_person - 1e-9) else None
        if replan_hz and step > 0 and step % int(round(p["controller_frequency"] / replan_hz)) == 0:
            plan = global_plan(x[:2], seen)
            plans.append((t, plan.copy()))
            crit.in_window = crit.rotating = False
            crit.trend = {"x": [0, False, False], "theta": [0, False, False]}
            check_xy = True
        if cm is None or t - t_cm >= 1.0 / p["update_frequency"] - 1e-9:
            cm, t_cm = Costmap(x, seen, p), t
        # FeasiblePathHandler: closest plan pose (not the last), prune behind it, keep up to prune_distance ahead
        # and while on the costmap
        upper = first_after_integrated_distance(plan, 0, cm.n * cm.res / 2)
        dists = np.hypot(plan[:upper, 0] - x[0], plan[:upper, 1] - x[1])
        k0 = int(np.argmin(dists))
        if len(plan) > 1 and k0 == len(plan) - 1:
            k0 -= 1
        k1 = first_after_integrated_distance(plan, k0, p["prune_distance"])
        local = []
        for q in plan[k0:k1]:
            if not np.all(cm.world_to_map(q[0], q[1])[2]):
                break
            local.append(q)
        local = np.array(local)
        plan = plan[k0:]
        # SimpleGoalChecker (stateful): xy within 0.25 m once, then the heading within 0.25 rad
        reached = False
        if path_length(local) <= p["path_length_tolerance"]:
            if check_xy:
                if math.hypot(x[0] - goal[0], x[1] - goal[1]) <= p["xy_goal_tolerance"]:
                    check_xy = False
            if not check_xy and abs(wrap(goal[2] - x[2])) <= p["yaw_goal_tolerance"]:
                reached = True
        if reached:
            result.update(arrived=True, t_arrive=t, reason="goal reached")
            out.append(dict(t=t, x=x.copy(), v=v, w=w, person=seen, local=local, cmd=(0.0, 0.0), rec=None))
            break
        # SimpleProgressChecker: 0.5 m within 10 s
        if math.hypot(x[0] - prog_pose[0], x[1] - prog_pose[1]) > p["required_movement_radius"]:
            prog_pose, prog_t = x.copy(), t
        elif t - prog_t > p["movement_time_allowance"]:
            result.update(reason="failed to make progress")
            break
        vel = (v if abs(v) >= p["min_x_velocity_threshold"] else 0.0,
               w if abs(w) >= p["min_theta_velocity_threshold"] else 0.0)
        cmd, rec = compute_velocity(crit, cm, x.copy(), vel, goal, local, p, keep=step in keep_steps)
        if cmd is None:                                  # no legal trajectory: stop, abort after failure_tolerance
            cmd = (0.0, 0.0)
            if t - last_valid > p["failure_tolerance"]:
                result.update(reason="controller patience exceeded")
                out.append(dict(t=t, x=x.copy(), v=v, w=w, person=seen, local=local, cmd=None, rec=rec, cm=cm))
                break
        else:
            last_valid = t
        out.append(dict(t=t, x=x.copy(), v=v, w=w, person=seen, local=local, cmd=cmd, rec=rec,
                        cm=cm if step in keep_steps else None, crit_state=(crit.in_window, crit.rotating)))
        # the robot follows the command for one cycle within its limits
        h = dt_c / n_sub
        for _ in range(n_sub):
            v = v + float(np.clip(cmd[0] - v, -A_MAX * h, A_MAX * h))
            w = w + float(np.clip(cmd[1] - w, -p["acc_lim_theta"] * h, p["acc_lim_theta"] * h))
            lim = (V_WHEEL - abs(v)) / (L_AXLE / 2)
            w = float(np.clip(w, -lim, lim))
            x = x + h * np.array([v * math.cos(x[2] + w * h / 2), v * math.sin(x[2] + w * h / 2), w])
        t = round(t + dt_c, 10)
        step += 1
    result["cycles"] = out
    result["plans"] = plans
    return result


def results():
    """Every run the Note quotes (cached by this file's text)."""
    import hashlib
    import pickle
    import tempfile
    from pathlib import Path
    key = hashlib.sha1(Path(__file__).read_bytes()).hexdigest()[:12]
    f = Path(tempfile.gettempdir()) / "ro078_cache" / f"dwb_{key}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    from concurrent.futures import ProcessPoolExecutor
    jobs = dict(replan=dict(replan_hz=1.0, keep_times=(T_PERSON,)),       # the main run: Nav2's 1 Hz replanning
                once=dict(keep_times=(T_PERSON,)),                        # the plan made once, as in RO-058
                free=dict(person=None),                                   # the clear room, plan made once
                free_replan=dict(person=None, replan_hz=1.0),
                spin6=dict(person=None, p=dict(PARAMS, max_vel_theta=2 * V_WHEEL / L_AXLE)),
                dwa=dict(person=None, p=dict(PARAMS, trajectory_generator="limited"), t_end=12.0,
                         keep_times=(0.0,)))
    with ProcessPoolExecutor(len(jobs)) as ex:
        futs = {k: ex.submit(run, **v) for k, v in jobs.items()}
        R = {k: fu.result() for k, fu in futs.items()}
    f.parent.mkdir(exist_ok=True)
    f.write_bytes(pickle.dumps(R))
    return R


if __name__ == "__main__":
    # self-check: window, sample counts and one rollout on easy numbers
    pairs, vwin, wwin, vs, ws = window(0.3, 0.0, 1.0 / 20, dict(PARAMS, trajectory_generator="limited"))
    assert abs(vwin[0] - 0.275) < 1e-9 and abs(vwin[1] - 0.325) < 1e-9 and len(vs) == 20
    assert abs(wwin[1] - 0.16) < 1e-9
    tr = rollout(np.array([0.0, 0.0, 0.0]), (0.3, 0.0), (0.3, 0.0), dict(PARAMS, trajectory_generator="limited"))
    assert abs(tr[-1, 0] - 0.3 * 1.7) < 1e-9 and abs(tr[-1, 1]) < 1e-12
    assert inflation_cost(0.25) == INSCRIBED and inflation_cost(0.5) == int(252 * math.exp(-0.75))
    print("dwbkit self-check passed")
