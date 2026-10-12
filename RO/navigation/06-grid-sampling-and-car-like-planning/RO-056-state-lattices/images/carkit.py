"""The car-like robot and the parking lot of this Note, and its planners (no output when run on its own).

The car: rear-axle reference point (x, y, theta), wheelbase 2.5 m, body 4.0 m x 1.8 m with the rear axle 0.75 m from
the rear bumper, tightest circle (minimum turning radius) 5 m, so the largest steering angle is atan(2.5 / 5) = 26.6 deg.
The lot: 24 m x 24 m. The lower lane runs along the bottom wall (y 0-7); a middle row of six parked cars (bays 2.5 m
wide, y 7-12, x 0.75-15.75) separates it from the upper lane (y 12-19), and the two lanes meet at the right end
(x 15.75-24). Along the top wall a row of nine bays (y 19-24) holds a parked car (4.0 m x 1.8 m) in every bay except
the target bay, x 10.75-13.25. Start: (2, 3, 0 deg) in the lower lane; goal: backed into the target bay, nose out,
rear axle at (12, 23, -90 deg).

Contents: collision test of the body (separating-axis test against the parked cars and the walls), the 1 m grid with
cells centred on whole metres, A* on the grid (RO-034), the 2D distance-to-goal map, Hybrid A* (Dolgov et al. 2008)
with its six arcs, and the smoother (Udacity CS373)."""
import heapq
import math

import numpy as np
from carpaths import _candidates, reeds_shepp, sample, step

RHO = 5.0                         # tightest circle, m
WHEELBASE = 2.5                   # m
CAR_L, CAR_W, REAR_OH = 4.0, 1.8, 0.75
STEER_MAX = math.atan(WHEELBASE / RHO)
LOT_W, LOT_H = 24.0, 24.0
BAY_W = 2.5
ISLAND = [0.75 + BAY_W * (k + 0.5) for k in range(6)]           # bay centres of the middle row: 2.0 ... 14.5
TOP = [0.75 + BAY_W * (k + 0.5) for k in range(9)]              # bay centres of the top row: 2.0 ... 22.0
TARGET_X = 12.0
START = (2.0, 3.0, 0.0)
GOAL = (12.0, 23.0, -math.pi / 2)

PARKED = [(c - CAR_W / 2, c + CAR_W / 2, 7.5, 11.5) for c in ISLAND]          # the middle row of parked cars
PARKED += [(c - CAR_W / 2, c + CAR_W / 2, 19.5, 23.5) for c in TOP if c != TARGET_X]
WALLS = [(-1.0, 0.0, -1.0, LOT_H + 1), (LOT_W, LOT_W + 1, -1.0, LOT_H + 1),
         (-1.0, LOT_W + 1, -1.0, 0.0), (-1.0, LOT_W + 1, LOT_H, LOT_H + 1)]
OBS = np.array(PARKED + WALLS)                                     # rows (x0, x1, y0, y1)
_OC = np.stack([(OBS[:, 0] + OBS[:, 1]) / 2, (OBS[:, 2] + OBS[:, 3]) / 2], axis=1)
_OH = np.stack([(OBS[:, 1] - OBS[:, 0]) / 2, (OBS[:, 3] - OBS[:, 2]) / 2], axis=1)
MARGIN = 0.1                      # the collision test uses a body 0.1 m larger on every side
_A, _B = CAR_L / 2 + MARGIN, CAR_W / 2 + MARGIN                    # tested half length, half width
_FWD = CAR_L / 2 - REAR_OH                                         # rear axle to body centre, 1.25 m


def body_corners(pose):
    """The four corners of the body at a pose (rear-left, front-left, front-right, rear-right)."""
    x, y, th = pose
    c, s = math.cos(th), math.sin(th)
    out = []
    for a, b in ((-REAR_OH, CAR_W / 2), (CAR_L - REAR_OH, CAR_W / 2), (CAR_L - REAR_OH, -CAR_W / 2),
                 (-REAR_OH, -CAR_W / 2)):
        out.append((x + a * c - b * s, y + a * s + b * c))
    return out


