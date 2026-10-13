"""One NavigateToPose goal through Nav2, re-written in Python (no output when imported; run it to check itself).

This is our own Python version of Nav2's servers, written from the navigation2 code on `main` (read 2026-10-12) and
the bring-up parameters in nav2_bringup/params/nav2_params.yaml. It is not Nav2 running. Files followed:
- nav2_bringup/launch/bringup_launch.py, localization_launch.py, navigation_launch.py: the node list and the one
  lifecycle manager; nav2_lifecycle_manager/src/lifecycle_manager.cpp: configure all in order, then activate all;
- nav2_bt_navigator/behavior_trees/navigate_to_pose_w_replanning_and_recovery.xml and nav2_behavior_tree plugins
  (pipeline_sequence, rate_controller, is_goal_nearby_condition, truncate_path_local, validate_path) and
  nav2_planner/is_path_valid_service.hpp: the tree ticked every 10 ms;
- nav2_planner/src/planner_server.cpp, nav2_navfn_planner/src/navfn.cpp and navfn_planner.cpp: NavFn;
- nav2_costmap_2d: static, obstacle and inflation layers (inflation_layer.hpp computeCost);
- nav2_controller/src/controller_server.cpp with DWB: copied from RO-078's dwbkit.py (same code base);
- nav2_velocity_smoother/src/velocity_smoother.cpp (applyConstraints, open loop);
- nav2_collision_monitor/src/polygon.cpp (getCollisionTime), collision_monitor_node.cpp (processApproach),
  kinematics.cpp (projectState);
- nav2_amcl: likelihood_field_model.cpp, differential_motion_model.cpp, pf.c (KLD limit), amcl_node.cpp.

Simplifications (all listed in the Note):
- one process, a fixed order inside each 0.05 s cycle (laser, AMCL, costmaps, tree, controller, smoother,
  monitor, base); planning and every service answer within the cycle; no message delays;
- the laser is 2D (the local costmap's voxel layer becomes a 2D obstacle layer), ray-cast on the exact room;
- NavFn's potential is spread with a heap (exact order) instead of NavFn's threshold buckets, and to the whole map;
- AMCL's estimate is the weighted mean of all particles (Nav2 takes the mean of the heaviest cluster);
- costmap layers that the bring-up lists but our run never uses (keep-out and speed filters) are left out.

Our robot replaces the TurtleBot of the bring-up file: a disk of radius 0.25 m (robot_radius 0.22 in the file),
each wheel at most 0.6 m/s, forward acceleration at most 0.5 m/s^2 (the smoother's 3.0 in the file). Its left wheel
is 1 percent smaller than the odometry assumes, so odometry drifts and AMCL has something to correct."""
import heapq
import math

import numpy as np
from scipy import ndimage

import dwbkit as D

RES = 0.05
LETHAL, INSCRIBED, NO_INFO, FREE = 254, 253, 255, 0
START, GOAL = D.START.copy(), D.GOAL.copy()

# ---------------------------------------------------------------- parameters (Nav2 name: value)
P = dict(
    # amcl (bring-up)
    alpha=(0.005, 0.005, 0.005, 0.005),  # ours: reliable odometry (ROS Navigation Tuning Guide 5.2); bring-up 0.2
    laser_likelihood_max_dist=2.0, laser_max_range=100.0, max_beams=60,
    max_particles=2000, min_particles=500, pf_err=0.05, pf_z=0.99, sigma_hit=0.2, z_hit=0.5, z_rand=0.5,
    update_min_a=0.2, update_min_d=0.25, resample_interval=1,
    set_initial_pose=True,               # initial pose given as AMCL parameters (the start pose): zero covariance
    init_cov=(0.5 ** 2, 0.5 ** 2, (math.pi / 12) ** 2),          # AMCL's covariance when the pose is not known
    # costmaps (bring-up); robot_radius is ours
    robot_radius=D.R_BODY, inflation_radius=0.70, cost_scaling_factor=3.0,
    global_update_frequency=1.0, local_update_frequency=5.0, local_size=3.0,
    obstacle_max_range=2.5, raytrace_max_range=3.0,
    # bt_navigator and the default tree
    bt_loop_duration=0.010, replan_hz=1.0, proximity_threshold=4.0, max_robot_pose_search_dist=1.5,
    # planner_server: GridBased = NavFn
    tolerance=0.5, use_astar=False, allow_unknown=True,
    # velocity_smoother (bring-up names; values ours where marked)
    smoothing_frequency=20.0, max_velocity=(D.V_WHEEL, 2.0), max_accel=(D.A_MAX, 3.2), max_decel=(-D.A_MAX, -3.2),
    # collision_monitor (bring-up): FootprintApproach
    time_before_collision=1.2, simulation_time_step=0.1, min_points=6,
    # laser (nav2_loopback_sim's scan in the bring-up file): 241 beams, 0.02617 rad apart, up to 30 m
    scan_angle_min=-3.1415, scan_angle_increment=0.02617, scan_n=241, scan_range_max=30.0, scan_range_min=0.05,
    scan_rate=10.0, scan_noise=0.01,                               # ours: 10 scans a second, 1 cm noise
    left_wheel_scale=0.99,                                         # ours: true left wheel radius / assumed
)
DWB = dict(D.PARAMS)                  # RO-078's DWB parameters (configuration-guide example, our robot's limits)
DT = 0.01                             # simulation step = bt_loop_duration
CYCLE = 0.05                          # controller_frequency 20 Hz and smoothing_frequency 20 Hz

# bringup_launch.py: the localisation nodes, the keep-out and speed zone filter servers (use_keepout_zones and
# use_speed_zones default True), then the navigation nodes of navigation_launch.py: 17 managed nodes
NODES = ["map_server", "amcl", "keepout_filter_mask_server", "keepout_costmap_filter_info_server",
         "speed_filter_mask_server", "speed_costmap_filter_info_server", "controller_server", "smoother_server",
         "planner_server", "route_server", "behavior_server", "velocity_smoother", "collision_monitor",
         "bt_navigator", "waypoint_follower", "docking_server", "following_server"]


