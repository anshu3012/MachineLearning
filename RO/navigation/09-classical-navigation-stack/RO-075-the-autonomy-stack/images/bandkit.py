"""The local planner of this Note (no output when run on its own): a timed elastic band (TEB) in the room.

Written after teb_local_planner (noetic-devel): the band is a list of poses s_k = (x_k, y_k, theta_k) with the time
dT_k between neighbours; the first pose (the robot) and the last (the local goal) are fixed. The cost is
sum dT_k^2 plus squared, weighted penalties (TEB's defaults): non-holonomic 1000, obstacle 50 (doubled after each
of 4 outer passes), wheel speed 2, acceleration 1, forward drive 1, each starting penalty_epsilon = 0.05 inside its
bound. Each outer pass resizes the band (dt_ref 0.3 s, hysteresis 0.1 s) and runs 5 Levenberg-Marquardt steps.
Our robot replaces TEB's separate speed and turn-rate limits by its own: each wheel at most 0.6 m/s (wheel
separation 0.2 m), forward acceleration at most 0.5 m/s^2; its footprint is a disk of radius 0.25 m.

Also here: the room's obstacles and the person the map does not have (a disk of radius 0.2 m), the global plan
(the A* route of RO-034 on 0.5 m cells), A* on a 0.1 m local costmap, the receding-horizon loop, the elastic-band
smoother of Autoware (second differences, sideways moves, bounds) and the sparsity of the band's problem."""
import heapq
import math

import numpy as np
from trajkit import A_MAX, GOAL, L_AXLE, R_BODY, START, TABLE, V_WHEEL

# ---------------------------------------------------------------- the room, the person, the global plan
ROOM_W, ROOM_H, DOOR = 7.0, 4.0, (3.0, 4.2)
CAB = [(5.6, 7.0, 3.4, 4.0), (6.4, 7.0, 2.4, 4.0)]
POLES = [(1.0, 3.0), (6.0, 0.8)]
POLE_R = 0.1
WALLS = [((0, 0), (ROOM_W, 0)), ((ROOM_W, 0), (ROOM_W, ROOM_H)), ((0, ROOM_H), (0, 0)),
         ((0, ROOM_H), (DOOR[0], ROOM_H)), ((DOOR[1], ROOM_H), (ROOM_W, ROOM_H))]
ROUTE = np.array([(2.25, 1.25), (2.75, 1.75), (2.75, 2.25), (2.75, 2.75), (2.75, 3.25), (3.25, 3.75),
                  (3.75, 3.75)])                       # RO-034's A* route, cell centres, 3.414 m
SEG = np.hypot(*np.diff(ROUTE, axis=0).T)
S_ROUTE = np.concatenate([[0], np.cumsum(SEG)])
PERSON_R = 0.2
PERSON = np.array([2.90, 2.75])                        # the person the map does not have: a disk, centre and radius
T_PERSON = 2.4                                         # when the person steps onto the route, s

# ---------------------------------------------------------------- TEB's settings (cfg defaults) and our robot's
DT_REF, DT_HYST, MIN_SAMPLES = 0.3, 0.1, 3
LOOKAHEAD = 1.5                                        # m of global plan (Roesmann et al. 2021 benchmark)
CYCLE = 0.1                                            # s: 10 Hz
EPS = 0.05                                             # penalty_epsilon
MIN_OBST = 0.1                                         # min_obstacle_dist, gap from the disk's edge, m
W_TIME, W_NH, W_OBST, W_VEL, W_ACC, W_FWD = 1.0, 1000.0, 50.0, 2.0, 1.0, 1.0
OUTER, INNER, ADAPT = 4, 5, 2.0


def _seg_dist(px, py, a, b):
    ax, ay = a
    ex, ey = b[0] - a[0], b[1] - a[1]
    t = np.clip(((px - ax) * ex + (py - ay) * ey) / (ex * ex + ey * ey), 0, 1)
    return np.hypot(px - ax - t * ex, py - ay - t * ey)


