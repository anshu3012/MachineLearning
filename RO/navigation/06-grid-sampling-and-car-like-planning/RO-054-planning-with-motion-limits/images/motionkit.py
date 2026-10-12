"""The robot of this Note and its motion limits (no output when run on its own).

The robot: RO-001's differential drive (wheel separation 0.2 m) with RO-037's disk footprint (radius 0.25 m), in
RO-009's room, the door closed. Its limits: each wheel at most 0.6 m/s, the forward speed changes by at most 0.5 m/s
per second. Driving at 0.5 m/s it can turn at most 1 rad/s, a circle of radius 0.5 m.

Contents:
- the free space of the robot's centre (obstacles grown by 0.25 m, walls moved in by 0.25 m);
- simulate(): the system simulator, Euler steps of 0.01 s of x' = v cos(theta), y' = v sin(theta), theta' = omega;
- the straight drive towards the closed door along RO-037's line, its phase space, the region of inevitable collision
  and the lattice search;
- the kinodynamic RRT with three motion primitives."""
import heapq
import math

import numpy as np
import shapely
from roommap import CAB, H, POLE_R, POLES, TABLE, W
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

R_BODY = 0.25                      # disk footprint radius, m
L_AXLE = 0.2                       # wheel separation, m (RO-001)
V_WHEEL = 0.6                      # top wheel speed, m/s
A_MAX = 0.5                        # largest change of forward speed, m/s per s
V_CRUISE = 0.5                     # cruising speed, m/s
W_MAX = round(2 * (V_WHEEL - V_CRUISE) / L_AXLE, 12)   # largest turn rate at the cruising speed: 1 rad/s
RHO = round(V_CRUISE / W_MAX, 12)  # tightest circle at the cruising speed: 0.5 m
START = (2.0, 1.0, math.radians(30))           # RO-001's pose
DOOR_POSE = (3.6, 3.5, math.radians(90))       # in front of the closed door, facing it
W_HEADING = 0.25                   # metres counted per radian of heading difference (RO-038 7.3)

# ---------------------------------------------------------------- free space of the centre
OBST = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                   + [Point(p).buffer(POLE_R, quad_segs=64) for p in POLES.values()])
GROWN = OBST.buffer(R_BODY, quad_segs=32)
INNER = box(R_BODY, R_BODY, W - R_BODY, H - R_BODY)            # the door is closed: the top wall is whole
FREE = INNER.difference(GROWN)
shapely.prepare(FREE)


def free_xy(x, y):
    """True where the centre (x, y) keeps the disk off every obstacle and wall (arrays allowed)."""
    return shapely.contains_xy(FREE, x, y)


def clearance(x, y):
    """Distance from the centre to the nearest obstacle or wall, minus the radius (negative: overlap)."""
    p = Point(x, y)
    walls = min(x, y, W - x, H - y)
    return min(walls, OBST.distance(p)) - R_BODY


# ---------------------------------------------------------------- system simulator
H_STEP = 0.01


def simulate(pose, v, omega, duration, h=H_STEP):
    """Euler steps of h seconds with constant (v, omega) for `duration` s; returns an (n + 1, 3) array of poses."""
    n = int(round(duration / h))
    out = np.empty((n + 1, 3))
    out[0] = pose
    x, y, th = pose
    for k in range(1, n + 1):
        x, y, th = x + v * math.cos(th) * h, y + v * math.sin(th) * h, th + omega * h
        out[k] = (x, y, th)
    return out


def wheel_speeds(v, omega):
    """Right and left wheel speeds over the floor (RO-001 4.5)."""
    return v + omega * L_AXLE / 2, v - omega * L_AXLE / 2


# ---------------------------------------------------------------- the straight drive to the closed door
LINE_FROM, LINE_TO = (2.0, 1.0), (3.6, 4.0)                   # RO-037 2.4: 3.4 m at 61.9 degrees
LINE_LEN = math.hypot(LINE_TO[0] - LINE_FROM[0], LINE_TO[1] - LINE_FROM[1])
LINE_DIR = ((LINE_TO[0] - LINE_FROM[0]) / LINE_LEN, (LINE_TO[1] - LINE_FROM[1]) / LINE_LEN)
LINE_HEADING = math.atan2(LINE_DIR[1], LINE_DIR[0])
S_DOOR = (H - R_BODY - LINE_FROM[1]) / LINE_DIR[1]           # distance along the line at which the disk meets the door
S_GOAL = 3.0                                                  # where the robot should stop
V_TOP = V_WHEEL                                               # top forward speed, m/s


def on_line(s):
    return (LINE_FROM[0] + s * LINE_DIR[0], LINE_FROM[1] + s * LINE_DIR[1])


