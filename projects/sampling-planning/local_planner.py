"""From a path to a drive (RO-058): the elastic band, the timed elastic band (TEB) as a local planner on a receding
horizon, and direct collocation of a whole drive, solved once.

The robot is the one of RO-058: a differential drive, wheels 0.2 m apart, each wheel at most 0.6 m/s, its forward
speed changing by at most 0.5 m/s every second, and a disk whose radius is the world's robot_radius (0.25 m, as in
RO-058). State (x, y, heading theta, speed v), controls (acceleration a, turn rate omega):
x' = v cos theta, y' = v sin theta, theta' = omega, v' = a.

Map interface: only a Space (collision.py). Clearance(space) measures the gap from the robot's disk to the nearest
obstacle or wall from space.free_region; grid_route rasterises the same test and searches it with the grid
project's A*; elastic_band only needs a vectorised free test, so a street map can pass its own."""
import math
import sys
from pathlib import Path

import numpy as np
import shapely
from scipy.optimize import least_squares, lsq_linear, minimize
from threadpoolctl import threadpool_limits

sys.path.append(str(Path(__file__).resolve().parents[1] / "grid-pathfinding"))
from algorithms import a_star  # noqa: E402  (projects/grid-pathfinding)
from grid import Grid  # noqa: E402
from potential import path_length  # noqa: E402

threadpool_limits(1)  # one BLAS thread: faster on these small matrices, and the solvers take the same steps anywhere

# ---------------------------------------------------------------- the robot of RO-058
L_AXLE, V_WHEEL, A_MAX = 0.2, 0.6, 0.5         # wheel separation (m), wheel limit (m/s), acceleration limit (m/s^2)
W_SPIN = 2 * V_WHEEL / L_AXLE                   # turn rate on the spot: 6 rad/s


def wheels(v, w):
    return v + w * L_AXLE / 2, v - w * L_AXLE / 2


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


class Clearance:
    """clear(x, y, persons): the gap (m) between the robot's disk centred at (x, y) and the nearest obstacle, wall
    or person, negative on overlap. persons: [(x, y, radius)], disks the map does not have. Arrays allowed."""

    def __init__(self, space):
        self.region, self.edge, self.r = space.free_region, space.free_region.boundary, space.radius
        shapely.prepare(self.region)
        shapely.prepare(self.edge)

    def __call__(self, x, y, persons=()):
        x, y = np.asarray(x, float), np.asarray(y, float)
        xs, ys = x.ravel(), y.ravel()
        d = shapely.distance(self.edge, shapely.points(xs, ys))
        d = np.where(shapely.contains_xy(self.region, xs, ys), d, -d).reshape(x.shape) - self.r
        for px, py, pr in persons:
            d = np.minimum(d, np.hypot(x - px, y - py) - pr - self.r)
        return d


def corners_only(P):
    """The route's points where it turns (and its two ends): points on a straight piece dropped."""
    P = np.asarray(P, float)
    keep = [0]
    for k in range(1, len(P) - 1):
        a, b = P[k] - P[keep[-1]], P[k + 1] - P[k]
        if abs(a[0] * b[1] - a[1] * b[0]) > 1e-9 or a @ b < 0:
            keep.append(k)
    return P[keep + [len(P) - 1]]


# ---------------------------------------------------------------- A* on a grid made from the world
def grid_route(space, a, b, cell=0.25, persons=(), window=None, clear=None):
    """A* (the grid project's own: 8 neighbours, no cutting a corner) on cells of `cell` m. A cell is free when the
    robot's disk centred on it touches nothing (persons included). window (x0, y0, x1, y1): search only there, a
    local costmap. Returns (the route's points, a and b at the ends; its length; cells expanded)."""
    clear = clear or Clearance(space)
    x0, y0, x1, y1 = window or space.bounds
    cols, rows = int(round((x1 - x0) / cell)), int(round((y1 - y0) / cell))
    origin = (x0 + cell / 2, y0 + cell / 2)
    X, Y = np.meshgrid(origin[0] + np.arange(cols) * cell, origin[1] + (rows - 1 - np.arange(rows)) * cell)
    g = Grid(clear(X, Y, persons) >= 0, cell, origin=origin)
    at = lambda p: (int(round((p[0] - origin[0]) / cell)), rows - 1 - int(round((p[1] - origin[1]) / cell)))
    r = a_star(g, at(a), at(b))
    pts = np.array([g.xy(n) for n in r.route])
    pts[0], pts[-1] = a[:2], b[:2]
    return pts, path_length(pts), r.visited