def poly_dist(px, py, P):
    """Signed distance from points to a convex polygon given counter-clockwise: positive outside."""
    best = np.full(np.shape(px), np.inf)
    inside = np.ones(np.shape(px), bool)
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        best = np.minimum(best, _seg_dist(px, py, a, b))
        inside &= ((b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0])) >= 0
    return np.where(inside, -best, best)


def obstacles(person=None):
    """Distance functions of every obstacle: table, cabinet, poles, walls, and the person if given."""
    obs = [lambda x, y: poly_dist(x, y, TABLE)]
    for x0, x1, y0, y1 in CAB:
        R = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
        obs.append(lambda x, y, R=R: poly_dist(x, y, R))
    for c in POLES:
        obs.append(lambda x, y, c=c: np.hypot(x - c[0], y - c[1]) - POLE_R)
    for a, b in WALLS:
        obs.append(lambda x, y, a=a, b=b: _seg_dist(x, y, a, b))
    if person is not None:
        obs.append(lambda x, y: np.hypot(x - person[0], y - person[1]) - PERSON_R)
    return obs


def gap(px, py, person=None):
    """Distance from the robot disk's edge to the nearest obstacle (negative: overlap)."""
    return np.min([o(np.asarray(px, float), np.asarray(py, float)) for o in obstacles(person)], axis=0) - R_BODY


# ---------------------------------------------------------------- the band's cost
def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def band_terms(P, DT, v0, stop_at_end):
    """Speeds, turn rates and accelerations of a band by finite differences (TEB's edges)."""
    d = np.diff(P[..., :2], axis=-2)
    dist = np.hypot(d[..., 0], d[..., 1])
    proj = d[..., 0] * np.cos(P[..., :-1, 2]) + d[..., 1] * np.sin(P[..., :-1, 2])
    sgn = np.sign(proj)                                # forward or backward (TEB's code smooths this sign)
    v = dist / DT * sgn
    w = wrap(np.diff(P[..., 2], axis=-1)) / DT
    a_mid = 2 * np.diff(v, axis=-1) / (DT[..., :-1] + DT[..., 1:])
    a_start = (v[..., :1] - v0) / DT[..., :1]
    acc = [a_start, a_mid]
    if stop_at_end:
        acc.append((0 - v[..., -1:]) / DT[..., -1:])
    return v, w, np.concatenate(acc, axis=-1), d, proj


def residuals(P, DT, v0, stop_at_end, obs, w_obst=W_OBST):
    """Every residual of TEB's least-squares cost for a batch of bands: P (B, n, 3), DT (B, n - 1)."""
    v, w, acc, d, proj = band_terms(P, DT, v0, stop_at_end)
    c0, s0, c1, s1 = np.cos(P[..., :-1, 2]), np.sin(P[..., :-1, 2]), np.cos(P[..., 1:, 2]), np.sin(P[..., 1:, 2])
    nh = (c0 + c1) * d[..., 1] - (s0 + s1) * d[..., 0]
    fwd = np.maximum(0, -proj)
    wr, wl = v + w * L_AXLE / 2, v - w * L_AXLE / 2
    pen = lambda x, lim: np.maximum(0, np.abs(x) - (lim - EPS))
    Pi = np.concatenate([P[..., 1:-1, :2], (P[..., 1:, :2] + P[..., :-1, :2]) / 2], axis=-2)  # poses, halfway points
    ob = [np.maximum(0, (MIN_OBST + EPS) - (o(Pi[..., 0], Pi[..., 1]) - R_BODY)) for o in obs]
    return np.concatenate([np.sqrt(W_TIME) * DT, np.sqrt(W_NH) * nh, np.sqrt(W_FWD) * fwd,
                           np.sqrt(W_VEL) * pen(wr, V_WHEEL), np.sqrt(W_VEL) * pen(wl, V_WHEEL),
                           np.sqrt(W_ACC) * pen(acc, A_MAX)] + [np.sqrt(w_obst) * x for x in ob], axis=-1)