def stopping_distance(v, a=A_MAX):
    return v * v / (2 * a)


def inevitable(s, v):
    """True when the state (s, v) of the straight drive cannot avoid the door: it needs more room to stop than it has."""
    return s + stopping_distance(v) > S_DOOR + 1e-12


def brake_run(s0, v0, a=A_MAX, h=0.01):
    """Brake at a from (s0, v0); returns times, positions, speeds until stopped or at the door."""
    t, s, v = [0.0], [s0], [v0]
    while v[-1] > 0 and s[-1] < S_DOOR:
        dt = min(h, v[-1] / a)
        s_next = s[-1] + v[-1] * dt - 0.5 * a * dt * dt
        if s_next > S_DOOR:                                   # stop the run exactly where the disk meets the door
            v_hit = math.sqrt(v[-1] ** 2 - 2 * a * (S_DOOR - s[-1]))
            dt, s_next = (v[-1] - v_hit) / a, S_DOOR
        s.append(s_next)
        v.append(v[-1] - a * dt)
        t.append(t[-1] + dt)
    return np.array(t), np.array(s), np.array(v)


def lattice_search(dt, s_goal=S_GOAL, v_top=V_TOP, a=A_MAX, trace=False):
    """Breadth-first search on the lattice of the straight drive (LaValle 14.4.1): every dt seconds the robot
    accelerates (+a), coasts (0) or brakes (-a). Speeds are whole multiples of a dt, positions whole multiples of
    q = a dt^2 / 2, so a state is a pair of integers (i, j): s = i q, v = j a dt. From (i, j) the action k in
    {-1, 0, 1} gives (i + 2 j + k, j + k). States with s > S_DOOR or v outside [0, v_top] are not allowed.
    Returns the number of steps to (s_goal, 0), the time, the path of states and, with trace, the levels."""
    q, dv = a * dt * dt / 2, a * dt
    jmax = int(math.floor(v_top / dv + 1e-9))
    imax = int(math.floor(S_DOOR / q + 1e-9))
    goal = (int(round(s_goal / q)), 0)
    assert abs(goal[0] * q - s_goal) < 1e-9, "the goal must be a lattice point"
    start = (0, 0)
    parent = {start: None}
    level = [start]
    levels = [level]
    steps = 0
    while level and goal not in parent:
        nxt = []
        for i, j in level:
            for k in (1, 0, -1):
                n = (i + 2 * j + k, j + k)
                if 0 <= n[1] <= jmax and 0 <= n[0] <= imax and n not in parent:
                    parent[n] = (i, j)
                    nxt.append(n)
        level = nxt
        levels.append(level)
        steps += 1
    if goal not in parent:
        return None
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    path = [(i * q, j * dv) for i, j in reversed(path)]
    out = dict(steps=steps, time=steps * dt, path=path, q=q, dv=dv, n_states=len(parent))
    if trace:
        out["levels"] = [[(i * q, j * dv) for i, j in lv] for lv in levels]
    return out


def bang_coast_bang(s_goal=S_GOAL, v_top=V_TOP, a=A_MAX):
    """Least time to drive s_goal from rest to rest with |accel| <= a and v <= v_top: speed up, cruise, brake."""
    s_ramp = v_top * v_top / a                                   # speeding up plus braking
    if s_ramp >= s_goal:
        return 2 * math.sqrt(s_goal / a)
    return 2 * v_top / a + (s_goal - s_ramp) / v_top


# ---------------------------------------------------------------- moving at the cruising speed
PRIMS = {"left": W_MAX, "straight": 0.0, "right": -W_MAX}      # turn rates of the three forward primitives
DT_PRIM = 0.75                                                # how long each primitive is held, s


def heading_gap(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def metric(p, q):
    """RO-038's weighted distance: metres plus 0.25 m per radian of heading difference."""
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (W_HEADING * heading_gap(p[2], q[2])) ** 2)


def edge_free(traj):
    return bool(np.all(free_xy(traj[:, 0], traj[:, 1])))


def in_goal(p, goal=DOOR_POSE, r_pos=0.25, r_head=math.radians(25)):
    return math.hypot(p[0] - goal[0], p[1] - goal[1]) <= r_pos and heading_gap(p[2], goal[2]) <= r_head