def lifecycle_bringup():
    """lifecycle_manager.cpp startup(): configure every node in order, then activate every node in order.
    Returns the list of (node, transition, new state)."""
    out = [(n, "configure", "inactive") for n in NODES]
    out += [(n, "activate", "active") for n in NODES]
    return out


# ---------------------------------------------------------------- the map (map_server) and the laser
MARGIN = 0.5                          # the map reaches 0.5 m beyond the walls, as a map made by driving round would
OX = OY = -MARGIN                     # map origin (m)


def build_map():
    """The occupancy grid map_server serves: 0.05 m cells from (-0.5, -0.5) to (7.5, 4.5) m; a cell is occupied
    when its centre lies within half a cell of an obstacle or a wall (walls two cells thick), unknown outside the
    room, free inside. Returns (occ, unknown), both [j, i] with row j along y."""
    nx, ny = int(round((D.W_ROOM + 2 * MARGIN) / RES)), int(round((D.H_ROOM + 2 * MARGIN) / RES))
    X, Y = np.meshgrid(OX + (np.arange(nx) + 0.5) * RES, OY + (np.arange(ny) + 0.5) * RES)
    occ = D.obstacle_dist(X, Y) <= RES / 2
    outside = (X < 0) | (X > D.W_ROOM) | (Y < 0) | (Y > D.H_ROOM)
    return occ, outside & ~occ


def _segments():
    segs = list(D.WALLS)
    segs += [(tuple(D.TABLE[i]), tuple(D.TABLE[(i + 1) % 4])) for i in range(4)]
    for x0, x1, y0, y1 in D.CAB:
        c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        segs += [(c[i], c[(i + 1) % 4]) for i in range(4)]
    return np.array(segs, float)                      # (S, 2, 2)


SEGS = _segments()
ANGLES = P["scan_angle_min"] + np.arange(P["scan_n"]) * P["scan_angle_increment"]


def scan(pose, person=None, rng=None):
    """Ranges of the 241 beams from the true pose (bearing from the heading); inf where nothing is within 30 m."""
    th = pose[2] + ANGLES
    dx, dy = np.cos(th)[:, None], np.sin(th)[:, None]
    ax, ay = SEGS[None, :, 0, 0], SEGS[None, :, 0, 1]
    ex, ey = SEGS[None, :, 1, 0] - ax, SEGS[None, :, 1, 1] - ay
    den = dx * ey - dy * ex
    with np.errstate(divide="ignore", invalid="ignore"):
        t = ((ax - pose[0]) * ey - (ay - pose[1]) * ex) / den
        s = ((ax - pose[0]) * dy - (ay - pose[1]) * dx) / den
    t = np.where((np.abs(den) > 1e-12) & (t > 1e-9) & (s >= 0) & (s <= 1), t, np.inf)
    r = t.min(axis=1)
    circles = [(c, D.POLE_R) for c in D.POLES] + ([(person, D.PERSON_R)] if person is not None else [])
    for c, rad in circles:
        fx, fy = pose[0] - c[0], pose[1] - c[1]
        b = fx * dx[:, 0] + fy * dy[:, 0]
        disc = b * b - (fx * fx + fy * fy - rad * rad)
        hit = np.where(disc >= 0, -b - np.sqrt(np.maximum(disc, 0)), np.inf)
        r = np.minimum(r, np.where(hit > 0, hit, np.inf))
    if rng is not None and P["scan_noise"]:
        r = r + rng.normal(0, P["scan_noise"], r.shape)
    r = np.where(r > P["scan_range_max"], np.inf, r)
    return r


def scan_points(pose, ranges):
    """World coordinates of the finite returns, seen from `pose`."""
    ok = np.isfinite(ranges)
    a = pose[2] + ANGLES[ok]
    return np.column_stack([pose[0] + ranges[ok] * np.cos(a), pose[1] + ranges[ok] * np.sin(a)])


# ---------------------------------------------------------------- frames
def compose(a, b):
    """Pose b given in frame a, expressed in a's parent frame."""
    c, s = math.cos(a[2]), math.sin(a[2])
    return np.array([a[0] + c * b[0] - s * b[1], a[1] + s * b[0] + c * b[1], D.wrap(a[2] + b[2])])


def inverse(a):
    c, s = math.cos(a[2]), math.sin(a[2])
    return np.array([-c * a[0] - s * a[1], s * a[0] - c * a[1], -a[2]])