def cost(P, DT, v0, stop_at_end, obs, w_obst=W_OBST):
    return float(np.sum(residuals(P[None], DT[None], v0, stop_at_end, obs, w_obst) ** 2))


def _pack(P, DT):
    return np.concatenate([P[1:-1].ravel(), DT])


def _unpack(Z, P):
    """Z (B, 3 (n - 2) + n - 1) -> P (B, n, 3), DT (B, n - 1), with the fixed first and last poses of P."""
    n = len(P)
    B = len(Z)
    Pb = np.broadcast_to(P, (B, n, 3)).copy()
    Pb[:, 1:-1] = Z[:, :3 * (n - 2)].reshape(B, n - 2, 3)
    return Pb, Z[:, 3 * (n - 2):]


def lm(P, DT, v0, stop_at_end, obs, iters, w_obst, hist=None, mu=1e-2):
    """Levenberg-Marquardt on the band (the steps g2o takes): solve (J^T J + mu diag) step = -J^T r, keep the step
    if the cost falls (mu / 3), else retry with mu x 4. Jacobian by central differences, all variables at once.
    dT is kept at 0.01 s or more."""
    z = _pack(P, DT)
    m = len(z)

    def res(Z):
        Pb, Db = _unpack(Z, P)
        return residuals(Pb, Db, v0, stop_at_end, obs, w_obst)

    r = res(z[None])[0]
    c = float(r @ r)
    for _ in range(iters):
        e = 1e-6
        Zp = np.vstack([z + e * np.eye(m), z - e * np.eye(m)])
        F = res(Zp)
        J = ((F[:m] - F[m:]) / (2 * e)).T
        H, g = J.T @ J, J.T @ r
        for _try in range(20):
            step = -np.linalg.solve(H + mu * np.diag(np.diag(H) + 1e-9), g)
            zn = z + step
            zn[3 * (len(P) - 2):] = np.maximum(zn[3 * (len(P) - 2):], 0.01)
            rn = res(zn[None])[0]
            cn = float(rn @ rn)
            if cn < c:
                z, r, c = zn, rn, cn
                mu = max(mu / 3, 1e-9)
                break
            mu *= 4
        if hist is not None:
            Pb, Db = _unpack(z[None], P)
            hist.append((Pb[0].copy(), Db[0].copy(), c))
    Pb, Db = _unpack(z[None], P)
    return Pb[0], Db[0], c


def auto_resize(P, DT):
    """TEB's autoResize: split an interval longer than dt_ref + hysteresis (in half when longer than 2 dt_ref, else
    give the excess to the next), merge one shorter than dt_ref - hysteresis into its neighbour."""
    P, DT = [p.copy() for p in P], list(DT)
    for _rep in range(100):
        modified = False
        i = 0
        while i < len(DT):
            if DT[i] > DT_REF + DT_HYST:
                if DT[i] > 2 * DT_REF:
                    DT[i] /= 2
                    a, b = P[i], P[i + 1]
                    mid = np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, a[2] + wrap(b[2] - a[2]) / 2])
                    P.insert(i + 1, mid)
                    DT.insert(i + 1, DT[i])
                    modified = True
                    continue
                if i < len(DT) - 1:
                    DT[i + 1] += DT[i] - DT_REF
                DT[i] = DT_REF
            elif DT[i] < DT_REF - DT_HYST and len(DT) > MIN_SAMPLES:
                if i < len(DT) - 1:
                    DT[i + 1] += DT[i]
                    del DT[i]
                    del P[i + 1]
                else:
                    DT[i - 1] += DT[i]
                    del DT[i]
                    del P[i]
                modified = True
                continue
            i += 1
        if not modified:
            break
    return np.array(P), np.array(DT)