# ---------------------------------------------------------------- the elastic band (RO-058 section 4)
def resample(P, spacing):
    """Points evenly spaced along the polyline P, about `spacing` apart, both ends kept."""
    S = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
    s = np.linspace(0, S[-1], max(2, int(round(S[-1] / spacing))) + 1)
    return np.stack([np.interp(s, S, P[:, 0]), np.interp(s, S, P[:, 1])], axis=1)


def normals(P):
    """Sideways direction at every inner point: at right angles to the line through its two neighbours."""
    c = P[2:] - P[:-2]
    c /= np.hypot(c[:, 0], c[:, 1])[:, None]
    return np.stack([-c[:, 1], c[:, 0]], axis=1)


def room(P, n, ok, cap, step=0.01):
    """How far each inner point may move along +n and along -n (at most cap) with ok() true all the way."""
    ts = np.arange(step, cap + step / 2, step)
    out = []
    for sign in (1, -1):
        X = P[1:-1, None, 0] + sign * ts * n[:, None, 0]
        Y = P[1:-1, None, 1] + sign * ts * n[:, None, 1]
        free = np.concatenate([ok(X, Y), np.zeros((len(P) - 2, 1), bool)], axis=1)  # a sentinel: stop at the end
        out.append(ts[np.argmin(free, axis=1) - 1] * (np.argmin(free, axis=1) > 0))
    return out[0], out[1]


def elastic_band(P, ok, spacing=0.2, cap=0.3, w_len=0.1, passes=100, tol=1e-3):
    """Smooth and shorten the path P (points) as one optimisation, solved again and again (RO-058 section 4).
    Each pass: resample the band evenly, about `spacing` m apart; find each inner point's sideways direction and how
    far it may move each way with ok(x, y) true (at most `cap`); then move every inner point sideways at once to
    make the sum of squared second differences (smooth) plus w_len times the sum of squared first differences
    (short, Apollo's length term) as small as possible within those bounds: a quadratic program, solved exactly by
    SciPy's lsq_linear. The two ends stay fixed. Stops when no point moves more than tol. Returns
    [(band, lower bounds, upper bounds, moves)], one per pass, and the final band."""
    P = resample(np.asarray(P, float), spacing)
    hist = []
    for _ in range(passes):
        m, n = len(P), normals(P)
        hi, lo = room(P, n, ok, cap)
        rows, rhs = [], []
        for k in range(1, m - 1):  # second difference p(k-1) - 2 p(k) + p(k+1), with p(j) = P(j) + d(j) n(j)
            for ax in range(2):
                row = np.zeros(m - 2)
                for j, c in ((k - 1, 1.0), (k, -2.0), (k + 1, 1.0)):
                    if 1 <= j <= m - 2:
                        row[j - 1] += c * n[j - 1, ax]
                rows.append(row)
                rhs.append(P[k - 1, ax] - 2 * P[k, ax] + P[k + 1, ax])
        for k in range(m - 1):  # first difference p(k+1) - p(k), the length of a piece
            for ax in range(2):
                row = np.zeros(m - 2)
                for j, c in ((k, -1.0), (k + 1, 1.0)):
                    if 1 <= j <= m - 2:
                        row[j - 1] += c * n[j - 1, ax]
                rows.append(math.sqrt(w_len) * row)
                rhs.append(math.sqrt(w_len) * (P[k + 1, ax] - P[k, ax]))
        d = lsq_linear(np.array(rows), -np.array(rhs), bounds=(-lo, hi + 1e-12)).x
        hist.append((P, -lo, hi, d))
        P = P.copy()
        P[1:-1] += d[:, None] * n
        if np.abs(d).max() < tol:
            break
        P = resample(P, spacing)
    return hist, P


# ---------------------------------------------------------------- the timed elastic band (RO-058 sections 5 and 8)
# TEB's default settings (teb_local_planner), as RO-058 uses them; our robot's wheel limit replaces TEB's separate
# speed and turn-rate limits
DT_REF, DT_HYST, MIN_SAMPLES = 0.3, 0.1, 3      # poses about 0.3 s apart
LOOKAHEAD, CYCLE = 1.5, 0.1                      # m of global plan in the window; s between solves (10 Hz)
EPS, MIN_OBST = 0.05, 0.1                        # penalty margin; gap kept from the disk's edge (m)
W_TIME, W_NH, W_OBST, W_VEL, W_ACC, W_FWD = 1.0, 1000.0, 50.0, 2.0, 1.0, 1.0
OUTER, INNER, ADAPT = 4, 5, 2.0                  # 4 passes of 5 solver steps; obstacle weight doubled after each
GOAL_XY = 0.05                                   # m: at the goal when this close and stopped (TEB's default: 0.2)