def kino_rrt(seed=4, dt=DT_PRIM, goal=DOOR_POSE, goal_bias=0.1, max_nodes=4000):
    """Kinodynamic RRT (LaValle 1998; MR 10.5): sample a pose, take the nearest node by the weighted metric, simulate
    each of the three primitives for dt seconds from it, keep the end closest to the sample, add it if the swept
    path is free. Stops when a node lands in the goal region (0.25 m and 25 degrees around the goal pose).
    Returns the tree and, for the animation, a log of every iteration."""
    rng = np.random.default_rng(seed)
    nodes, parent, trajs = [tuple(START)], [-1], [None]
    log = []
    while len(nodes) < max_nodes:
        if rng.random() < goal_bias:
            samp, kind = tuple(goal), "goal"
        else:
            samp = (rng.uniform(R_BODY, W - R_BODY), rng.uniform(R_BODY, H - R_BODY), rng.uniform(-math.pi, math.pi))
            kind = "random"
        arr = np.array(nodes)
        dth = np.abs(arr[:, 2] - samp[2]) % (2 * math.pi)
        dth = np.minimum(dth, 2 * math.pi - dth)
        d = np.sqrt((arr[:, 0] - samp[0]) ** 2 + (arr[:, 1] - samp[1]) ** 2 + (W_HEADING * dth) ** 2)
        near = int(np.argmin(d))
        cands = {name: simulate(nodes[near], V_CRUISE, om, dt) for name, om in PRIMS.items()}
        best = min(cands, key=lambda k: metric(tuple(cands[k][-1]), samp))
        ok = edge_free(cands[best])
        entry = dict(sample=samp, kind=kind, near=near, cands=cands, best=best, ok=ok, new=None)
        if ok:
            nodes.append(tuple(cands[best][-1]))
            parent.append(near)
            trajs.append(cands[best])
            entry["new"] = len(nodes) - 1
        log.append(entry)
        if ok and in_goal(nodes[-1], goal):
            break
    path = [len(nodes) - 1]
    while parent[path[-1]] != -1:
        path.append(parent[path[-1]])
    path.reverse()
    reached = in_goal(nodes[-1], goal)
    return dict(nodes=nodes, parent=parent, trajs=trajs, log=log, path=path, reached=reached,
                length=V_CRUISE * dt * (len(path) - 1))


# ---------------------------------------------------------------- reachable set
def reach_trails(T=2.0, n=400, seed=1, h=0.02):
    """Trajectories of the robot at 0.5 m/s from START for T seconds under random turn rates in [-1, 1] rad/s, held
    for random lengths of time, plus the three extremes (full left, straight, full right)."""
    rng = np.random.default_rng(seed)
    steps = int(round(T / h))
    trails = []
    for om in (W_MAX, 0.0, -W_MAX):
        trails.append(simulate(START, V_CRUISE, om, T, h=h))
    for _ in range(n):
        om = np.empty(steps)
        k = 0
        while k < steps:
            hold = int(rng.integers(5, 40))
            om[k:k + hold] = rng.choice([-W_MAX, 0.0, W_MAX]) if rng.random() < 0.6 else rng.uniform(-W_MAX, W_MAX)
            k += hold
        x, y, th = START
        tr = [(x, y, th)]
        for j in range(steps):
            x, y, th = x + V_CRUISE * math.cos(th) * h, y + V_CRUISE * math.sin(th) * h, th + om[j] * h
            tr.append((x, y, th))
        trails.append(np.array(tr))
    return trails


# ---------------------------------------------------------------- Reeds-Shepp pieces along a route (MR 13.3.3)
ROUTE = [(2.0, 1.0), (2.75, 1.75), (2.75, 3.25), (3.6, 3.5)]   # straight pieces round the table's left side


def route_pose(f, route=ROUTE):
    """Pose at fraction f of the route's length: the point, facing along its piece; the ends are START and DOOR_POSE."""
    if f <= 0:
        return START
    if f >= 1:
        return DOOR_POSE
    lens = [math.dist(a, b) for a, b in zip(route, route[1:])]
    d = f * sum(lens)
    for (a, b), ln in zip(zip(route, route[1:]), lens):
        if d <= ln + 1e-12:
            t = d / ln
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), math.atan2(b[1] - a[1], b[0] - a[0]))
        d -= ln


def subdivide(max_depth=6):
    """Try a Reeds-Shepp path between the route's two ends; if it hits an obstacle, halve the stretch and try each
    half (MR 13.3.3). Returns the tries in order, (f0, f1, path, free), and the pieces kept."""
    import carpaths as cp
    tries, kept = [], []

    def solve(f0, f1, depth):
        a, b = route_pose(f0), route_pose(f1)
        p = cp.reeds_shepp(a, b, RHO)
        pts = cp.sample(a, p, RHO)
        ok = bool(np.all(free_xy(pts[:, 0], pts[:, 1])))
        tries.append((f0, f1, p, ok))
        if ok:
            kept.append((f0, f1, p))
            return
        assert depth < max_depth, "subdivision did not converge"
        fm = (f0 + f1) / 2
        solve(f0, fm, depth + 1)
        solve(fm, f1, depth + 1)

    solve(0.0, 1.0, 0)
    return tries, kept