def optimise(P, DT, v0, stop_at_end, person, hist=None, outer=OUTER, inner=INNER):
    """TEB's optimizeTEB: outer passes of (resize, inner LM steps), the obstacle weight doubled after each pass."""
    obs = obstacles(person)
    w = W_OBST
    for _ in range(outer):
        P, DT = auto_resize(P, DT)
        if hist is not None:
            hist.append((P.copy(), DT.copy(), cost(P, DT, v0, stop_at_end, obs, w)))
        P, DT, c = lm(P, DT, v0, stop_at_end, obs, inner, w, hist)
        w *= ADAPT
    return P, DT, cost(P, DT, v0, stop_at_end, obs, W_OBST)


# ---------------------------------------------------------------- following the global plan
def route_point(s, route=ROUTE):
    seg = np.hypot(*np.diff(route, axis=0).T)
    S = np.concatenate([[0], np.cumsum(seg)])
    s = float(np.clip(s, 0, S[-1]))
    j = min(np.searchsorted(S, s, side="right") - 1, len(seg) - 1)
    u = (route[j + 1] - route[j]) / seg[j]
    return route[j] + (s - S[j]) * u, math.atan2(u[1], u[0])


def project(xy, route=ROUTE):
    """Arc length along the route of the point of the route nearest to xy."""
    seg = np.hypot(*np.diff(route, axis=0).T)
    S = np.concatenate([[0], np.cumsum(seg)])
    best, sb = np.inf, 0.0
    for j in range(len(seg)):
        a, b = route[j], route[j + 1]
        t = np.clip(np.dot(xy - a, b - a) / seg[j] ** 2, 0, 1)
        d = np.hypot(*(a + t * (b - a) - xy))
        if d < best:
            best, sb = d, S[j] + t * seg[j]
    return sb


def local_goal(xy, route=ROUTE):
    """The pose LOOKAHEAD m further along the route, facing along it; the door pose once the route ends within
    reach. Returns (pose, final)."""
    S = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(route, axis=0).T))])
    s = project(xy, route) + LOOKAHEAD
    if s >= S[-1]:
        return GOAL[:3].copy(), True
    p, th = route_point(s, route)
    return np.array([p[0], p[1], th]), False


def init_band(start, goal, route=ROUTE, step=0.1):
    """TEB's initTrajectoryToGoal: poses on the plan (here every 0.1 m, as on a fine costmap) between the start and
    the goal, facing along it, each dT the time at full speed; then the resize rule."""
    s0 = project(start[:2], route)
    s1 = project(goal[:2], route)
    pts = [np.array(start, float)]
    for s in np.arange(s0 + step, s1 - step / 2, step):
        p, th = route_point(s, route)
        pts.append(np.array([p[0], p[1], th]))
    pts.append(np.array(goal, float))
    P = np.array(pts)
    for k in range(1, len(P) - 1):
        d = P[k + 1, :2] - P[k - 1, :2]
        P[k, 2] = math.atan2(d[1], d[0])
    DT = np.maximum(np.hypot(*np.diff(P[:, :2], axis=0).T) / V_WHEEL, 0.02)
    return auto_resize(P, DT)


# ---------------------------------------------------------------- A* on the 0.5 m grid of RO-034: the global plan
CELL = 0.5