# ---------------------------------------------------------------- AMCL
class AMCL:
    """nav2_amcl with the bring-up parameters: odometry motion model (DifferentialMotionModel), likelihood field
    model (p = 1 + sum of pz cubed over 60 beams), KLD-limited resampling (pf.c pf_resample_limit with bins of
    0.5 m x 0.5 m x 10 degrees), a filter update only after 0.25 m or 0.2 rad of odometry (or on the first scan)."""

    def __init__(self, occ, init_pose, rng):
        self.rng = rng
        free = ~occ
        self.dist = np.minimum(ndimage.distance_transform_edt(free) * RES, P["laser_likelihood_max_dist"])
        n = P["max_particles"]
        cov = np.zeros(3) if P["set_initial_pose"] else np.sqrt(P["init_cov"])
        self.x = np.column_stack([init_pose[0] + rng.normal(0, cov[0], n), init_pose[1] + rng.normal(0, cov[1], n),
                                  D.wrap(init_pose[2] + rng.normal(0, cov[2], n))])
        self.w = np.full(n, 1.0 / n)
        self.last_odom = None
        self.updates = []
        self.est = np.array(init_pose, float)

    def motion(self, old, new):
        """DifferentialMotionModel::odometryUpdate, applied to every particle."""
        a1, a2, a3, a4 = P["alpha"]
        dx, dy = new[0] - old[0], new[1] - old[1]
        trans = math.hypot(dx, dy)
        rot1 = 0.0 if trans < 0.01 else D.wrap(math.atan2(dy, dx) - old[2])
        rot2 = D.wrap(D.wrap(new[2] - old[2]) - rot1)
        n1 = min(abs(D.wrap(rot1)), abs(D.wrap(rot1 - math.pi)))
        n2 = min(abs(D.wrap(rot2)), abs(D.wrap(rot2 - math.pi)))
        m = len(self.x)
        r1 = rot1 - self.rng.normal(0, math.sqrt(a1 * n1 ** 2 + a2 * trans ** 2), m)
        tr = trans - self.rng.normal(0, math.sqrt(a3 * trans ** 2 + a4 * n1 ** 2 + a4 * n2 ** 2), m)
        r2 = rot2 - self.rng.normal(0, math.sqrt(a1 * n2 ** 2 + a2 * trans ** 2), m)
        self.x[:, 0] += tr * np.cos(self.x[:, 2] + r1)
        self.x[:, 1] += tr * np.sin(self.x[:, 2] + r1)
        self.x[:, 2] = D.wrap(self.x[:, 2] + r1 + r2)

    def sensor(self, ranges):
        """LikelihoodFieldModel::sensorFunction: every max_beams-th beam (step 4: 61 beams) that returned."""
        rmax = min(P["scan_range_max"], P["laser_max_range"])
        step = max(1, (P["scan_n"] - 1) // (P["max_beams"] - 1))
        idx = np.arange(0, P["scan_n"], step)
        idx = idx[np.isfinite(ranges[idx]) & (ranges[idx] < rmax)]
        hx = self.x[:, 0:1] + ranges[idx][None, :] * np.cos(self.x[:, 2:3] + ANGLES[idx][None, :])
        hy = self.x[:, 1:2] + ranges[idx][None, :] * np.sin(self.x[:, 2:3] + ANGLES[idx][None, :])
        mi, mj = np.floor((hx - OX) / RES).astype(int), np.floor((hy - OY) / RES).astype(int)
        ny, nx = self.dist.shape
        ok = (mi >= 0) & (mi < nx) & (mj >= 0) & (mj < ny)
        z = np.where(ok, self.dist[np.clip(mj, 0, ny - 1), np.clip(mi, 0, nx - 1)], P["laser_likelihood_max_dist"])
        pz = P["z_hit"] * np.exp(-z * z / (2 * P["sigma_hit"] ** 2)) + P["z_rand"] / rmax
        p = 1.0 + np.sum(pz ** 3, axis=1)
        self.w = self.w * p
        self.w /= self.w.sum()

    def kld_limit(self, k):
        """pf_resample_limit: particles needed for k occupied bins (pop_err = pf_err, pop_z = pf_z as in the code)."""
        if k <= 1:
            return P["max_particles"]
        b = 2 / (9 * (k - 1))
        x = 1 - b + math.sqrt(b) * P["pf_z"]
        n = math.ceil((k - 1) / (2 * P["pf_err"]) * x ** 3)
        return int(min(max(n, P["min_particles"]), P["max_particles"]))

    def resample(self):
        """pf_update_resample: draw particles by weight one at a time until there are more than the KLD limit for
        the bins they fill."""
        c = np.cumsum(self.w)
        draws = self.rng.random(P["max_particles"])
        picks = np.minimum(np.searchsorted(c, draws * c[-1]), len(c) - 1)
        bins, out = set(), []
        for i in picks:
            q = self.x[i]
            bins.add((math.floor(q[0] / 0.5), math.floor(q[1] / 0.5), math.floor(q[2] / math.radians(10))))
            out.append(i)
            if len(out) > self.kld_limit(len(bins)):
                break
        self.x = self.x[out].copy()
        self.w = np.full(len(out), 1.0 / len(out))
        return len(bins)

    def scan_received(self, t, odom_pose, ranges):
        """laserReceived: update the filter if odometry moved enough since the last update (always the first time).
        Returns True when the filter was updated."""
        if self.last_odom is not None:
            d = odom_pose - self.last_odom
            d[2] = D.wrap(d[2])
            # amcl_node: the per-axis test on the odometry change
            if not (abs(d[0]) > P["update_min_d"] or abs(d[1]) > P["update_min_d"] or abs(d[2]) > P["update_min_a"]):
                return False
            self.motion(self.last_odom, odom_pose)
        self.last_odom = odom_pose.copy()
        self.sensor(ranges)
        w = self.w
        self.est = np.array([np.sum(w * self.x[:, 0]), np.sum(w * self.x[:, 1]),
                             math.atan2(np.sum(w * np.sin(self.x[:, 2])), np.sum(w * np.cos(self.x[:, 2])))])
        n_before = len(self.x)
        k = self.resample()
        self.updates.append(dict(t=t, est=self.est.copy(), n=n_before, n_after=len(self.x), bins=k,
                                 particles=self.x[self.rng.choice(len(self.x), min(400, len(self.x)), False)].copy(),
                                 odom=odom_pose.copy()))
        return True

    def map_to_odom(self):
        """The map -> odom transform AMCL publishes: its estimate composed with the inverse of the odometry pose."""
        return compose(self.est, inverse(self.last_odom))


# ---------------------------------------------------------------- costmaps
def inflation(lethal, p=P):
    """InflationLayer: distance from every cell to the nearest lethal cell (between cell centres), then
    computeCost: 254 on the obstacle, 253 within the robot's radius, 252 exp(-3 (d - 0.25)) out to 0.70 m."""
    dc = ndimage.distance_transform_edt(~lethal)                   # distance in cells, between cell centres
    d = dc * RES
    r_in = p["robot_radius"]
    reach = math.ceil(p["inflation_radius"] / RES)                 # cellDistance(inflation_radius): 14 cells
    c = np.where(dc == 0, LETHAL, np.where(d <= r_in, INSCRIBED, 0))
    mid = (d > r_in) & (dc <= reach)
    c = np.where(mid, (252 * np.exp(-p["cost_scaling_factor"] * (d - r_in))).astype(int), c)
    return c.astype(np.int16)


class Costmap:
    """A layered costmap. kind 'global': map frame, the whole room, static + obstacle + inflation layers, updated at
    1 Hz. kind 'local': odom frame, a rolling 3 m x 3 m window, obstacle (the voxel layer, in 2D) + inflation,
    updated at 5 Hz. The obstacle layer keeps marked cells until a later beam passes through them."""

    def __init__(self, kind, static=None, unknown=None):
        self.kind, self.static, self.unknown, self.res = kind, static, unknown, RES
        self.marks = set()
        self.n = int(round(P["local_size"] / RES)) if kind == "local" else None
        self.ox, self.oy = (OX, OY) if kind == "global" else (0.0, 0.0)
        self.cost = None

    def _keys(self, pts):
        return set(zip(np.floor(pts[:, 0] / RES).astype(int).tolist(), np.floor(pts[:, 1] / RES).astype(int).tolist()))

    def update(self, sensor_pose, ranges, robot_pose):
        """ObstacleLayer::updateBounds: clear along each beam (up to 3.0 m, endpoint excluded), then mark endpoints
        nearer than 2.5 m; clear the robot's footprint; then build the master grid and inflate it."""
        fin = np.where(np.isfinite(ranges), ranges, np.inf)
        reach = np.minimum(fin, P["raytrace_max_range"])
        clear = []
        for k in range(len(ANGLES)):
            n = int(reach[k] / (RES / 2))
            if n <= 1:
                continue
            s = (np.arange(n) * (RES / 2))[: -1 if np.isfinite(fin[k]) and fin[k] <= P["raytrace_max_range"] else None]
            a = sensor_pose[2] + ANGLES[k]
            clear.append(np.column_stack([sensor_pose[0] + s * math.cos(a), sensor_pose[1] + s * math.sin(a)]))
        if clear:
            self.marks -= self._keys(np.vstack(clear))
        mark = np.where(fin <= P["obstacle_max_range"], fin, np.inf)
        pts = scan_points(sensor_pose, mark)
        if len(pts):
            self.marks |= self._keys(pts)
        # footprint clearing
        rr = P["robot_radius"]
        self.marks = {k for k in self.marks if math.hypot((k[0] + 0.5) * RES - robot_pose[0],
                                                          (k[1] + 0.5) * RES - robot_pose[1]) > rr}
        if self.kind == "global":
            ny, nx = self.static.shape
            lethal = self.static.copy()
            i0, j0 = int(round(OX / RES)), int(round(OY / RES))
            for i, j in self.marks:
                if 0 <= i - i0 < nx and 0 <= j - j0 < ny:
                    lethal[j - j0, i - i0] = True
        else:
            half = P["local_size"] / 2
            self.ox = math.floor((robot_pose[0] - half) / RES) * RES
            self.oy = math.floor((robot_pose[1] - half) / RES) * RES
            i0, j0 = int(round(self.ox / RES)), int(round(self.oy / RES))
            lethal = np.zeros((self.n, self.n), bool)
            for i, j in self.marks:
                if i0 <= i < i0 + self.n and j0 <= j < j0 + self.n:
                    lethal[j - j0, i - i0] = True
            self.marks = {(i, j) for i, j in self.marks if i0 <= i < i0 + self.n and j0 <= j < j0 + self.n}
        self.lethal = lethal
        self.cost = inflation(lethal)
        if self.kind == "global":                          # unknown cells stay unknown unless inflated to 253+
            self.cost = np.where(self.unknown & ~lethal & (self.cost < INSCRIBED), NO_INFO, self.cost).astype(np.int16)

    def world_to_map(self, x, y):
        """The same interface as RO-078's Costmap, so DWB's critics can read it."""
        i = np.floor((np.asarray(x) - self.ox) / RES).astype(int)
        j = np.floor((np.asarray(y) - self.oy) / RES).astype(int)
        ny, nx = self.cost.shape
        ok = (i >= 0) & (i < nx) & (j >= 0) & (j < ny) & (np.asarray(x) >= self.ox) & (np.asarray(y) >= self.oy)
        return i, j, ok


# ---------------------------------------------------------------- planner_server: NavFn
COST_NEUTRAL, COST_FACTOR, COST_OBS, POT_HIGH = 50, 0.8, 254, 1.0e10


def navfn(cost, start, goal, p=P):
    """NavfnPlanner::makePlan on the global costmap: NavFn's cost array (50 + 0.8 cost, 254 for 253 and above),
    the potential spread from the robot's cell with NavFn's planar-wave update (updateCell), then the path from
    the goal down the potential's gradient in steps of half a cell (calcPath), reversed. Returns (path poses with
    yaw 0 except the last, which takes the goal's heading, number of cells reached)."""
    ny, nx = cost.shape
    c = np.where(cost < 253, np.minimum(COST_NEUTRAL + COST_FACTOR * cost, COST_OBS - 1), COST_OBS).astype(float)
    if p["allow_unknown"]:
        c = np.where(cost == NO_INFO, COST_OBS - 1, c)
    c[0, :] = c[-1, :] = c[:, 0] = c[:, -1] = COST_OBS
    si, sj = int((start[0] - OX) / RES), int((start[1] - OY) / RES)
    c[sj, si] = COST_NEUTRAL                                       # clearRobotCell
    pot = np.full((ny, nx), POT_HIGH)
    pot[sj, si] = 0.0
    heap = [(0.0, sj, si - 1), (0.0, sj, si + 1), (0.0, sj - 1, si), (0.0, sj + 1, si)]
    while heap:
        _, j, i = heapq.heappop(heap)
        if not (0 < i < nx - 1 and 0 < j < ny - 1) or c[j, i] >= COST_OBS:
            continue
        l, r, u, d = pot[j, i - 1], pot[j, i + 1], pot[j - 1, i], pot[j + 1, i]
        tc, ta = min(l, r), min(u, d)
        hf = c[j, i]
        dc = tc - ta
        if dc < 0:
            dc, ta = -dc, tc
        if dc >= hf:
            new = ta + hf
        else:
            q = dc / hf
            new = ta + hf * (-0.2301 * q * q + 0.5307 * q + 0.7040)
        if new < pot[j, i]:
            pot[j, i] = new
            for (jj, ii) in ((j, i - 1), (j, i + 1), (j - 1, i), (j + 1, i)):
                if pot[jj, ii] > new + 0.707106781 * c[jj, ii]:
                    heapq.heappush(heap, (new, jj, ii))
    reached = int(np.sum(pot < POT_HIGH))
    # the goal, or the nearest reachable point within `tolerance` of it
    gi, gj = int((goal[0] - OX) / RES), int((goal[1] - OY) / RES)
    if pot[gj, gi] >= POT_HIGH:
        best = None
        k = int(p["tolerance"] / RES)
        for jj in range(gj - k, gj + k + 1):
            for ii in range(gi - k, gi + k + 1):
                if 0 <= ii < nx and 0 <= jj < ny and pot[jj, ii] < POT_HIGH:
                    dd = (ii - gi) ** 2 + (jj - gj) ** 2
                    if best is None or dd < best[0]:
                        best = (dd, ii, jj)
        if best is None:
            return None, reached
        gi, gj = best[1], best[2]
    # calcPath with gradients (gradCell)
    gx, gy = np.zeros((ny, nx)), np.zeros((ny, nx))
    done = np.zeros((ny, nx), bool)

    def grad(j, i):
        if done[j, i]:
            return
        done[j, i] = True
        cv = pot[j, i]
        dx = dy = 0.0
        if cv >= POT_HIGH:
            if pot[j, i - 1] < POT_HIGH:
                dx = -COST_OBS
            elif pot[j, i + 1] < POT_HIGH:
                dx = COST_OBS
            if pot[j - 1, i] < POT_HIGH:
                dy = -COST_OBS
            elif pot[j + 1, i] < POT_HIGH:
                dy = COST_OBS
        else:
            if pot[j, i - 1] < POT_HIGH:
                dx += pot[j, i - 1] - cv
            if pot[j, i + 1] < POT_HIGH:
                dx += cv - pot[j, i + 1]
            if pot[j - 1, i] < POT_HIGH:
                dy += pot[j - 1, i] - cv
            if pot[j + 1, i] < POT_HIGH:
                dy += cv - pot[j + 1, i]
        nrm = math.hypot(dx, dy)
        if nrm > 0:
            gx[j, i], gy[j, i] = dx / nrm, dy / nrm

    ci, cj, fx, fy = gi, gj, 0.0, 0.0
    px, py = [], []
    for _ in range(max(nx, ny) * 4 * 10):
        ni, nj = ci + int(round(fx)), cj + int(round(fy))
        if pot[min(max(nj, 0), ny - 1), min(max(ni, 0), nx - 1)] < COST_NEUTRAL:
            px.append(si)
            py.append(sj)
            break
        px.append(ci + fx)
        py.append(cj + fy)
        osc = len(px) > 2 and px[-1] == px[-3] and py[-1] == py[-3]
        nb = pot[cj - 1:cj + 2, ci - 1:ci + 2]
        if (nb >= POT_HIGH).any() or osc:
            jj, ii = np.unravel_index(int(np.argmin(nb)), nb.shape)
            ci, cj, fx, fy = ci + ii - 1, cj + jj - 1, 0.0, 0.0
            continue
        for (jj, ii) in ((cj, ci), (cj, ci + 1), (cj + 1, ci), (cj + 1, ci + 1)):
            grad(jj, ii)
        x1 = (1 - fx) * gx[cj, ci] + fx * gx[cj, ci + 1]
        x2 = (1 - fx) * gx[cj + 1, ci] + fx * gx[cj + 1, ci + 1]
        gxx = (1 - fy) * x1 + fy * x2
        y1 = (1 - fx) * gy[cj, ci] + fx * gy[cj, ci + 1]
        y2 = (1 - fx) * gy[cj + 1, ci] + fx * gy[cj + 1, ci + 1]
        gyy = (1 - fy) * y1 + fy * y2
        if gxx == 0 and gyy == 0:
            return None, reached
        ss = 0.5 / math.hypot(gxx, gyy)
        fx += gxx * ss
        fy += gyy * ss
        if fx > 1:
            ci, fx = ci + 1, fx - 1
        if fx < -1:
            ci, fx = ci - 1, fx + 1
        if fy > 1:
            cj, fy = cj + 1, fy - 1
        if fy < -1:
            cj, fy = cj - 1, fy + 1
    pts = np.column_stack([OX + np.array(px[::-1]) * RES, OY + np.array(py[::-1]) * RES])   # mapToWorld: origin + m res
    path = np.column_stack([pts, np.zeros(len(pts))])
    g = np.array(goal, float)
    if len(path) >= 2 and np.sum((path[-1, :2] - path[-2, :2]) ** 2) > np.sum((g[:2] - path[-2, :2]) ** 2):
        path[-1] = g                                               # smoothApproachToGoal
    elif np.sum((path[-1, :2] - g[:2]) ** 2) < 1e-6:
        path[-1] = g
    else:
        path = np.vstack([path, g])
    return path, reached


def path_valid(cost, path, robot):
    """IsPathValidService (robot_radius footprint): from the path pose nearest the robot onwards, invalid at the first
    pose on a cell of cost 253 or more."""
    k0 = int(np.argmin(np.hypot(path[:, 0] - robot[0], path[:, 1] - robot[1])))
    ny, nx = cost.shape
    for k in range(k0, len(path)):
        i, j = int((path[k, 0] - OX) / RES), int((path[k, 1] - OY) / RES)
        cv = cost[j, i] if (0 <= i < nx and 0 <= j < ny) else LETHAL
        if cv == NO_INFO:
            cv = FREE
        if cv >= INSCRIBED:
            return False, k
    return True, None


# ---------------------------------------------------------------- velocity smoother and collision monitor
def smooth(last, cmd, p=P):
    """VelocitySmoother::smootherTimer (open loop): clamp to the speed limits, then change each axis by at most its
    acceleration (or deceleration) limit per 1/20 s (applyConstraints, eta = 1)."""
    out = []
    for k in range(2):
        v = min(max(cmd[k], -p["max_velocity"][k]), p["max_velocity"][k])
        dv = v - last[k]
        if abs(v) >= abs(last[k]) and last[k] * v >= 0:
            lo, hi = -p["max_accel"][k] / p["smoothing_frequency"], p["max_accel"][k] / p["smoothing_frequency"]
        else:
            lo, hi = p["max_decel"][k] / p["smoothing_frequency"], -p["max_decel"][k] / p["smoothing_frequency"]
        out.append(last[k] + min(max(dv, lo), hi))
    return tuple(out)


def _circle_footprint(r):
    """makeFootprintFromRadius: 16 points on a circle of the robot's radius."""
    ang = np.arange(16) * 2 * math.pi / 16
    return np.column_stack([r * np.cos(ang), r * np.sin(ang)])


def box(x0, x1, y0, y1):
    return np.array([(x1, y1), (x1, y0), (x0, y0), (x0, y1)])[::-1]      # counter-clockwise


# collision_monitor polygons, in the order the node checks them. Bring-up: only the approach footprint.
MONITOR_BRINGUP = [dict(name="FootprintApproach", action="approach", poly=_circle_footprint(D.R_BODY),
                        time_before_collision=1.2, simulation_time_step=0.1, min_points=6)]
# nav2_collision_monitor/params/collision_monitor_params.yaml: the package's example zones (all four enabled here)
MONITOR_EXAMPLE = [
    dict(name="PolygonStop", action="stop", poly=box(0.0, 0.3, -0.3, 0.3), min_points=4),
    dict(name="PolygonSlow", action="slowdown", poly=box(-0.4, 0.4, -0.4, 0.4), min_points=4, slowdown_ratio=0.3),
    dict(name="PolygonLimit", action="limit", poly=box(-0.5, 0.5, -0.5, 0.5), min_points=4, linear_limit=0.4,
         angular_limit=0.5),
    dict(name="FootprintApproach", action="approach", poly=_circle_footprint(D.R_BODY), time_before_collision=2.0,
         simulation_time_step=0.1, min_points=6),
]


def points_inside(poly, pts):
    """Polygon::getPointsInside for a convex polygon given counter-clockwise: points on the left of every edge."""
    if len(pts) == 0:
        return 0
    a, b = poly, np.roll(poly, -1, axis=0)
    cr = (b[None, :, 0] - a[None, :, 0]) * (pts[:, None, 1] - a[None, :, 1]) - \
         (b[None, :, 1] - a[None, :, 1]) * (pts[:, None, 0] - a[None, :, 0])
    return int(np.sum(np.all(cr >= 0, axis=1)))


def collision_time(points_base, vel, z):
    """Polygon::getCollisionTime: the footprint already holding min_points scan points gives 0; else project the
    robot at the command (kinematics.cpp projectState) in steps of simulation_time_step up to
    time_before_collision; the first projected pose whose footprint holds min_points points gives the loop's time
    at that step (0.0 for the first step); -1 if none. Also returns the projected poses."""
    if points_inside(z["poly"], points_base) >= z["min_points"]:
        return 0.0, [(0.0, 0.0, 0.0)]
    pose = [0.0, 0.0, 0.0]
    vx, vy, w = vel[0], 0.0, vel[1]
    steps, t, dt = [], 0.0, z["simulation_time_step"]
    while t <= z["time_before_collision"] + 1e-9:
        th = w * dt
        pose = [pose[0] + vx * dt, pose[1] + vy * dt, pose[2] + th]
        vx, vy = vx * math.cos(th) - vy * math.sin(th), vx * math.sin(th) + vy * math.cos(th)
        steps.append(tuple(pose))
        c, s = math.cos(pose[2]), math.sin(pose[2])
        dx, dy = points_base[:, 0] - pose[0], points_base[:, 1] - pose[1]
        if points_inside(z["poly"], np.column_stack([dx * c + dy * s, -dx * s + dy * c])) >= z["min_points"]:
            return t, steps
        t = round(t + dt, 10)
    return -1.0, steps


def monitor(points_base, cmd, zones=MONITOR_BRINGUP):
    """CollisionMonitor::process: start from the incoming command; each zone may make it safer (smaller
    v^2 + w^2): stop -> 0; slowdown -> x slowdown_ratio; limit -> scaled so v <= linear_limit and |w| <= angular_limit;
    approach -> x (time to collision / time_before_collision). A stop ends the checks.
    Returns (command out, name of the zone that acted or None, time to collision of the approach zone, its poses)."""
    req, who, tc, steps = cmd, None, -1.0, []
    mag = lambda v: v[0] ** 2 + v[1] ** 2
    for z in zones:
        if z["action"] == "approach":
            tc, steps = collision_time(points_base, cmd, z)
            if tc >= 0.0:
                k = tc / z["time_before_collision"]
                safe = (cmd[0] * k, cmd[1] * k)
                if mag(safe) < mag(req):
                    req, who = safe, z["name"]
            continue
        if points_inside(z["poly"], points_base) < z["min_points"]:
            continue
        if z["action"] == "stop":
            req, who = (0.0, 0.0), z["name"] + ":stop"
            break
        if z["action"] == "slowdown":
            safe = (cmd[0] * z["slowdown_ratio"], cmd[1] * z["slowdown_ratio"])
        else:
            ratio = 1.0
            if cmd[0] != 0.0:
                ratio = min(ratio, z["linear_limit"] / abs(cmd[0]))
            if cmd[1] != 0.0:
                ratio = min(ratio, z["angular_limit"] / abs(cmd[1]))
            ratio = min(max(ratio, 0.0), 1.0)
            safe = (cmd[0] * ratio, cmd[1] * ratio)
        if mag(safe) < mag(req):
            req, who = safe, z["name"]
    return req, who, tc, steps


# ---------------------------------------------------------------- the behaviour tree (the default tree's nodes on our run)
class Tree:
    """navigate_to_pose_w_replanning_and_recovery.xml, ticked every 10 ms: the selectors return SUCCESS; the
    RateController (1 Hz) ticks the replanning branch: a new path only when the goal was updated, the goal is farther
    than 4.0 m along the path, or the remaining path is invalid on the global costmap (ValidatePath); FollowPath runs
    the controller server. The recovery branch is ticked only when one of them fails."""

    def __init__(self):
        self.path = None
        self.rate_start = None
        self.first = True
        self.events = []

    def tick(self, t, sim):
        # PipelineSequence: 5 selectors (SUCCESS), RateController, FollowPath
        run_child = self.first or (t - self.rate_start >= 1.0 / P["replan_hz"] - 1e-9)
        if run_child:
            self.first = False
            need, why = True, "no path yet"
            if self.path is not None:
                remaining = sim.remaining_length(self.path)
                nearby = remaining < P["proximity_threshold"]
                ok, k = path_valid(sim.gcm.cost, self.path, sim.map_pose())
                need = not (nearby and ok)
                why = "path blocked on the global costmap" if not ok else ("goal far" if not nearby else "")
                self.events.append(dict(t=t, node="CheckIfNewPathNeeded", status="FAILURE" if need else "SUCCESS",
                                        remaining=remaining, valid=ok, blocked_index=k))
            if need:
                path, reached = navfn(sim.gcm.cost, sim.map_pose(), GOAL)
                self.events.append(dict(t=t, node="ComputePathToPose", status="SUCCESS" if path is not None else
                                        "FAILURE", why=why, length=D.path_length(path) if path is not None else None,
                                        reached=reached))
                if path is None:
                    return "FAILURE"
                self.path = path
                sim.new_path(path, t)
            self.rate_start = t
        status = sim.follow_path_status()
        return status


# ---------------------------------------------------------------- the whole goal
class Sim:
    def __init__(self, person=D.PERSON, t_person=D.T_PERSON, seed=0, t_end=20.0, keep=(), zones=MONITOR_BRINGUP):
        self.rng = np.random.default_rng(seed)
        self.person, self.t_person, self.t_end, self.keep, self.zones = person, t_person, t_end, keep, zones
        self.occ, self.unknown = build_map()
        self.true = START.copy()
        self.v = self.w = 0.0
        self.odom = START.copy()                      # odom frame placed on the map at the start
        self.odom_vel = (0.0, 0.0)
        self.amcl = AMCL(self.occ, START.copy(), self.rng)
        self.gcm = Costmap("global", self.occ, self.unknown)
        self.lcm = Costmap("local")
        self.tree = Tree()
        self.crit = D.Critics(DWB)
        self.plan_map = None
        self.check_xy = True
        self.prog_pose, self.prog_t = None, 0.0
        self.last_valid = 0.0
        self.result = None
        self.cmd_nav = self.cmd_smooth = self.cmd_out = (0.0, 0.0)
        self.log = []
        self.plans = []
        self.costmap_snaps = {}
        self.scan = None

    # frames
    def map_to_odom(self):
        return self.amcl.map_to_odom() if self.amcl.last_odom is not None else np.zeros(3)

    def map_pose(self):
        return compose(self.map_to_odom(), self.odom)

    def remaining_length(self, path):
        q = self.map_pose()
        k0 = int(np.argmin(np.hypot(path[:, 0] - q[0], path[:, 1] - q[1])))
        return D.path_length(path[k0:])

    def new_path(self, path, t):
        """The controller server receives a new path (FollowPath goal update): setPlannerPath resets the goal
        checker, and DWB's critics start afresh (newPathReceived)."""
        self.plan_map = path.copy()
        self.plans.append((t, path.copy()))
        self.crit.in_window = self.crit.rotating = False
        self.crit.trend = {"x": [0, False, False], "theta": [0, False, False]}
        self.check_xy = True
        if self.prog_pose is None:
            self.prog_pose, self.prog_t = self.odom.copy(), t

    def follow_path_status(self):
        if self.result is None:
            return "RUNNING"
        return "SUCCESS" if self.result == "goal reached" else "FAILURE"

    def controller_cycle(self, t, keep):
        """ControllerServer::computeControl at 20 Hz, as RO-078's run(): the plan in the odom frame, pruned and cut
        to the local costmap, the goal and progress checks, DWB's command."""
        m2o = inverse(self.map_to_odom())
        plan = np.array([compose(m2o, q) for q in self.plan_map])
        goal = plan[-1].copy()
        x = self.odom.copy()
        cm = self.lcm
        upper = D.first_after_integrated_distance(plan, 0, cm.n * cm.res / 2)
        dists = np.hypot(plan[:upper, 0] - x[0], plan[:upper, 1] - x[1])
        k0 = int(np.argmin(dists))
        if len(plan) > 1 and k0 == len(plan) - 1:
            k0 -= 1
        k1 = D.first_after_integrated_distance(plan, k0, DWB["prune_distance"])
        local = []
        for q in plan[k0:k1]:
            if not np.all(cm.world_to_map(q[0], q[1])[2]):
                break
            local.append(q)
        local = np.array(local)
        self.plan_map = self.plan_map[k0:]
        if D.path_length(local) <= DWB["path_length_tolerance"]:
            if self.check_xy and math.hypot(x[0] - goal[0], x[1] - goal[1]) <= DWB["xy_goal_tolerance"]:
                self.check_xy = False
            if not self.check_xy and abs(D.wrap(goal[2] - x[2])) <= DWB["yaw_goal_tolerance"]:
                self.result = "goal reached"
                return (0.0, 0.0), None, local
        if math.hypot(x[0] - self.prog_pose[0], x[1] - self.prog_pose[1]) > DWB["required_movement_radius"]:
            self.prog_pose, self.prog_t = x.copy(), t
        elif t - self.prog_t > DWB["movement_time_allowance"]:
            self.result = "failed to make progress"
            return (0.0, 0.0), None, local
        vel = (self.odom_vel[0] if abs(self.odom_vel[0]) >= DWB["min_x_velocity_threshold"] else 0.0,
               self.odom_vel[1] if abs(self.odom_vel[1]) >= DWB["min_theta_velocity_threshold"] else 0.0)
        cmd, rec = D.compute_velocity(self.crit, cm, x, vel, goal, local, DWB, keep=keep)
        if cmd is None:
            cmd = (0.0, 0.0)
            if t - self.last_valid > DWB["failure_tolerance"]:
                self.result = "controller patience exceeded"
        else:
            self.last_valid = t
        return cmd, rec, local

    def run(self):
        t, k = 0.0, 0
        next_scan = next_g = next_l = 0.0
        steps_cycle = int(round(CYCLE / DT))
        while t < self.t_end - 1e-9:
            seen = self.person if (self.person is not None and t >= self.t_person - 1e-9) else None
            # laser and AMCL
            if t >= next_scan - 1e-9:
                r = scan(self.true, seen, self.rng)
                self.scan = (t, self.odom.copy(), r)
                self.amcl.scan_received(t, self.odom.copy(), r)
                next_scan += 1.0 / P["scan_rate"]
            # costmaps
            if t >= next_g - 1e-9:
                so = compose(self.map_to_odom(), self.scan[1])
                self.gcm.update(so, self.scan[2], self.map_pose())
                next_g += 1.0 / P["global_update_frequency"]
            if t >= next_l - 1e-9:
                self.lcm.update(self.scan[1], self.scan[2], self.odom)
                next_l += 1.0 / P["local_update_frequency"]
            # behaviour tree, every 10 ms
            status = self.tree.tick(t, self)
            if status != "RUNNING":
                break
            if k % steps_cycle == 0:
                keep = any(abs(t - kt) < 1e-6 for kt in self.keep)
                cmd, rec, local = self.controller_cycle(t, keep)
                self.cmd_nav = cmd
                self.cmd_smooth = smooth(self.cmd_smooth, self.cmd_nav)
                pts = scan_points(np.zeros(3), self.scan[2])
                self.cmd_out, who, tc, csteps = monitor(pts, self.cmd_smooth, self.zones)
                self.log.append(dict(t=t, true=self.true.copy(), odom=self.odom.copy(), map=self.map_pose(),
                                     v=self.v, w=self.w, cmd_nav=cmd, cmd_smooth=self.cmd_smooth,
                                     cmd_out=self.cmd_out, zone=who, tc=tc,
                                     csteps=csteps if keep or 0 <= tc else None, scan_base=pts if who else None,
                                     person=seen, local=local, rec=rec if keep else None,
                                     best=None if rec is None or rec.get("cmd") is None else rec.get("traj"),
                                     lcm=(self.lcm.cost.copy(), self.lcm.ox, self.lcm.oy, self.lcm.lethal.copy())
                                     if keep else None,
                                     gcm=(self.gcm.cost.copy(), self.gcm.lethal.copy()) if keep else None,
                                     m2o=self.map_to_odom(), plan=None if self.plan_map is None else
                                     self.plan_map.copy(),
                                     n_particles=len(self.amcl.x)))
                if self.result is not None and self.result != "goal reached":
                    break
            # the base follows cmd_vel within its limits; odometry with the smaller left wheel
            v0, w0 = self.v, self.w
            self.v += float(np.clip(self.cmd_out[0] - self.v, -D.A_MAX * DT, D.A_MAX * DT))
            self.w += float(np.clip(self.cmd_out[1] - self.w, -DWB["acc_lim_theta"] * DT, DWB["acc_lim_theta"] * DT))
            lim = (D.V_WHEEL - abs(self.v)) / (D.L_AXLE / 2)
            self.w = float(np.clip(self.w, -lim, lim))
            th = self.true[2]
            self.true = self.true + DT * np.array([self.v * math.cos(th + self.w * DT / 2),
                                                   self.v * math.sin(th + self.w * DT / 2), self.w])
            self.true[2] = D.wrap(self.true[2])
            vr = self.v + self.w * D.L_AXLE / 2
            vl = (self.v - self.w * D.L_AXLE / 2) / P["left_wheel_scale"]   # encoder ticks read as a bigger wheel
            vo, wo = (vr + vl) / 2, (vr - vl) / D.L_AXLE
            tho = self.odom[2]
            self.odom = self.odom + DT * np.array([vo * math.cos(tho + wo * DT / 2), vo * math.sin(tho + wo * DT / 2), wo])
            self.odom[2] = D.wrap(self.odom[2])
            self.odom_vel = (vo, wo)
            t = round(t + DT, 10)
            k += 1
        self.t_final = t
        return self


def _run(kw):
    sim = Sim(**kw).run()
    return dict(log=sim.log, plans=sim.plans, events=sim.tree.events, amcl=sim.amcl.updates, result=sim.result,
                t_final=sim.t_final, occ=sim.occ, unknown=sim.unknown)


JOBS = dict(
    main=dict(keep=(0.0, 1.0, 2.4, 2.55, 3.0)),                             # the goal of the Note, bring-up monitor
    clear=dict(person=None),                                                 # the clear room
    alpha_bringup=dict(),                                                    # AMCL with the bring-up alphas 0.2
    example_zones=dict(),                                                    # the package's example monitor zones
)


def results():
    """Every run the Note quotes (cached by this file's and dwbkit's text)."""
    import hashlib
    import pickle
    import tempfile
    from concurrent.futures import ProcessPoolExecutor
    from pathlib import Path
    here = Path(__file__).parent
    key = hashlib.sha1((here / "nav2sim.py").read_bytes() + (here / "dwbkit.py").read_bytes()).hexdigest()[:12]
    f = Path(tempfile.gettempdir()) / "ro080_cache" / f"nav2_{key}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    jobs = {k: dict(v) for k, v in JOBS.items()}
    jobs["example_zones"]["zones"] = MONITOR_EXAMPLE
    with ProcessPoolExecutor(len(jobs)) as ex:
        futs = {k: ex.submit(_run_with, k, v) for k, v in jobs.items()}
        R = {k: fu.result() for k, fu in futs.items()}
    f.parent.mkdir(exist_ok=True)
    f.write_bytes(pickle.dumps(R))
    return R


def _run_with(name, kw):
    if name == "alpha_bringup":
        P["alpha"] = (0.2, 0.2, 0.2, 0.2)
    return _run(kw)


if __name__ == "__main__":
    assert lifecycle_bringup()[0] == ("map_server", "configure", "inactive") and len(lifecycle_bringup()) == 34
    occ, unk = build_map()
    assert occ.shape == (100, 160)
    c = inflation(np.pad(np.ones((1, 1), bool), 20))
    assert c[20, 20] == LETHAL and c[20, 25] == INSCRIBED and c[20, 26] == int(252 * math.exp(-3 * 0.05))
    assert smooth((0.0, 0.0), (0.6, 0.0)) == (0.025, 0.0)
    print("nav2sim self-check passed")