class Person:
    """A disk the map does not have. It steps out at time t0 from p0, walks at `speed` m/s to p1 and stands there.
    at(t): (x, y, radius), or None before t0."""

    def __init__(self, p0, p1, t0, speed=1.0, radius=0.2):
        self.p0, self.p1, self.t0, self.speed, self.radius = np.array(p0, float), np.array(p1, float), t0, speed, radius

    def at(self, t):
        if t < self.t0 - 1e-9:
            return None
        d = np.hypot(*(self.p1 - self.p0))
        u = min(1.0, (t - self.t0) * self.speed / d) if d else 1.0
        x, y = self.p0 + u * (self.p1 - self.p0)
        return (x, y, self.radius)


def band_terms(P, DT, v0, stop_at_end):
    """Speeds, turn rates and accelerations of a band by differences between neighbours (RO-058 section 5.1)."""
    d = np.diff(P[..., :2], axis=-2)
    proj = d[..., 0] * np.cos(P[..., :-1, 2]) + d[..., 1] * np.sin(P[..., :-1, 2])
    v = np.hypot(d[..., 0], d[..., 1]) / DT * np.sign(proj)
    w = wrap(np.diff(P[..., 2], axis=-1)) / DT
    acc = [(v[..., :1] - v0) / DT[..., :1], 2 * np.diff(v, axis=-1) / (DT[..., :-1] + DT[..., 1:])]
    if stop_at_end:
        acc.append((0 - v[..., -1:]) / DT[..., -1:])
    return v, w, np.concatenate(acc, axis=-1), d, proj


def residuals(P, DT, v0, stop_at_end, clear, persons, w_obst=W_OBST):
    """Every term of TEB's cost, square-rooted, for a batch of bands P (B, n, 3), DT (B, n - 1): the time steps,
    the arc rule, driving backwards, both wheels, the acceleration and the clearance (at every pose and halfway)."""
    v, w, acc, d, proj = band_terms(P, DT, v0, stop_at_end)
    c0, s0, c1, s1 = np.cos(P[..., :-1, 2]), np.sin(P[..., :-1, 2]), np.cos(P[..., 1:, 2]), np.sin(P[..., 1:, 2])
    arc = (c0 + c1) * d[..., 1] - (s0 + s1) * d[..., 0]
    wr, wl = wheels(v, w)
    over = lambda x, lim: np.maximum(0, np.abs(x) - (lim - EPS))
    Q = np.concatenate([P[..., 1:-1, :2], (P[..., 1:, :2] + P[..., :-1, :2]) / 2], axis=-2)
    near = np.maximum(0, (MIN_OBST + EPS) - clear(Q[..., 0], Q[..., 1], persons))
    return np.concatenate([math.sqrt(W_TIME) * DT, math.sqrt(W_NH) * arc, math.sqrt(W_FWD) * np.maximum(0, -proj),
                           math.sqrt(W_VEL) * over(wr, V_WHEEL), math.sqrt(W_VEL) * over(wl, V_WHEEL),
                           math.sqrt(W_ACC) * over(acc, A_MAX), math.sqrt(w_obst) * near], axis=-1)


def band_cost(P, DT, v0, stop_at_end, clear, persons):
    """TEB's cost with its set weights: sum of the squared terms."""
    return float(np.sum(residuals(P[None], DT[None], v0, stop_at_end, clear, persons) ** 2))


def fd_jac(batch, z, e=1e-6):
    """Jacobian by central differences, every variable moved at once in one batch."""
    Z = np.vstack([z + e * np.eye(len(z)), z - e * np.eye(len(z))])
    F = batch(Z)
    return ((F[:len(z)] - F[len(z):]) / (2 * e)).T