def blocked_cells():
    from shapely.geometry import Point, Polygon, box as sbox
    from shapely.ops import unary_union
    parts = [Polygon(TABLE)] + [sbox(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB] + \
            [Point(p).buffer(POLE_R, quad_segs=64) for p in POLES]
    u = unary_union(parts)
    nx, ny = int(ROOM_W / CELL), int(ROOM_H / CELL)
    return {(i, j) for i in range(nx) for j in range(ny)
            if sbox(i * CELL, j * CELL, (i + 1) * CELL, (j + 1) * CELL).intersection(u).area > 0}


def astar(start=(4, 2), goal=(7, 7)):
    """A* with the octile heuristic, 8 neighbours, no cutting the corner of a blocked cell. Returns cell centres."""
    B = blocked_cells()
    nx, ny = int(ROOM_W / CELL), int(ROOM_H / CELL)
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
    cells = path[::-1]
    return np.array([((i + 0.5) * CELL, (j + 0.5) * CELL) for i, j in cells]), g[goal]


def astar_fine(a, b, person=None, cell=0.1):
    """A* on a local costmap of `cell` m cells: a cell is blocked when the disk centred there would overlap an
    obstacle. 8 neighbours, no corner cutting, octile heuristic. Returns the route from a to b (cell centres between,
    the exact a and b at the ends) and its length."""
    nx, ny = int(round(ROOM_W / cell)), int(round(ROOM_H / cell))
    cx, cy = np.meshgrid((np.arange(nx) + 0.5) * cell, (np.arange(ny) + 0.5) * cell, indexing="ij")
    blocked = gap(cx, cy, person) < 0
    s = (int(a[0] // cell), int(a[1] // cell))
    t = (int(b[0] // cell), int(b[1] // cell))
    free = lambda c: 0 <= c[0] < nx and 0 <= c[1] < ny and not blocked[c]
    d2 = math.sqrt(2) * cell
    h = lambda c: d2 * min(abs(c[0] - t[0]), abs(c[1] - t[1])) + cell * abs(abs(c[0] - t[0]) - abs(c[1] - t[1]))
    g, came, openl, closed = {s: 0.0}, {}, [(h(s), h(s), s)], set()
    while openl:
        _, _, c = heapq.heappop(openl)
        if c in closed:
            continue
        if c == t:
            break
        closed.add(c)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (c[0] + dx, c[1] + dy)
                if (dx, dy) == (0, 0) or not free(n):
                    continue
                if dx and dy and not (free((c[0] + dx, c[1])) and free((c[0], c[1] + dy))):
                    continue
                gn = g[c] + (d2 if dx and dy else cell)
                if gn < g.get(n, np.inf) - 1e-12:
                    g[n], came[n] = gn, c
                    heapq.heappush(openl, (gn + h(n), h(n), n))
    path = [t]
    while path[-1] != s:
        path.append(came[path[-1]])
    pts = np.array([((i + 0.5) * cell, (j + 0.5) * cell) for i, j in path[::-1]])
    pts[0], pts[-1] = a[:2], b[:2]
    return pts, float(np.sum(np.hypot(*np.diff(pts, axis=0).T))), len(closed)


# ---------------------------------------------------------------- the receding-horizon loop
def run_loop(person=PERSON, t_person=T_PERSON, t_end=12.0, keep_iters=False):
    """Every CYCLE s: measure the robot, move the band's first pose to it and drop the poses it has passed (TEB's
    warm start), set the last pose to the new local goal, optimise, and drive the first piece of the band for one
    cycle. The robot's speed follows the command within 0.5 m/s^2. Returns a list of cycle records."""
    x = np.array(START[:3], float)
    v = 0.0
    goal, final = local_goal(x[:2])
    P, DT = init_band(x, goal)
    out = []
    t = 0.0
    while t < t_end:
        seen = person if t >= t_person - 1e-9 else None
        goal, final = local_goal(x[:2])
        # warm start: prune the passed poses, overwrite the first and the last
        n = len(P)
        look = min(n - MIN_SAMPLES, 10)
        k_near = 0
        dbest = np.hypot(*(P[0, :2] - x[:2]))
        for i in range(1, look + 1):
            di = np.hypot(*(P[i, :2] - x[:2]))
            if di < dbest:
                dbest, k_near = di, i
            else:
                break
        if k_near > 0:
            P = np.delete(P, range(1, k_near + 1), axis=0)
            DT = np.delete(DT, range(1, k_near + 1))
        P[0] = x
        P[-1] = goal
        warm = (P.copy(), DT.copy())
        hist = [] if keep_iters else None
        P, DT, c = optimise(P, DT, v, final, seen, hist)
        vv, ww, acc, _, _ = band_terms(P, DT, v, final)
        v_cmd, w_cmd = float(vv[0]), float(ww[0])
        out.append(dict(t=t, x=x.copy(), v=v, person=seen, goal=goal, final=final, warm=warm, P=P.copy(),
                        DT=DT.copy(), cost=c, cmd=(v_cmd, w_cmd), hist=hist))
        if final and np.hypot(*(x[:2] - GOAL[:2])) < 0.02 and abs(v) < 0.02 and abs(wrap(x[2] - GOAL[2])) < 0.05:
            break
        # drive the band's first CYCLE seconds: each piece's speed and turn rate in turn, the speed changing by at
        # most 0.5 m/s^2, never below 0, and both wheels kept within 0.6 m/s
        T_band = np.concatenate([[0], np.cumsum(DT)])
        h = CYCLE / 20
        for j in range(20):
            tm = (j + 0.5) * h
            i = min(np.searchsorted(T_band, tm, side="right") - 1, len(DT) - 1)
            v_c, w_c = (float(vv[i]), float(ww[i])) if tm < T_band[-1] else (0.0, 0.0)
            v_new = float(np.clip(v + np.clip(v_c - v, -A_MAX * h, A_MAX * h), 0.0, V_WHEEL))   # forward only
            lim = (V_WHEEL - abs(v_new)) / (L_AXLE / 2)
            w_new = float(np.clip(w_c, -lim, lim))
            x = x + h * np.array([v_new * math.cos(x[2] + w_new * h / 2), v_new * math.sin(x[2] + w_new * h / 2),
                                  w_new])
            v = v_new
        t = round(t + CYCLE, 10)
    return out


# ---------------------------------------------------------------- the elastic-band smoother (Autoware's path smoother)
W_SMOOTH, W_LAT, CLEAR = 1.0, 0.001, 0.1               # smooth_weight, lat_error_weight, clearance_for_smooth (m)


def normals(p):
    """Sideways direction at every interior point: at right angles to the line through its two neighbours."""
    c = p[2:] - p[:-2]
    c = c / np.hypot(c[:, 0], c[:, 1])[:, None]
    return np.stack([-c[:, 1], c[:, 0]], axis=1)


def smooth_system(p, w_s=W_SMOOTH, w_e=W_LAT):
    """The smoothing cost as linear least squares in the sideways moves d of the interior points:
    cost = |A d + b|^2 = w_s sum |p_(k-1) - 2 p_k + p_(k+1)|^2 + w_e sum d_k^2, with p_k = p0_k + d_k n_k."""
    m = len(p)
    n = normals(p)
    rows, b = [], []
    for k in range(1, m - 1):                           # second difference at point k, x then y
        for ax in range(2):
            row = np.zeros(m - 2)
            for j, c in ((k - 1, 1.0), (k, -2.0), (k + 1, 1.0)):
                if 1 <= j <= m - 2:
                    row[j - 1] += c * n[j - 1, ax]
            rows.append(np.sqrt(w_s) * row)
            b.append(np.sqrt(w_s) * (p[k - 1, ax] - 2 * p[k, ax] + p[k + 1, ax]))
    rows += list(np.sqrt(w_e) * np.eye(m - 2))
    b += [0.0] * (m - 2)
    return np.array(rows), np.array(b), n


def smooth(p, clear=CLEAR, iters=400):
    """Projected gradient steps on the smoothing cost: step downhill, then clip every move to [-clear, clear].
    Returns the moves after every step and the exact answer of the bounded problem (SciPy's lsq_linear)."""
    from scipy.optimize import lsq_linear
    A, b, n = smooth_system(p)
    step = 1 / (2 * np.linalg.eigvalsh(A.T @ A).max())
    d = np.zeros(A.shape[1])
    hist = [d.copy()]
    for _ in range(iters):
        d = np.clip(d - step * 2 * A.T @ (A @ d + b), -clear, clear)
        hist.append(d.copy())
    exact = lsq_linear(A, -b, bounds=(-clear, clear), tol=1e-12).x
    return dict(hist=hist, exact=exact, n=n, A=A, b=b, step=step,
                cost=lambda d: float(np.sum((A @ d + b) ** 2)), pts=lambda d: np.vstack(
                    [p[0], p[1:-1] + d[:, None] * n, p[-1]]))


# ---------------------------------------------------------------- sparsity of the band's least-squares problem
def sparsity(n):
    """Which entries of J^T J are non-zero for a band of n poses (first and last fixed), with the free variables in
    TEB's order dT_1, s_2, dT_2, s_3, ..., s_(n-1), dT_(n-1). Returns the boolean pattern and the variable names."""
    names, idx = [], {}
    for k in range(1, n):
        if k >= 2:
            for c in "xyt":
                idx[(c, k)] = len(names)
                names.append(f"{c}{k}")
        idx[("T", k)] = len(names)
        names.append(f"T{k}")
    pose = lambda k: [idx[(c, k)] for c in "xyt"] if 2 <= k <= n - 1 else []
    edges = []
    for k in range(1, n):                               # time, non-holonomic, speed: poses k, k+1 and dT_k
        edges.append(pose(k) + pose(k + 1) + [idx[("T", k)]])
    for k in range(1, n - 1):                           # acceleration: poses k, k+1, k+2 and dT_k, dT_(k+1)
        edges.append(pose(k) + pose(k + 1) + pose(k + 2) + [idx[("T", k)], idx[("T", k + 1)]])
    for k in range(2, n):                               # obstacles: one pose (and the halfway points)
        edges.append(pose(k))
    m = len(names)
    M = np.zeros((m, m), bool)
    for e in edges:
        for a in e:
            for b in e:
                M[a, b] = True
    return M, names


# ---------------------------------------------------------------- every run the Note quotes, computed once
PERSON_LEFT = PERSON - np.array([0.25, 0.0])           # the same person 0.25 m further left (local minimum)


def results():
    """All runs the figures and the notebook use (cached by this file's and trajkit's text)."""
    import hashlib
    import pickle
    import tempfile
    from pathlib import Path
    here = Path(__file__).parent
    key = hashlib.sha1(Path(__file__).read_bytes() + (here / "trajkit.py").read_bytes()).hexdigest()[:12]
    f = Path(tempfile.gettempdir()) / "ro058_cache" / f"band_{key}.pkl"
    if f.exists():
        R = pickle.loads(f.read_bytes())
        R["smooth"] = smooth(ROUTE)                     # holds functions, so it is not stored
        return R
    R = {}
    R["loop"] = run_loop(keep_iters=True)
    R["free"] = run_loop(person=None)
    k = int(round(T_PERSON / CYCLE))
    c = R["free"][k]                                    # the cycle the person appears in, as if there were none
    Pw, Dw = c["warm"]
    hist_w = []
    Pw2, Dw2, cw = optimise(Pw.copy(), Dw.copy(), c["v"], c["final"], PERSON_LEFT, hist_w)
    route, L, nexp = astar_fine(c["x"], c["goal"], PERSON_LEFT)
    Pa, Da = init_band(c["x"], c["goal"], route=route)
    hist_a = []
    Pa2, Da2, ca = optimise(Pa.copy(), Da.copy(), c["v"], c["final"], PERSON_LEFT, hist_a)
    R["wrong"] = dict(cycle=c, warm=(Pw, Dw), hist_w=hist_w, res_w=(Pw2, Dw2, cw), route=route, route_len=L,
                      expanded=nexp, init_a=(Pa, Da), hist_a=hist_a, res_a=(Pa2, Da2, ca))
    R["smooth"] = smooth(ROUTE)
    f.parent.mkdir(exist_ok=True)
    f.write_bytes(pickle.dumps({k: v for k, v in R.items() if k != "smooth"}))
    return R