def collides(poses, margin=None):
    """True for every pose whose body, grown by the 0.1 m margin, overlaps a parked car or a wall: the
    separating-axis test between the body (a turned rectangle) and each obstacle (an upright rectangle).
    poses: (n, 3) array. margin=0 tests the body itself."""
    a_, b_ = (_A, _B) if margin is None else (CAR_L / 2 + margin, CAR_W / 2 + margin)
    p = np.atleast_2d(np.asarray(poses, dtype=float))
    c, s = np.cos(p[:, 2]), np.sin(p[:, 2])
    cx, cy = p[:, 0] + _FWD * c, p[:, 1] + _FWD * s
    dx, dy = cx[:, None] - _OC[None, :, 0], cy[:, None] - _OC[None, :, 1]
    hx, hy = _OH[None, :, 0], _OH[None, :, 1]
    ac, as_ = np.abs(c)[:, None], np.abs(s)[:, None]
    sep = np.abs(dx) > a_ * ac + b_ * as_ + hx
    sep |= np.abs(dy) > a_ * as_ + b_ * ac + hy
    sep |= np.abs(dx * c[:, None] + dy * s[:, None]) > a_ + hx * ac + hy * as_
    sep |= np.abs(-dx * s[:, None] + dy * c[:, None]) > b_ + hx * as_ + hy * ac
    return ~np.all(sep, axis=1)


def clearance(pose):
    """Smallest distance from the body to a parked car or a wall, in m (0 if they touch or overlap)."""
    from shapely.geometry import Polygon, box
    body = Polygon(body_corners(pose))
    return min(body.distance(box(x0, y0, x1, y1)) for x0, x1, y0, y1 in OBS)


def path_free(poses):
    return not bool(np.any(collides(poses)))


# ---------------------------------------------------------------- the 1 m grid
NX, NY = int(LOT_W) + 1, int(LOT_H) + 1                           # cells centred on whole metres


def _cell_blocked(i, j):
    x0, x1, y0, y1 = i - 0.5, i + 0.5, j - 0.5, j + 0.5
    if x0 < 0 or y0 < 0 or x1 > LOT_W or y1 > LOT_H:
        return True
    for a0, a1, b0, b1 in PARKED:
        if min(x1, a1) - max(x0, a0) > 0 and min(y1, b1) - max(y0, b0) > 0:
            return True
    return False


BLOCKED = np.array([[_cell_blocked(i, j) for i in range(NX)] for j in range(NY)])   # BLOCKED[j, i]
S2 = math.sqrt(2)
ORDER = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


def free(c):
    i, j = c
    return 0 <= i < NX and 0 <= j < NY and not BLOCKED[j, i]


def neighbours(c):
    """8-connected free neighbours with the move's length; a diagonal move may not cut a blocked cell's corner."""
    i, j = c
    out = []
    for dx, dy in ORDER:
        n = (i + dx, j + dy)
        if not free(n) or (dx and dy and not (free((i + dx, j)) and free((i, j + dy)))):
            continue
        out.append((n, S2 if dx and dy else 1.0))
    return out