def auto_resize(P, DT):
    """TEB's autoResize: split a step longer than 2 dt_ref in two; trim one longer than dt_ref + hysteresis to dt_ref
    and give the rest to the next; remove a pose where a step is shorter than dt_ref - hysteresis."""
    P, DT = [p.copy() for p in P], list(DT)
    for _ in range(100):
        changed, i = False, 0
        while i < len(DT):
            if DT[i] > DT_REF + DT_HYST:
                if DT[i] > 2 * DT_REF:
                    DT[i] /= 2
                    a, b = P[i], P[i + 1]
                    P.insert(i + 1, np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, a[2] + wrap(b[2] - a[2]) / 2]))
                    DT.insert(i + 1, DT[i])
                    changed = True
                    continue
                if i < len(DT) - 1:
                    DT[i + 1] += DT[i] - DT_REF
                DT[i] = DT_REF
            elif DT[i] < DT_REF - DT_HYST and len(DT) > MIN_SAMPLES:
                if i < len(DT) - 1:
                    DT[i + 1] += DT[i]
                    del DT[i], P[i + 1]
                else:
                    DT[i - 1] += DT[i]
                    del DT[i], P[i]
                changed = True
                continue
            i += 1
        if not changed:
            break
    return np.array(P), np.array(DT)


def solve_band(P, DT, v0, stop_at_end, clear, persons, hist=None):
    """TEB's optimizeTEB: 4 passes, each resizing the band and taking 5 steps of SciPy's least-squares solver (a
    Gauss-Newton trust-region method, a cousin of TEB's Levenberg-Marquardt), the clearance weight doubled after each
    pass. The first and last poses stay fixed; every time step stays at least 0.01 s. hist: list to collect
    (P, DT, cost with the set weights) after every step."""
    w = W_OBST
    for _ in range(OUTER):
        P, DT = auto_resize(P, DT)
        n = len(P)

        def unpack(Z):
            Pb = np.broadcast_to(P, (len(Z), n, 3)).copy()
            Pb[:, 1:-1] = Z[:, :3 * (n - 2)].reshape(len(Z), n - 2, 3)
            return Pb, Z[:, 3 * (n - 2):]

        def batch(Z):
            return residuals(*unpack(Z), v0, stop_at_end, clear, persons, w)

        def keep(z):  # SciPy calls it with the variables after each step
            Pb, Db = unpack(z[None])
            hist.append((Pb[0], Db[0], band_cost(Pb[0], Db[0], v0, stop_at_end, clear, persons)))

        if hist is not None:
            hist.append((P, DT, band_cost(P, DT, v0, stop_at_end, clear, persons)))
        lo = np.concatenate([np.full(3 * (n - 2), -np.inf), np.full(n - 1, 0.01)])
        z0 = np.maximum(np.concatenate([P[1:-1].ravel(), DT]), lo + 1e-9)
        r = least_squares(lambda z: batch(z[None])[0], z0, jac=lambda z: fd_jac(batch, z), bounds=(lo, np.inf),
                          method="trf", max_nfev=INNER, callback=keep if hist is not None else None)
        Pb, Db = unpack(r.x[None])
        P, DT = Pb[0], Db[0]
        w *= ADAPT
    return P, DT, band_cost(P, DT, v0, stop_at_end, clear, persons)


# ---------------------------------------------------------------- following the global plan
class Route:
    """The global plan as a polyline with arc length; the robot's place on it only moves forward."""

    def __init__(self, pts):
        self.pts = np.asarray(pts, float)
        self.S = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(self.pts, axis=0).T))])
        self.length = self.S[-1]

    def point(self, s):
        """The point at arc length s and the heading of the route there."""
        s = float(np.clip(s, 0, self.length))
        j = min(np.searchsorted(self.S, s, side="right") - 1, len(self.pts) - 2)
        u = (self.pts[j + 1] - self.pts[j]) / (self.S[j + 1] - self.S[j])
        return self.pts[j] + (s - self.S[j]) * u, math.atan2(u[1], u[0])

    def project(self, xy, s_from=0.0, ahead=2.0):
        """Arc length of the route's point nearest to xy, looked for between s_from - 0.3 m and s_from + ahead."""
        best, sb = np.inf, s_from
        for j in range(len(self.pts) - 1):
            if self.S[j + 1] < s_from - 0.3 or self.S[j] > s_from + ahead:
                continue
            a, b = self.pts[j], self.pts[j + 1]
            t = np.clip(np.dot(xy - a, b - a) / np.dot(b - a, b - a), 0, 1)
            d = np.hypot(*(a + t * (b - a) - xy))
            if d < best:
                best, sb = d, self.S[j] + t * (self.S[j + 1] - self.S[j])
        return sb


def init_band(route, start, goal, step=0.1):
    """TEB's first band: poses on the plan every 0.1 m from the start to the goal, facing along it, each time step
    the time at full speed; then the resize rule."""
    s0, s1 = route.project(start[:2]), route.project(goal[:2], 0.0, route.length)
    pts = [np.array(start, float)]
    for s in np.arange(s0 + step, s1 - step / 2, step):
        p, th = route.point(s)
        pts.append(np.array([p[0], p[1], th]))
    pts.append(np.array(goal, float))
    P = np.array(pts)
    for k in range(1, len(P) - 1):
        d = P[k + 1, :2] - P[k - 1, :2]
        P[k, 2] = math.atan2(d[1], d[0])
    return auto_resize(P, np.maximum(np.hypot(*np.diff(P[:, :2], axis=0).T) / V_WHEEL, 0.02))


def run_loop(space, route, start, goal, person=None, t_end=90.0, keep_steps=False, clear=None):
    """The receding-horizon loop (RO-058 section 8). Every 0.1 s: measure the robot; warm start: drop the poses it
    has passed, move the first pose to the robot and the last to the local goal, the route's pose 1.5 m ahead (the
    goal pose once the route ends within 1.5 m); optimise; drive the band's first 0.1 s, the robot keeping its own
    limits (wheels at most 0.6 m/s, speed changing at most 0.5 m/s per second, never backwards). Once stopped within
    GOAL_XY of the goal, the robot turns on the spot to the goal's heading and has arrived.
    route: a Route; start, goal: poses (x, y, heading). Returns (cycles, the driven states (t, x, y, heading, v) every
    5 ms, the last one at the arrival)."""
    clear = clear or Clearance(space)
    x, v, s_now = np.array(start, float), 0.0, 0.0
    goal = np.array(goal, float)
    P, DT = init_band(route, x, local_goal(route, 0.0, goal)[0])
    cycles, drive, t = [], [(0.0, *x, 0.0)], 0.0
    while t < t_end:
        persons = [p for p in [person.at(t) if person else None] if p]
        s_now = route.project(x[:2], s_now)
        lg, final = local_goal(route, s_now, goal)
        k_near, dbest = 0, np.hypot(*(P[0, :2] - x[:2]))  # TEB's pruning: drop poses the robot has passed
        for i in range(1, min(len(P) - MIN_SAMPLES, 10) + 1):
            di = np.hypot(*(P[i, :2] - x[:2]))
            if di >= dbest:
                break
            dbest, k_near = di, i
        if k_near:
            P, DT = np.delete(P, range(1, k_near + 1), axis=0), np.delete(DT, range(1, k_near + 1))
        P[0], P[-1] = x, lg
        warm = (P.copy(), DT.copy())
        hist = [] if keep_steps else None
        P, DT, c = solve_band(P, DT, v, final, clear, persons, hist)
        vv, ww, _, _, _ = band_terms(P, DT, v, final)
        cycles.append(dict(t=t, x=x.copy(), v=v, persons=persons, goal=lg, final=final, warm=warm, P=P.copy(),
                           DT=DT.copy(), cost=c, hist=hist))
        if final and np.hypot(*(x[:2] - goal[:2])) < GOAL_XY and v < 0.02:  # at the goal: turn on the spot to face
            turn = wrap(goal[2] - x[2])                                       # its heading (6 rad/s), and stop
            x = np.array([*x[:2], x[2] + turn])
            drive.append((t + abs(turn) / W_SPIN, *x, 0.0))
            break
        T_band, h = np.concatenate([[0], np.cumsum(DT)]), CYCLE / 20
        for j in range(20):  # drive the band's first 0.1 s, each piece's speed and turn rate in turn
            tm = (j + 0.5) * h
            i = min(np.searchsorted(T_band, tm, side="right") - 1, len(DT) - 1)
            v_c, w_c = (float(vv[i]), float(ww[i])) if tm < T_band[-1] else (0.0, 0.0)
            v = float(np.clip(v + np.clip(v_c - v, -A_MAX * h, A_MAX * h), 0.0, V_WHEEL))
            w = float(np.clip(w_c, -(V_WHEEL - v) / (L_AXLE / 2), (V_WHEEL - v) / (L_AXLE / 2)))
            x = x + h * np.array([v * math.cos(x[2] + w * h / 2), v * math.sin(x[2] + w * h / 2), w])
            drive.append((t + (j + 1) * h, *x, v))
        t = round(t + CYCLE, 10)
    return cycles, np.array(drive)