def octile(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return S2 * min(dx, dy) + (max(dx, dy) - min(dx, dy))


def grid_astar(start=(2, 3), goal=(12, 23)):
    """A* on the grid with the octile distance (RO-034). Returns the route's cells, its length and the expansions."""
    g, parent, closed = {start: 0.0}, {start: None}, set()
    heap = [(octile(start, goal), octile(start, goal), start)]
    while heap:
        _, _, c = heapq.heappop(heap)
        if c in closed:
            continue
        closed.add(c)
        if c == goal:
            break
        for n, w in neighbours(c):
            if n not in closed and g[c] + w < g.get(n, math.inf) - 1e-12:
                g[n], parent[n] = g[c] + w, c
                heapq.heappush(heap, (g[n] + octile(n, goal), octile(n, goal), n))
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return dict(path=path[::-1], cost=g[goal], expanded=len(closed))


def distance_map(goal=(12, 23)):
    """Dijkstra from the goal cell over the free cells: the length of the shortest grid route from every cell to the
    goal, ignoring the car's turning limit (Dolgov's second heuristic). DIST[j, i]; inf where no route exists."""
    d = np.full((NY, NX), math.inf)
    d[goal[1], goal[0]] = 0.0
    heap = [(0.0, goal)]
    while heap:
        dc, c = heapq.heappop(heap)
        if dc > d[c[1], c[0]]:
            continue
        for n, w in neighbours(c):
            if dc + w < d[n[1], n[0]]:
                d[n[1], n[0]] = dc + w
                heapq.heappush(heap, (dc + w, n))
    return d


DIST = distance_map()


def cell_of(x, y):
    return (int(math.floor(x + 0.5)), int(math.floor(y + 0.5)))


# ---------------------------------------------------------------- heuristics
def rs_length(pose, goal=GOAL, rho=RHO):
    """Length of the shortest Reeds-Shepp path to the goal, ignoring obstacles (Dolgov's first heuristic)."""
    dx, dy = goal[0] - pose[0], goal[1] - pose[1]
    c, s = math.cos(pose[2]), math.sin(pose[2])
    x, y = (c * dx + s * dy) / rho, (-s * dx + c * dy) / rho
    return rho * min(sum(abs(v) for v in ls) for _, ls in _candidates(x, y, goal[2] - pose[2]))


def h_euclid(pose):
    return math.hypot(GOAL[0] - pose[0], GOAL[1] - pose[1])


def h_grid(pose):
    i, j = cell_of(pose[0], pose[1])
    return DIST[j, i] if 0 <= i < NX and 0 <= j < NY else math.inf


HEURISTICS = {"euclid": h_euclid, "rs": rs_length, "grid": h_grid,
              "max": lambda p: max(rs_length(p), h_grid(p))}

# ---------------------------------------------------------------- Hybrid A*
STEP = 1.5                        # length of one arc, m: longer than a cell's diagonal, 1.414 m
NBINS = 72                        # heading bins of 5 deg (Dolgov; Nav2's default)
REV_MULT = 2.0                    # reverse costs twice as much (Nav2 reverse_penalty)
SWITCH = 2.0                      # extra cost each time the car switches between forward and reverse, m
PRIMS = [(d, k) for d in (1, -1) for k in ("L", "S", "R")]       # (direction, steering) of the six arcs
CHECK_DS = 0.25                   # spacing of the body checks along an arc, m
HEAD_TOL = math.radians(10)       # heading error accepted at the goal when no shot is used


def bin_of(th):
    return int(round(th / (2 * math.pi / NBINS))) % NBINS


def key_of(pose):
    i, j = cell_of(pose[0], pose[1])
    return (i, j, bin_of(pose[2]))


def arc(pose, direction, kind, length=STEP):
    """Poses every 0.25 m along one arc of the given direction (+1 forward, -1 reverse) and steering (L, S, R)."""
    n = int(round(length / CHECK_DS))
    return np.array([pose] + [step(pose, kind, direction * length * k / n, RHO) for k in range(1, n + 1)])


def arc_cost(direction, kind, prev_direction):
    c = STEP * (REV_MULT if direction < 0 else 1.0)
    if prev_direction is not None and prev_direction != direction:
        c += SWITCH
    return c


def rs_cost(path):
    """Cost of a Reeds-Shepp path with the same rules as the arcs (reverse x2, each switch +2 m)."""
    c, prev = 0.0, None
    for kind, s in path:
        d = 1 if s > 0 else -1
        c += abs(s) * (REV_MULT if d < 0 else 1.0)
        if prev is not None and prev != d:
            c += SWITCH
        prev = d
    return c


def shot_every(h):
    """How many expansions between two attempts of the Reeds-Shepp shot: fewer as the goal comes nearer (Dolgov)."""
    return max(1, int(h // 3))


def hybrid_astar(heuristic="max", shot=True, trace=False, max_expansions=200000, start=START, goal=GOAL):
    """Hybrid A*: A* over (cell, heading bin) keys, each holding one continuous pose; expanding a pose drives the six
    arcs; a child whose key is already closed, or open with a smaller cost so far, is dropped. With shot=True, every
    few expansions the Reeds-Shepp path from the expanded pose to the goal is checked and, if free, ends the search.
    Returns the path as a list of segments, the expansions and the counts."""
    hf = HEURISTICS[heuristic]
    sk = key_of(start)
    nodes = {sk: dict(pose=start, g=0.0, parent=None, traj=None, d=None, kind=None)}
    heap = [(hf(start), 0, sk)]
    closed, counter, expanded, since_shot = set(), 1, 0, 0
    log, generated, dropped = [], 0, 0
    goal_key = key_of(goal)
    result = None
    while heap and expanded < max_expansions:
        _, _, k = heapq.heappop(heap)
        if k in closed:
            continue
        closed.add(k)
        expanded += 1
        nd = nodes[k]
        entry = dict(key=k, pose=nd["pose"], children=[]) if trace else None
        if k[:2] == goal_key[:2] and abs(math.atan2(math.sin(nd["pose"][2] - goal[2]),
                                                     math.cos(nd["pose"][2] - goal[2]))) <= HEAD_TOL:
            result = dict(key=k, shot=None)       # in the goal's cell, heading within 10 deg: close enough
        if result is None and shot:
            since_shot += 1
            if since_shot >= shot_every(h_euclid(nd["pose"])):
                since_shot = 0
                rs = reeds_shepp(nd["pose"], goal, RHO)
                pts = sample(nd["pose"], rs, RHO, ds=CHECK_DS)
                ok = path_free(pts)
                if trace:
                    entry["shot"] = dict(path=rs, pts=pts, ok=ok)
                if ok:
                    result = dict(key=k, shot=rs)
        if trace:
            log.append(entry)
        if result is not None:
            break
        for d, kind in PRIMS:
            traj = arc(nd["pose"], d, kind)
            generated += 1
            if not path_free(traj):
                if trace:
                    entry["children"].append(dict(traj=traj, status="blocked", d=d, kind=kind))
                continue
            child = tuple(traj[-1])
            ck = key_of(child)
            g = nd["g"] + arc_cost(d, kind, nd["d"])
            if ck in closed or (ck in nodes and nodes[ck]["g"] <= g):
                dropped += 1
                if trace:
                    entry["children"].append(dict(traj=traj, status="dropped", d=d, kind=kind))
                continue
            nodes[ck] = dict(pose=child, g=g, parent=k, traj=traj, d=d, kind=kind)
            heapq.heappush(heap, (g + hf(child), counter, ck))
            counter += 1
            if trace:
                entry["children"].append(dict(traj=traj, status="added", g=g, h=hf(child), d=d, kind=kind))
    out = dict(expanded=expanded, generated=generated, dropped=dropped, found=result is not None, log=log)
    if result is None:
        return out
    segs, k = [], result["key"]
    while nodes[k]["parent"] is not None:
        segs.append(dict(d=nodes[k]["d"], kind=nodes[k]["kind"], traj=nodes[k]["traj"]))
        k = nodes[k]["parent"]
    segs.reverse()
    cost = nodes[result["key"]]["g"]
    if result["shot"] is not None:
        pre = segs[-1]["d"] if segs else None
        first = 1 if result["shot"][0][1] > 0 else -1
        cost += rs_cost(result["shot"]) + (SWITCH if pre is not None and pre != first else 0.0)
    out.update(segments=segs, shot=result["shot"], shot_from=nodes[result["key"]]["pose"], cost=cost)
    out["poses"], out["dirs"] = path_poses(out, start)
    out["length"] = float(np.sum(np.hypot(np.diff(out["poses"][:, 0]), np.diff(out["poses"][:, 1]))))
    out["cusps"] = int(np.sum(np.diff(out["dirs"]) != 0))
    return out


def path_poses(res, start, ds=CHECK_DS):
    """All poses along the found path (arcs, then the shot) and the direction (+1/-1) of the motion into each."""
    first = res["segments"][0]["d"] if res["segments"] else (1 if res["shot"][0][1] > 0 else -1)
    poses, dirs = [np.array(start)], [first]
    for s in res["segments"]:
        poses.extend(s["traj"][1:])
        dirs.extend([s["d"]] * (len(s["traj"]) - 1))
    if res["shot"] is not None:
        p = res["shot_from"]
        for kind, s in res["shot"]:
            n = max(1, int(math.ceil(abs(s) / ds)))
            for k in range(1, n + 1):
                poses.append(np.array(step(p, kind, s * k / n, RHO)))
                dirs.append(1 if s > 0 else -1)
            p = tuple(poses[-1])
    return np.array(poses), np.array(dirs)


# ---------------------------------------------------------------- smoothing (Udacity CS373)
def smooth(points, alpha=0.5, beta=0.1, tol=1e-6, max_iter=100000, keep=None):
    """Udacity CS373's smoother: start with y = x, then in every sweep move each point except the two ends by
        alpha (x_i - y_i) + beta (y_(i+1) + y_(i-1) - 2 y_i),
    all points from the last sweep's positions, until the total move in one sweep is below tol.
    Returns the result, the number of sweeps and the points after the sweeps listed in keep."""
    x = np.asarray(points, dtype=float)
    y, rec = _smooth_piece(x, 1, {0, len(x) - 1}, alpha, beta, 0.0, 0.0, tol, max_iter, keep)
    return y, rec["iters"], rec


def turning(points):
    """Dolgov's curvature at each inner vertex: the change of direction there divided by the length of the step
    into it, kappa_i = dphi_i / |dx_i| (1/m)."""
    p = np.asarray(points, dtype=float)
    d = np.diff(p, axis=0)
    ang = np.arctan2(d[:, 1], d[:, 0])
    dphi = np.abs(np.arctan2(np.sin(np.diff(ang)), np.cos(np.diff(ang))))
    return dphi / np.hypot(d[:-1, 0], d[:-1, 1]), dphi


def headings_along(points, dirs):
    """Heading at each point from the direction of travel (turned by 180 deg where the car reverses)."""
    p = np.asarray(points, dtype=float)
    d = np.gradient(p, axis=0)
    th = np.arctan2(d[:, 1], d[:, 0])
    return np.where(np.asarray(dirs) < 0, th + math.pi, th)


KAPPA_MAX = 0.2001                # 1 / 5 m as measured on 0.5 m chords of the 5 m circle (0.20008)


_U = np.linspace(0, 1, 40, endpoint=False)
_OUTLINE = np.concatenate([np.column_stack([-REAR_OH + CAR_L * _U, np.full(40, CAR_W / 2)]),
                           np.column_stack([np.full(18, CAR_L - REAR_OH), CAR_W / 2 - CAR_W * _U[:18] * 40 / 18]),
                           np.column_stack([CAR_L - REAR_OH - CAR_L * _U, np.full(40, -CAR_W / 2)]),
                           np.column_stack([np.full(18, -REAR_OH), -CAR_W / 2 + CAR_W * _U[:18] * 40 / 18])])


def body_push(points, headings, d_safe):
    """For every vertex: how far, and which way, to move it so that the car's body keeps d_safe from the nearest
    obstacle; zero where it already does (Dolgov's obstacle term, measured from 116 points on the body's outline to
    the parked cars and walls). points: (n, 2), headings: (n,)."""
    c, s = np.cos(headings)[:, None], np.sin(headings)[:, None]
    px = points[:, 0:1] + _OUTLINE[None, :, 0] * c - _OUTLINE[None, :, 1] * s          # (n, 116)
    py = points[:, 1:2] + _OUTLINE[None, :, 0] * s + _OUTLINE[None, :, 1] * c
    x0, x1, y0, y1 = (OBS[:, k][None, None, :] for k in range(4))
    ex = np.maximum(x0 - px[..., None], 0) - np.maximum(px[..., None] - x1, 0)       # (n, 116, boxes), signed
    ey = np.maximum(y0 - py[..., None], 0) - np.maximum(py[..., None] - y1, 0)
    dist = np.hypot(ex, ey)
    flat = dist.reshape(len(points), -1)
    k = np.argmin(flat, axis=1)
    r = np.arange(len(points))
    dmin = flat[r, k]
    vx, vy = -ex.reshape(len(points), -1)[r, k], -ey.reshape(len(points), -1)[r, k]   # from the obstacle to the body
    n = np.maximum(np.hypot(vx, vy), 1e-9)
    w = np.where(dmin < d_safe, d_safe - dmin, 0.0)
    return np.column_stack([vx * w / n, vy * w / n])


def pieces(res):
    """The found path cut at its cusps: list of (vertices every 0.5 m, direction). Ends and cusps are vertices."""
    P, D = res["poses"], res["dirs"]
    cuts = [0] + [i - 1 for i in range(1, len(D)) if D[i] != D[i - 1]] + [len(P) - 1]
    out = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        idx = list(range(a, b + 1, 2))
        if idx[-1] != b:
            idx.append(b)
        out.append((P[idx, :2].copy(), int(D[a + 1])))
    return out


def _smooth_piece(x, d, fixed, alpha, beta, gamma, d_safe, tol, max_iter, keep):
    """Sweeps of the smoothing update applied to all free vertices at once (each from the last sweep's points)."""
    y = x.copy()
    move = np.ones(len(x), dtype=bool)
    move[sorted(fixed)] = False
    rec = {0: y.copy()}
    for it in range(1, max_iter + 1):
        lap = np.zeros_like(y)
        lap[1:-1] = y[2:] + y[:-2] - 2 * y[1:-1]
        step_ = alpha * (x - y) + beta * lap
        if gamma:
            step_ += gamma * body_push(y, headings_along(y, np.full(len(y), d)), d_safe)
        step_[~move] = 0.0
        y = y + step_
        if keep is not None and it in keep:
            rec[it] = y.copy()
        if float(np.abs(step_).sum()) < tol:
            break
    rec["final"], rec["iters"] = y.copy(), it
    return y, rec


def smooth_path(res, alpha=0.2, beta=0.3, gamma=0.1, d_safe=0.3, tol=1e-6, max_iter=2000, keep=None):
    """Smooth each piece between cusps with the update of smooth() plus an obstacle term that pushes a vertex away
    while its body is closer than d_safe to an obstacle (Dolgov's obstacle term). The first two and last two vertices
    of every piece stay fixed, so the start, the goal and every cusp keep their position and heading. Where the
    result turns tighter than the 5 m circle, those vertices and their neighbours are also held at their places on the
    found path and the piece is smoothed again (a simple stand-in for Dolgov's curvature term).
    Returns [(vertices, direction)], the record of the last run of each piece and the number of reruns."""
    out, snaps, reruns = [], {}, 0
    for k, (x, d) in enumerate(pieces(res)):
        n = len(x)
        fixed = {0, 1, n - 2, n - 1}
        while True:
            y, rec = _smooth_piece(x, d, fixed, alpha, beta, gamma, d_safe, tol, max_iter, keep)
            kap, _ = turning(y)
            bad = {i + 1 for i in np.where(kap > KAPPA_MAX)[0]}
            if not bad:
                break
            reruns += 1
            fixed |= bad | {i - 1 for i in bad} | {i + 1 for i in bad}
        rec["fixed"] = sorted(fixed)
        out.append((y, d))
        snaps[k] = rec
    return out, snaps, reruns


def follow_route(cells, heading=START[2], look=2.0, dt=0.05, v=1.0, max_steps=3000):
    """Drive the car along a grid route as closely as its 5 m circle allows: every dt seconds steer towards the route
    point 2 m ahead (pure pursuit), with the curvature capped at 1/5 per m, at 1 m/s. Stops at the first pose whose
    body itself (no margin) touches an obstacle, or at the route's end. The car starts on the first cell with the
    given heading.
    Returns the poses and whether it collided."""
    pts = np.array(cells, dtype=float)
    x, y = pts[0]
    th = heading
    traj, seg = [(x, y, th)], 0
    for _ in range(max_steps):
        seg = max(seg, int(np.argmin(np.hypot(pts[:, 0] - x, pts[:, 1] - y))))
        tgt = next((p for p in pts[seg:] if math.hypot(p[0] - x, p[1] - y) >= look), pts[-1])
        a = math.atan2(tgt[1] - y, tgt[0] - x) - th
        a = math.atan2(math.sin(a), math.cos(a))
        kappa = max(-1 / RHO, min(1 / RHO, 2 * math.sin(a) / look))
        x, y, th = x + v * math.cos(th) * dt, y + v * math.sin(th) * dt, th + v * kappa * dt
        traj.append((x, y, th))
        if collides([traj[-1]], margin=0)[0]:
            return np.array(traj), True
        if math.hypot(x - pts[-1][0], y - pts[-1][1]) < 0.3:
            break
    return np.array(traj), False


def steering(points, direction=1):
    """Steering angle (deg) at each inner vertex: the angle that drives the vertex's curvature, atan(2.5 m x kappa),
    with kappa signed (+ left, - right) and turned for reverse driving."""
    p = np.asarray(points, dtype=float)
    d = np.diff(p, axis=0)
    ang = np.arctan2(d[:, 1], d[:, 0])
    dphi = np.arctan2(np.sin(np.diff(ang)), np.cos(np.diff(ang)))
    kappa = dphi / np.hypot(d[:-1, 0], d[:-1, 1])
    return np.degrees(np.arctan(WHEELBASE * kappa)) * direction


def dense_clearance(points, direction, ds=0.05):
    """Smallest body clearance along a polyline of rear-axle points, checked every ds metres with the heading of
    the segment (turned by 180 deg when reversing)."""
    from shapely.geometry import Polygon, box
    from shapely.ops import unary_union
    obs = unary_union([box(x0, y0, x1, y1) for x0, x1, y0, y1 in OBS])
    p = np.asarray(points, dtype=float)
    best = math.inf
    for a, b in zip(p[:-1], p[1:]):
        th = math.atan2(b[1] - a[1], b[0] - a[0]) + (math.pi if direction < 0 else 0.0)
        n = max(1, int(math.ceil(math.hypot(*(b - a)) / ds)))
        for k in range(n + 1):
            q = a + (b - a) * k / n
            best = min(best, Polygon(body_corners((q[0], q[1], th))).distance(obs))
    return best