def local_goal(route, s_now, goal):
    """The pose LOOKAHEAD m ahead on the route, facing along it; the goal pose once the route ends within reach.
    Returns (pose, final)."""
    if s_now + LOOKAHEAD >= route.length:
        return goal.copy(), True
    p, th = route.point(s_now + LOOKAHEAD)
    return np.array([p[0], p[1], th]), False


# ---------------------------------------------------------------- refine once: one solve for a whole drive (section 9)
def f(X, U):
    """The motion rules for any leading shape: X (..., 4) = (x, y, theta, v), U (..., 2) = (a, omega)."""
    return np.stack([X[..., 3] * np.cos(X[..., 2]), X[..., 3] * np.sin(X[..., 2]), U[..., 1], U[..., 0]], axis=-1)


def rk4(X, U, h):
    k1 = f(X, U)
    k2 = f(X + h / 2 * k1, U)
    k3 = f(X + h / 2 * k2, U)
    k4 = f(X + h * k3, U)
    return X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def along(route, n, T):
    """States at n equally spaced times along the route, driven at one steady speed, facing along it."""
    X = np.zeros((n, 4))
    for i, s in enumerate(np.linspace(0, route.length, n)):
        X[i, :2], X[i, 2] = route.point(s)
    X[:, 3] = route.length / T
    return X


def collocation(space, route, start, goal, N=60, T0=None, keep=True, clear=None, maxiter=500, cost_eps=1e-3,
                margin=0.01):
    """Trapezoidal direct collocation of the least-time drive from start to goal (poses; at rest at both ends),
    solved once with SciPy's SLSQP, which keeps every constraint exactly (RO-058 sections 6 and 9). Unknowns: the
    state and the controls at N + 1 knot points and the duration T. Constraints: the trapezoid rule between
    neighbouring knots, the start and the goal, and at every knot and halfway between knots both wheels at most
    0.6 m/s, a speed of at least 0 and the robot at least `margin` m clear of everything. First guess: the knots
    spread along the route at a steady speed. The cost is T plus cost_eps times the squared controls, which keeps
    the turn rate from wandering. Returns dict(X, U, T, hist=[(X, U, T)], nit, ok, msg, defects)."""
    clear = clear or Clearance(space)
    n = N + 1
    X0g, Xg = np.array([*start, 0.0]), np.array([*goal, 0.0])
    T0 = T0 or route.length / (0.8 * V_WHEEL)
    tw = np.full(n, 1.0)
    tw[[0, -1]] = 0.5  # trapezoid weights

    def unpack(Z):
        Z = np.atleast_2d(Z)
        return Z[:, :4 * n].reshape(len(Z), n, 4), Z[:, 4 * n:6 * n].reshape(len(Z), n, 2), Z[:, -1]

    def eq(Z):
        X, U, T = unpack(Z)
        F = f(X, U)
        d = X[:, 1:] - X[:, :-1] - (T / N)[:, None, None] / 2 * (F[:, 1:] + F[:, :-1])
        return np.concatenate([d.reshape(len(Z), -1), X[:, 0] - X0g, X[:, -1] - Xg], axis=1)

    def ineq(Z):
        X, U, T = unpack(Z)
        F = f(X, U)
        mid = (X[:, 1:] + X[:, :-1]) / 2 + (T / N)[:, None, None] / 8 * (F[:, :-1] - F[:, 1:])  # Kelly 2017, 3.4
        out = []
        for P, W in ((X, U), (mid, (U[:, 1:] + U[:, :-1]) / 2)):
            wr, wl = wheels(P[..., 3], W[..., 1])
            out += [V_WHEEL - wr, V_WHEEL - wl, P[..., 3], clear(P[..., 0], P[..., 1]) - margin]
        return np.concatenate(out, axis=1)

    def obj(z):
        X, U, T = unpack(z)
        return float(T[0] * (1 + cost_eps / N * np.sum(tw[:, None] * U[0] ** 2)))

    def obj_grad(z):
        X, U, T = unpack(z)
        g = np.zeros_like(z)
        g[4 * n:6 * n] = (2 * cost_eps * T[0] / N * tw[:, None] * U[0]).ravel()
        g[-1] = 1 + cost_eps / N * np.sum(tw[:, None] * U[0] ** 2)
        return g

    z0 = np.concatenate([along(route, n, T0).ravel(), np.zeros(2 * n), [T0]])
    x0, y0, x1, y1 = space.bounds
    r = space.radius
    bounds = ([(x0 + r, x1 - r), (y0 + r, y1 - r), (-2 * np.pi, 2 * np.pi), (0, V_WHEEL)] * n
              + [(-A_MAX, A_MAX), (-W_SPIN, W_SPIN)] * n + [(1.0, 10 * T0)])
    snap = lambda z: tuple(a[0] for a in unpack(z))
    hist = [snap(z0)]
    one = lambda g: (lambda z: g(z[None])[0])
    res = minimize(obj, z0, jac=obj_grad, method="SLSQP", bounds=bounds,
                   callback=(lambda zk: hist.append(snap(zk.copy()))) if keep else None,
                   constraints=[dict(type="eq", fun=one(eq), jac=lambda z: fd_jac(eq, z)),
                                dict(type="ineq", fun=one(ineq), jac=lambda z: fd_jac(ineq, z))],
                   options=dict(maxiter=maxiter, ftol=1e-10))
    X, U, T = snap(res.x)
    return dict(X=X, U=U, T=float(T), hist=hist, nit=res.nit, ok=res.success, msg=res.message,
                defects=eq(res.x[None])[0])


def replay(start, U, T, sub=20):
    """The check between the knots: the collocation's controls (straight lines between knots) replayed in small RK4
    steps from the start. Returns times and states."""
    N = len(U) - 1
    h = T / N / sub
    xs, ts = [np.array([*start, 0.0])], [0.0]
    for k in range(N):
        for j in range(sub):
            xs.append(rk4(xs[-1], U[k] + (U[k + 1] - U[k]) * (j + 0.5) / sub, h))
            ts.append(ts[-1] + h)
    return np.array(ts), np.array(xs)


def rest_to_rest(d):
    """Least time to drive d metres in a straight line from rest to rest within 0.6 m/s and 0.5 m/s^2."""
    if d >= V_WHEEL ** 2 / A_MAX:
        return 2 * V_WHEEL / A_MAX + (d - V_WHEEL ** 2 / A_MAX) / V_WHEEL
    return 2 * math.sqrt(d / A_MAX)


def stop_and_turn(route_pts, start_heading, goal_heading, dt=0.05):
    """Drive the route by turning on the spot to face each next corner (6 rad/s), driving to it from rest to rest
    (speed up at 0.5 m/s^2, cruise at 0.6 m/s if there is room, brake), and at the end turning to the goal's
    heading. Returns the total time, the pieces [(kind, seconds)] and the states (t, x, y, heading, v) every dt s."""
    pieces, th, states, t0 = [], start_heading, [], 0.0
    legs = list(zip(route_pts, route_pts[1:])) + [(route_pts[-1], None)]
    for p, q in legs:
        head = goal_heading if q is None else math.atan2(q[1] - p[1], q[0] - p[0])
        turn = wrap(head - th)
        pieces.append(("turn", abs(turn) / W_SPIN))
        for t in np.arange(0, pieces[-1][1], dt):
            states.append((t0 + t, p[0], p[1], th + turn * t / pieces[-1][1], 0.0))
        t0, th = t0 + pieces[-1][1], head
        if q is None:
            break
        d = math.dist(p, q)
        t1 = min(V_WHEEL / A_MAX, math.sqrt(d / A_MAX))  # time to top speed, and the top speed
        top = A_MAX * t1
        tc = (d - A_MAX * t1 ** 2) / top                  # time cruising
        pieces.append(("drive", 2 * t1 + tc))
        for t in np.arange(0, pieces[-1][1], dt):
            tb = max(0.0, t - t1 - tc)                     # time braking so far
            s = A_MAX * min(t, t1) ** 2 / 2 + top * min(max(t - t1, 0), tc) + top * tb - A_MAX * tb ** 2 / 2
            v = A_MAX * t if t < t1 else top - A_MAX * tb
            states.append((t0 + t, p[0] + s / d * (q[0] - p[0]), p[1] + s / d * (q[1] - p[1]), head, v))
        t0 += pieces[-1][1]
    states.append((t0, *route_pts[-1], goal_heading, 0.0))
    return t0, pieces, np.array(states)
