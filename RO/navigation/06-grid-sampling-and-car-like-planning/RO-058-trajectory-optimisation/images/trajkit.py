"""Trajectory optimisation for this Note (no output when run on its own).

The robot of the Note on planning with motion limits: a differential drive (wheel separation 0.2 m), disk footprint
of radius 0.25 m, each wheel at most 0.6 m/s, forward speed changing by at most 0.5 m/s per second. State
(x, y, theta, v), controls (a, omega): x' = v cos theta, y' = v sin theta, theta' = omega, v' = a.
The drive: from rest at (2.0, 1.0) facing 30 degrees to rest at the door pose (3.6, 3.5) facing 90 degrees,
past the table's corner at (3.5, 3.0).

Contents:
- the straight drive (one dimension): shooting by gradient descent, trapezoidal collocation of the time-optimal drive;
- the room drive: single shooting, multiple shooting and trapezoidal collocation, each solved with SciPy's SLSQP
  (a gradient-based solver for problems with constraints), keeping every iterate for the animations;
- iLQR on the room drive with a fixed time, and plain gradient descent on the same cost for comparison;
- the stop-and-turn baseline that follows the A* route, stopping to turn at each corner.
"""
import math

import numpy as np
from scipy.optimize import minimize
from threadpoolctl import threadpool_limits

threadpool_limits(1)   # one BLAS thread: the solvers' iteration counts depend on the thread count otherwise (80 to 82)

# ---------------------------------------------------------------- the robot and the room
L_AXLE, V_WHEEL, A_MAX, R_BODY = 0.2, 0.6, 0.5, 0.25
W_SPIN = 2 * V_WHEEL / L_AXLE                     # turn rate on the spot: 6 rad/s
START = np.array([2.0, 1.0, math.radians(30), 0.0])
GOAL = np.array([3.6, 3.5, math.radians(90), 0.0])
TABLE = np.array([(3.0, 1.0), (5.0, 1.0), (5.5, 2.5), (3.5, 3.0)])
CORNER = TABLE[3]
ROOM_W, ROOM_H = 7.0, 4.0
# The A* route of RO-034 (0.5 m cells, 3.414 m between cell centres) with the robot's position in place of the start
# cell's centre and the door pose in place of the goal cell's centre; points on a straight piece dropped
ROUTE_PTS = np.array([START[:2], (2.75, 1.75), (2.75, 3.25), (3.25, 3.75), GOAL[:2]])
LINE_LEN = float(np.hypot(*(GOAL[:2] - START[:2])))  # the straight line from start to goal: 2.968 m
LINE_HEADING = math.atan2(GOAL[1] - START[1], GOAL[0] - START[0])


def table_dist(px, py):
    """Signed distance from points to the table polygon: positive outside, negative inside (arrays allowed)."""
    px, py = np.asarray(px, float), np.asarray(py, float)
    best = np.full(px.shape, np.inf)
    inside = np.ones(px.shape, bool)
    for i in range(4):
        a, b = TABLE[i], TABLE[(i + 1) % 4]
        ex, ey = b - a
        t = np.clip(((px - a[0]) * ex + (py - a[1]) * ey) / (ex * ex + ey * ey), 0, 1)
        best = np.minimum(best, np.hypot(px - a[0] - t * ex, py - a[1] - t * ey))
        inside &= (ex * (py - a[1]) - ey * (px - a[0])) >= 0
    return np.where(inside, -best, best)


def clearance(px, py):
    """Gap between the robot's disk and the table (negative: overlap)."""
    return table_dist(px, py) - R_BODY


def f(X, U):
    """Time derivative of the state, rows of X = (x, y, theta, v), rows of U = (a, omega)."""
    X, U = np.atleast_2d(X), np.atleast_2d(U)
    return np.stack([X[:, 3] * np.cos(X[:, 2]), X[:, 3] * np.sin(X[:, 2]), U[:, 1], U[:, 0]], axis=1)


def rk4(x, u, h):
    k1 = f(x, u)[0]
    k2 = f(x + h / 2 * k1, u)[0]
    k3 = f(x + h / 2 * k2, u)[0]
    k4 = f(x + h * k3, u)[0]
    return x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(x0, U, T, sub=4):
    """Hold each row of U for T / len(U) s; RK4 with `sub` steps per interval. Returns all states (dense)."""
    n = len(U)
    h = T / n / sub
    xs = [np.array(x0, float)]
    for k in range(n):
        for _ in range(sub):
            xs.append(rk4(xs[-1], U[k], h))
    return np.array(xs)


def wheels(v, w):
    return v + w * L_AXLE / 2, v - w * L_AXLE / 2


# ---------------------------------------------------------------- the straight drive (one dimension)
def straight_gd(goal=3.0, T=10.0, eta=0.0006, steps=6):
    """Shooting with one number: speed up at a for T/2, brake at a for T/2, so the end position is a (T/2)^2.
    Gradient descent on the squared miss J(a) = (a (T/2)^2 - goal)^2. Returns [(a, end, miss, dJ/da)]."""
    k = (T / 2) ** 2
    a, out = 0.0, []
    for _ in range(steps):
        end = a * k
        miss = end - goal
        grad = 2 * k * miss
        out.append((a, end, miss, grad))
        a = a - eta * grad
    return out


def bang_coast_bang(dist=3.0, v_top=V_WHEEL, a=A_MAX):
    """Least time to drive `dist` from rest to rest with |accel| <= a and v <= v_top."""
    ramp = v_top * v_top / a
    return 2 * v_top / a + (dist - ramp) / v_top


def straight_collocation(dist=3.0, N=10, v_top=V_WHEEL, a_max=A_MAX):
    """Trapezoidal collocation of the least-time straight drive: knots (s, v, a) and the time T, solved with
    SciPy's SLSQP (constraints kept exactly). Returns dict(s, v, a, T, nit)."""
    n = N + 1

    def unpack(z):
        return z[:n], z[n:2 * n], z[2 * n:3 * n], z[-1]

    def defects(z):
        s, v, a, T = unpack(z)
        h = T / N
        return np.concatenate([s[1:] - s[:-1] - h / 2 * (v[1:] + v[:-1]), v[1:] - v[:-1] - h / 2 * (a[1:] + a[:-1]),
                               [s[0], v[0], s[-1] - dist, v[-1]]])

    T0 = 10.0
    z0 = np.concatenate([np.linspace(0, dist, n), np.full(n, dist / T0), np.zeros(n), [T0]])
    bounds = [(None, None)] * n + [(0, v_top)] * n + [(-a_max, a_max)] * n + [(1, 30)]
    r = minimize(lambda z: z[-1], z0, jac=lambda z: np.eye(len(z))[-1], method="SLSQP", bounds=bounds,
                 constraints=[dict(type="eq", fun=defects)], options=dict(maxiter=500, ftol=1e-12))
    s, v, a, T = unpack(r.x)
    return dict(s=s, v=v, a=a, T=float(T), ok=r.success, nit=r.nit)


# ---------------------------------------------------------------- the room drive: transcriptions
EPS = 1e-3            # a small cost on effort added to the time, so that the turn rate does not wander


C_W = 0.01            # effort weight of the turn rate: 1 rad/s costs as much as 0.1 m/s^2
RHOS = (1e2, 1e3, 1e4, 1e5, 1e6)   # penalty weights on the constraints, raised in turn


def fb(X, U):
    """f for any leading shape: X (..., 4), U (..., 2)."""
    return np.stack([X[..., 3] * np.cos(X[..., 2]), X[..., 3] * np.sin(X[..., 2]), U[..., 1], U[..., 0]], axis=-1)


def rk4b(X, U, h):
    h = np.asarray(h)[..., None]
    k1 = fb(X, U)
    k2 = fb(X + h / 2 * k1, U)
    k3 = fb(X + h / 2 * k2, U)
    k4 = fb(X + h * k3, U)
    return X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def _fd_jac(batch_fun, z, eps=1e-6):
    """Central-difference Jacobian of a batched function: every variable perturbed at once, in one batch."""
    n = len(z)
    Z = np.vstack([z + eps * np.eye(n), z - eps * np.eye(n)])
    F = batch_fun(Z)
    return ((F[:n] - F[n:]) / (2 * eps)).T


def _penalties(px, py, v, w, U):
    """Amounts by which the limits are broken (0 when kept): both wheels, negative speed, the table."""
    w1, w2 = wheels(v, w)
    return np.concatenate([np.maximum(0, w1 - V_WHEEL), np.maximum(0, w2 - V_WHEEL), np.maximum(0, -v),
                           np.maximum(0, -clearance(px, py))], axis=1)


def _ls(res_b, z0, lo, hi, snap, keep=True):
    """Least squares with penalties: the residuals are the cost's square roots plus sqrt(rho) times every defect
    and broken limit; SciPy's least_squares (a Gauss-Newton trust-region method that uses the Jacobian, the
    gradient of every residual) solves it for rho = 1e2, 1e3, ... 1e6 in turn. Returns (z, iterations, hist)."""
    from scipy.optimize import least_squares
    z = np.clip(np.asarray(z0, float), lo + 1e-9, hi - 1e-9)
    hist = [snap(z)]
    nit = 0
    for rho in RHOS:
        def cb(intermediate_result):
            if keep:
                hist.append(snap(intermediate_result.x.copy()))
        r = least_squares(lambda z: res_b(z[None], rho)[0], z, jac=lambda z: _fd_jac(lambda Z: res_b(Z, rho), z),
                          bounds=(lo, hi), method="trf", max_nfev=500, xtol=1e-12, ftol=1e-12, callback=cb)
        z = r.x
        nit += r.njev
    return z, nit, hist


def collocation(N=30, T0=9.0, guess=None, keep=True, T_fix=None):
    """Trapezoidal direct collocation. Without T_fix: the least-time drive (cost T^2 plus a little effort, which
    has the same best T); with T_fix: the least-effort drive in T_fix seconds. Variables: state and controls at
    N + 1 knot points (and T). Returns dict(X, U, T, hist=[(X, U, T)], nit, defects, effort)."""
    n = N + 1
    T0 = T0 if T_fix is None else T_fix
    tw = np.full(n, 1.0)                           # trapezoid weights: half at the two ends
    tw[0] = tw[-1] = 0.5

    def unpack(Z):
        Z = np.atleast_2d(Z)
        B = len(Z)
        T = Z[:, -1] if T_fix is None else np.full(B, T_fix)
        return Z[:, :4 * n].reshape(B, n, 4), Z[:, 4 * n:6 * n].reshape(B, n, 2), T

    def defects_b(Z):
        X, U, T = unpack(Z)
        h = (T / N)[:, None, None]
        F = fb(X, U)
        d = X[:, 1:] - X[:, :-1] - h / 2 * (F[:, 1:] + F[:, :-1])
        return np.concatenate([d.reshape(len(Z), -1), X[:, 0] - START, X[:, -1] - GOAL], axis=1)

    def res_b(Z, rho):
        X, U, T = unpack(Z)
        h = (T / N)[:, None]
        F = fb(X, U)
        # the state halfway between knots, on the quadratic the trapezoid rule implies (Kelly 2017, 3.4)
        mid = (X[:, 1:] + X[:, :-1]) / 2 + h[:, :, None] / 8 * (F[:, :-1] - F[:, 1:])
        Um = (U[:, 1:] + U[:, :-1]) / 2
        pen = np.concatenate([_penalties(X[..., 0], X[..., 1], X[..., 3], U[..., 1], U),
                              _penalties(mid[..., 0], mid[..., 1], mid[..., 3], Um[..., 1], Um)], axis=1)
        we = 1.0 if T_fix is not None else EPS
        eff = np.concatenate([np.sqrt(we * h * tw) * U[..., 0], np.sqrt(we * h * tw * C_W) * U[..., 1]], axis=1)
        parts = [eff, np.sqrt(rho) * defects_b(Z), np.sqrt(rho) * pen]
        if T_fix is None:
            parts.insert(0, T[:, None])
        return np.concatenate(parts, axis=1)

    if isinstance(guess, str) and guess == "shot":   # the first shot of shooting, read at the knots
        sub = 4
        Uf = first_shot(N, T0)
        X0 = simulate(START, Uf, T0, sub)[::sub]
        U0 = np.vstack([Uf, Uf[-1:]])
    else:                                          # knots on the route at a steady speed, the heading turning
        X0 = route_guess(n, T0)                     # evenly from the start's to the goal's, zero controls (at
        X0[:, 2] = np.linspace(START[2], GOAL[2], n)  # zero speed the model cannot move sideways, so a resting
        U0 = np.zeros((n, 2))                       # guess gives the solver no direction to move in)
    z0 = np.concatenate([X0.ravel(), U0.ravel()] + ([[T0]] if T_fix is None else []))
    lo = np.concatenate([np.tile([-np.inf, -np.inf, -np.inf, -np.inf], n), np.tile([-A_MAX, -W_SPIN], n)]
                        + ([[1.0]] if T_fix is None else []))
    hi = np.concatenate([np.tile([np.inf, np.inf, np.inf, np.inf], n), np.tile([A_MAX, W_SPIN], n)]
                        + ([[30.0]] if T_fix is None else []))
    snap = lambda z: tuple(a[0] for a in unpack(z))
    z, nit, hist = _ls(res_b, z0, lo, hi, snap, keep)
    X, U, T = snap(z)
    return dict(X=X, U=U, T=float(T), hist=hist, nit=nit, defects=defects_b(z[None])[0],
                effort=float(T / N * np.sum(tw * (U[:, 0] ** 2 + C_W * U[:, 1] ** 2))))


def collocation_time(N=30, T0=9.0, keep=True, maxiter=500):
    """Trapezoidal collocation of the least-time drive (plus EPS times the squared controls, to keep the turn rate
    from wandering), solved with SciPy's SLSQP so that every constraint holds exactly: the defects, the start and the
    goal, and at every knot and halfway between knots the wheel limits, a speed of at least 0 and the table.
    Returns dict(X, U, T, hist, nit, defects)."""
    n = N + 1
    tw = np.full(n, 1.0)
    tw[0] = tw[-1] = 0.5

    def unpack(Z):
        Z = np.atleast_2d(Z)
        B = len(Z)
        return Z[:, :4 * n].reshape(B, n, 4), Z[:, 4 * n:6 * n].reshape(B, n, 2), Z[:, -1]

    def eq_b(Z):
        X, U, T = unpack(Z)
        h = (T / N)[:, None, None]
        F = fb(X, U)
        d = X[:, 1:] - X[:, :-1] - h / 2 * (F[:, 1:] + F[:, :-1])
        return np.concatenate([d.reshape(len(Z), -1), X[:, 0] - START, X[:, -1] - GOAL], axis=1)

    def ineq_b(Z):
        X, U, T = unpack(Z)
        h = (T / N)[:, None, None]
        F = fb(X, U)
        mid = (X[:, 1:] + X[:, :-1]) / 2 + h / 8 * (F[:, :-1] - F[:, 1:])
        Um = (U[:, 1:] + U[:, :-1]) / 2
        out = []
        for P, W in ((X, U), (mid, Um)):
            w1, w2 = wheels(P[..., 3], W[..., 1])
            out += [V_WHEEL - w1, V_WHEEL - w2, P[..., 3], clearance(P[..., 0], P[..., 1])]
        return np.concatenate(out, axis=1)

    def obj(z):
        X, U, T = unpack(z)
        return float(T[0] + EPS * T[0] / N * np.sum(tw * (U[0, :, 0] ** 2 + U[0, :, 1] ** 2)))

    def obj_grad(z):
        X, U, T = unpack(z)
        g = np.zeros_like(z)
        g[4 * n:6 * n] = (2 * EPS * T[0] / N * tw[:, None] * U[0]).ravel()
        g[-1] = 1 + EPS / N * np.sum(tw * (U[0, :, 0] ** 2 + U[0, :, 1] ** 2))
        return g

    X0 = route_guess(n, T0)
    U0 = np.zeros((n, 2))
    z0 = np.concatenate([X0.ravel(), U0.ravel(), [T0]])
    bounds = ([(R_BODY, ROOM_W - R_BODY), (R_BODY, ROOM_H - R_BODY), (-np.pi, 2 * np.pi), (0, V_WHEEL)] * n
              + [(-A_MAX, A_MAX), (-W_SPIN, W_SPIN)] * n + [(1.0, 30.0)])
    snap = lambda z: tuple(a[0] for a in unpack(z))
    hist = [snap(z0)]
    one = lambda g: (lambda z: g(z[None])[0])
    r = minimize(obj, z0, jac=obj_grad, method="SLSQP", bounds=bounds,
                 callback=(lambda zk: hist.append(snap(zk.copy()))) if keep else None,
                 constraints=[dict(type="eq", fun=one(eq_b), jac=lambda z: _fd_jac(eq_b, z)),
                              dict(type="ineq", fun=one(ineq_b), jac=lambda z: _fd_jac(ineq_b, z))],
                 options=dict(maxiter=maxiter, ftol=1e-10))
    X, U, T = snap(r.x)
    return dict(X=X, U=U, T=float(T), hist=hist, nit=r.nit, ok=r.success, msg=r.message,
                defects=eq_b(r.x[None])[0])


def route_guess(n, T):
    """States at n equally spaced times along the A* route (ROUTE_PTS), driven at one steady speed and facing along
    the route: the search's route as the first guess."""
    pts = ROUTE_PTS
    seg = np.hypot(*np.diff(pts, axis=0).T)
    S = np.concatenate([[0], np.cumsum(seg)])
    X = np.zeros((n, 4))
    for i, s in enumerate(np.linspace(0, S[-1], n)):
        j = min(np.searchsorted(S, s, side="right") - 1, len(seg) - 1)
        u = (pts[j + 1] - pts[j]) / seg[j]
        X[i, :2] = pts[j] + (s - S[j]) * u
        X[i, 2] = math.atan2(u[1], u[0])
        X[i, 3] = S[-1] / T
    return X


def first_shot(N=30, T0=9.0, a=0.12):
    """The opening guess for shooting: turn to face the goal in the first interval, speed up at a for half the
    time, brake at a for the other half (too gently: it stops short of the goal)."""
    U0 = np.zeros((N, 2))
    U0[0, 1] = (LINE_HEADING - START[2]) / (T0 / N)
    U0[:N // 2, 0], U0[N // 2:, 0] = a, -a
    return U0


def shooting(N=30, M=1, T_fix=8.0, U0=None, keep=True, sub=4, starts="route"):
    """Direct shooting of the least-effort drive in T_fix seconds: piecewise-constant controls on N intervals,
    simulated with RK4 (sub steps per interval). M = 1: single shooting. M > 1: multiple shooting, the N intervals
    split into M segments, each starting from its own state, a decision variable, placed on the first shot; the
    segment ends must meet the next starts (defects). Returns dict(U, S, segs, traj, hist=[(segs, U)], nit,
    defects, effort)."""
    K = N // M
    h = T_fix / N
    U0 = first_shot(N, T_fix) if U0 is None else U0

    def unpack(Z):
        Z = np.atleast_2d(Z)
        B = len(Z)
        U = Z[:, :2 * N].reshape(B, N, 2)
        S = np.concatenate([np.broadcast_to(START, (B, 1, 4)), Z[:, 2 * N:].reshape(B, M - 1, 4)], axis=1)
        return U, S

    def segs_b(Z):
        """States at every RK4 substep of every segment: (B, M, K * sub + 1, 4)."""
        U, S = unpack(Z)
        X = S
        out = [S]
        for k in range(K):
            u = np.stack([U[:, j * K + k] for j in range(M)], axis=1)
            for _ in range(sub):
                X = rk4b(X, u, np.full((len(Z), 1), h / sub))
                out.append(X)
        return np.stack(out, axis=2)

    def defects_b(Z):
        U, S = unpack(Z)
        ends = segs_b(Z)[:, :, -1]
        d = [(ends[:, :-1] - S[:, 1:]).reshape(len(Z), -1)] if M > 1 else []
        return np.concatenate(d + [ends[:, -1] - GOAL], axis=1)

    def res_b(Z, rho):
        U, S = unpack(Z)
        P = segs_b(Z)
        B = len(Z)
        vs = P[:, :, :-1:sub, 3].reshape(B, -1)          # speed at the start of every interval, in order
        Pm = P[:, :, ::sub // 2].reshape(B, -1, 4)         # the start and the middle of every interval
        w1, w2 = wheels(vs, U[..., 1])
        pen = np.concatenate([np.maximum(0, w1 - V_WHEEL), np.maximum(0, w2 - V_WHEEL), np.maximum(0, -Pm[..., 3]),
                              np.maximum(0, -clearance(Pm[..., 0], Pm[..., 1]))], axis=1)
        eff = np.concatenate([np.sqrt(h) * U[..., 0], np.sqrt(h * C_W) * U[..., 1]], axis=1)
        return np.concatenate([eff, np.sqrt(rho) * defects_b(Z), np.sqrt(rho) * pen], axis=1)

    z0 = U0.ravel()
    if M > 1:                                       # segment starts on the route (or where the first shot is)
        S0 = route_guess(M + 1, T_fix)[1:-1] if starts == "route" else simulate(START, U0, T_fix, sub)[::K * sub][1:M]
        z0 = np.concatenate([z0, S0.ravel()])
    lo = np.concatenate([np.tile([-A_MAX, -W_SPIN], N), np.tile([-np.inf, -np.inf, -np.inf, -np.inf], M - 1)])
    hi = np.concatenate([np.tile([A_MAX, W_SPIN], N), np.tile([np.inf, np.inf, np.inf, np.inf], M - 1)])
    snap = lambda z: (segs_b(z[None])[0], unpack(z)[0][0])
    z, nit, hist = _ls(res_b, z0, lo, hi, snap, keep)
    segs, U = snap(z)
    return dict(U=U, S=unpack(z)[1][0], segs=segs, traj=segs.reshape(-1, 4), hist=hist, nit=nit,
                defects=defects_b(z[None])[0], effort=float(h * np.sum(U[:, 0] ** 2 + C_W * U[:, 1] ** 2)))


# ---------------------------------------------------------------- stop and turn along a route with one corner
def stop_and_turn():
    """Turn on the spot to face the next point, drive to it from rest to rest, and so on along ROUTE_PTS, then turn
    to the goal's heading. Returns dict(T, pieces=[(kind, duration, ...)], sample(t) -> (x, y, th, v))."""
    pts = list(ROUTE_PTS)
    th = START[2]
    pieces = []
    for p, q in zip(pts, pts[1:]):
        d = np.hypot(*(q - p))
        head = math.atan2(*(q - p)[::-1])
        pieces.append(("turn", abs(head - th) / W_SPIN, p, th, head))
        th = head
        if d >= V_WHEEL ** 2 / A_MAX:
            dur = bang_coast_bang(d)
        else:
            dur = 2 * math.sqrt(d / A_MAX)
        pieces.append(("drive", dur, p, q, d))
    pieces.append(("turn", abs(GOAL[2] - th) / W_SPIN, pts[-1], th, GOAL[2]))
    T = sum(pc[1] for pc in pieces)

    def drive_s(d, t):
        """Distance and speed after t s of a rest-to-rest drive of d m (speed up, maybe cruise, brake)."""
        if d >= V_WHEEL ** 2 / A_MAX:
            t1, vt = V_WHEEL / A_MAX, V_WHEEL
            tc = (d - V_WHEEL ** 2 / A_MAX) / V_WHEEL
        else:
            t1, tc = math.sqrt(d / A_MAX), 0.0
            vt = A_MAX * t1
        if t < t1:
            return A_MAX * t * t / 2, A_MAX * t
        s1 = A_MAX * t1 * t1 / 2
        if t < t1 + tc:
            return s1 + vt * (t - t1), vt
        tb = min(t - t1 - tc, t1)
        return s1 + vt * tc + vt * tb - A_MAX * tb * tb / 2, vt - A_MAX * tb

    def sample(t):
        for kind, dur, a, b, c in pieces:
            if t <= dur + 1e-12:
                if kind == "turn":
                    return (a[0], a[1], b + (c - b) * (t / dur if dur else 1), 0.0)
                s, v = drive_s(c, t)
                u = (b - a) / c
                return (a[0] + s * u[0], a[1] + s * u[1], math.atan2(u[1], u[0]), v)
            t -= dur
        return (GOAL[0], GOAL[1], GOAL[2], 0.0)

    return dict(T=T, pieces=pieces, sample=sample)


# ---------------------------------------------------------------- iLQR on the room drive, fixed time
ILQR_T, ILQR_N = 8.0, 30
R_A, R_W = 1.0, 0.01                 # effort weights on a (per (m/s^2)^2 s) and omega (per (rad/s)^2 s)
W_OBS, W_LIM = 1e6, 1e6              # penalty weights: table and wheel-speed limit (the last rho of the others)
Q_END = np.full(4, 1e6)


def _residual(x, u, h):
    """Stage cost = sum of squares of these residuals (effort, table and wheel penalties)."""
    w1, w2 = wheels(x[3], u[1])
    return np.array([math.sqrt(R_A * h) * u[0], math.sqrt(R_W * h) * u[1],
                     math.sqrt(W_OBS) * max(0.0, -clearance(x[0], x[1])),
                     math.sqrt(W_LIM) * max(0.0, w1 - V_WHEEL), math.sqrt(W_LIM) * max(0.0, w2 - V_WHEEL),
                     math.sqrt(W_LIM) * max(0.0, -x[3])])


def _end_residual(x):
    return np.sqrt(Q_END) * (x - GOAL)


def _jac(fun, z, eps=1e-6):
    f0 = fun(z)
    J = np.zeros((len(f0), len(z)))
    for i in range(len(z)):
        dz = np.zeros(len(z))
        dz[i] = eps
        J[:, i] = (fun(z + dz) - fun(z - dz)) / (2 * eps)
    return f0, J


def ilqr_cost(xs, us, h):
    return sum(float(np.sum(_residual(x, u, h) ** 2)) for x, u in zip(xs[:-1], us)) + float(
        np.sum(_end_residual(xs[-1]) ** 2))


def rollout(us, h, x0=START):
    xs = [np.array(x0, float)]
    for u in us:
        xs.append(rk4(xs[-1], u, h))
    return np.array(xs)


def ilqr(T=ILQR_T, N=ILQR_N, iters=200, us0=None, tol=1e-12):
    """iLQR: linearise the dynamics and make a quadratic model of the cost (Gauss-Newton) around the current
    trajectory; a backward pass gives, for every step, a change of control k and a feedback gain K; a forward
    pass simulates with u + alpha k + K (x - x_old), with a line search on alpha. Returns dict(xs, us, cost, hist)."""
    h = T / N
    us = np.zeros((N, 2)) if us0 is None else us0.copy()
    xs = rollout(us, h)
    cost = ilqr_cost(xs, us, h)
    hist = [(xs.copy(), us.copy(), cost)]
    mu = 1e-6
    for it in range(iters):
        A, B, rs, Jx, Ju = [], [], [], [], []
        for x, u in zip(xs[:-1], us):
            _, Jz = _jac(lambda z: rk4(z[:4], z[4:], h), np.concatenate([x, u]))
            A.append(Jz[:, :4])
            B.append(Jz[:, 4:])
            r, Jr = _jac(lambda z: _residual(z[:4], z[4:], h), np.concatenate([x, u]))
            rs.append(r)
            Jx.append(Jr[:, :4])
            Ju.append(Jr[:, 4:])
        rN, JN = _jac(_end_residual, xs[-1])
        Vx, Vxx = 2 * JN.T @ rN, 2 * JN.T @ JN
        ks, Ks = [None] * N, [None] * N
        for k in range(N - 1, -1, -1):
            lx, lu = 2 * Jx[k].T @ rs[k], 2 * Ju[k].T @ rs[k]
            lxx, luu, lux = 2 * Jx[k].T @ Jx[k], 2 * Ju[k].T @ Ju[k], 2 * Ju[k].T @ Jx[k]
            Qx = lx + A[k].T @ Vx
            Qu = lu + B[k].T @ Vx
            Qxx = lxx + A[k].T @ Vxx @ A[k]
            Quu = luu + B[k].T @ Vxx @ B[k] + mu * np.eye(2)
            Qux = lux + B[k].T @ Vxx @ A[k]
            ks[k] = -np.linalg.solve(Quu, Qu)
            Ks[k] = -np.linalg.solve(Quu, Qux)
            Vx = Qx + Ks[k].T @ Quu @ ks[k] + Ks[k].T @ Qu + Qux.T @ ks[k]
            Vxx = Qxx + Ks[k].T @ Quu @ Ks[k] + Ks[k].T @ Qux + Qux.T @ Ks[k]
            Vxx = (Vxx + Vxx.T) / 2
        for alpha in (1.0, 0.5, 0.25, 0.1, 0.05, 0.01):
            xn = [np.array(START, float)]
            un = []
            for k in range(N):
                u = us[k] + alpha * ks[k] + Ks[k] @ (xn[-1] - xs[k])
                un.append(u)
                xn.append(rk4(xn[-1], u, h))
            xn, un = np.array(xn), np.array(un)
            cn = ilqr_cost(xn, un, h)
            if cn < cost:
                break
        if cn >= cost:
            mu *= 10
            continue
        done = (cost - cn) < tol * cost
        xs, us, cost = xn, un, cn
        mu = max(mu / 10, 1e-9)
        hist.append((xs.copy(), us.copy(), cost))
        if done:
            break
    return dict(xs=xs, us=us, cost=cost, hist=hist, h=h)


def cost_gradient(us, h):
    """Gradient of the iLQR cost with respect to every control, by the chain rule backwards along the rollout
    (the same derivatives iLQR uses, without its quadratic model)."""
    xs = rollout(us, h)
    N = len(us)
    rN, JN = _jac(_end_residual, xs[-1])
    lam = 2 * JN.T @ rN
    g = np.zeros_like(us)
    for k in range(N - 1, -1, -1):
        _, Jz = _jac(lambda z: rk4(z[:4], z[4:], h), np.concatenate([xs[k], us[k]]))
        r, Jr = _jac(lambda z: _residual(z[:4], z[4:], h), np.concatenate([xs[k], us[k]]))
        g[k] = 2 * Jr[:, 4:].T @ r + Jz[:, 4:].T @ lam
        lam = 2 * Jr[:, :4].T @ r + Jz[:, :4].T @ lam
    return g, xs


def gradient_descent(T=ILQR_T, N=ILQR_N, iters=3000, target=None, us0=None):
    """Plain gradient descent on the same cost, with a step found by halving until the cost falls.
    Stops early when the cost reaches `target`. Returns dict(us, xs, costs)."""
    h = T / N
    us = np.zeros((N, 2)) if us0 is None else us0.copy()
    costs = [ilqr_cost(rollout(us, h), us, h)]
    step = 1e-3
    for it in range(iters):
        g, xs = cost_gradient(us, h)
        while True:
            un = us - step * g
            cn = ilqr_cost(rollout(un, h), un, h)
            if cn < costs[-1] or step < 1e-12:
                break
            step /= 2
        us = un
        costs.append(cn)
        step *= 1.5
        if target is not None and cn <= target:
            break
    return dict(us=us, xs=rollout(us, h), costs=costs)


# ---------------------------------------------------------------- iLQR on the straight drive: a check at easy values
def ilqr_straight(dist=3.0, T=10.0, N=30, q_end=1e6, iters=3):
    """iLQR on the straight drive: state (s, v), control a held over each step, exact steps
    s+ = s + v h + a h^2 / 2, v+ = v + a h; cost = sum a^2 h + q_end |(s, v) - (dist, 0)|^2. The model is linear and
    the cost quadratic, so the first iteration lands on the optimum. Returns the cost after each iteration and the
    controls."""
    h = T / N
    A = np.array([[1.0, h], [0.0, 1.0]])
    B = np.array([[h * h / 2], [h]])
    goal = np.array([dist, 0.0])
    us = np.zeros(N)

    def roll(us):
        xs = [np.zeros(2)]
        for u in us:
            xs.append(A @ xs[-1] + B[:, 0] * u)
        return np.array(xs)

    def cost(us):
        xs = roll(us)
        return float(np.sum(us ** 2) * h + q_end * np.sum((xs[-1] - goal) ** 2))

    costs = [cost(us)]
    for _ in range(iters):
        xs = roll(us)
        Vx, Vxx = 2 * q_end * (xs[-1] - goal), 2 * q_end * np.eye(2)
        ks, Ks = np.zeros(N), np.zeros((N, 2))
        for k in range(N - 1, -1, -1):
            Qu = 2 * h * us[k] + (B.T @ Vx)[0]
            Quu = 2 * h + (B.T @ Vxx @ B)[0, 0]
            Qux = (B.T @ Vxx @ A)[0]
            Qx = A.T @ Vx
            Qxx = A.T @ Vxx @ A
            ks[k], Ks[k] = -Qu / Quu, -Qux / Quu
            Vx = Qx + Ks[k] * Quu * ks[k] + Ks[k] * Qu + Qux * ks[k]
            Vxx = Qxx + Quu * np.outer(Ks[k], Ks[k]) + np.outer(Ks[k], Qux) + np.outer(Qux, Ks[k])
        xn, un = [np.zeros(2)], []
        for k in range(N):
            u = us[k] + ks[k] + Ks[k] @ (xn[-1] - xs[k])
            un.append(u)
            xn.append(A @ xn[-1] + B[:, 0] * u)
        us = np.array(un)
        costs.append(cost(us))
    return dict(costs=costs, us=us, xs=roll(us), h=h)


# ---------------------------------------------------------------- results shared by the figure scripts
def cached(name, fn):
    """fn() once, kept in a temporary folder keyed by this file's text, so the figure scripts share a solve."""
    import hashlib
    import pickle
    import tempfile
    from pathlib import Path
    key = hashlib.sha1(Path(__file__).read_bytes()).hexdigest()[:12]
    p = Path(tempfile.gettempdir()) / "ro058_cache" / f"{name}_{key}.pkl"
    if p.exists():
        return pickle.loads(p.read_bytes())
    out = fn()
    p.parent.mkdir(exist_ok=True)
    p.write_bytes(pickle.dumps(out))
    return out


def drive_controls(X, U, T, sub=20):
    """Simulate the collocation controls (straight lines between knots) with small RK4 steps from the start:
    the check between the knot points. Returns times and states."""
    N = len(U) - 1
    h = T / N / sub
    xs, ts = [np.array(START, float)], [0.0]
    for k in range(N):
        for j in range(sub):
            t0 = j / sub
            u = U[k] + (U[k + 1] - U[k]) * (t0 + 0.5 / sub)
            xs.append(rk4(xs[-1], u, h))
            ts.append(ts[-1] + h)
    return np.array(ts), np.array(xs)


def solutions():
    """Every solve the figures use, computed once (see cached)."""
    return dict(
        time=cached("time", lambda: collocation_time()),
        colloc=cached("colloc", lambda: collocation(T_fix=8.0)),
        single=cached("single", lambda: shooting(M=1)),
        multi=cached("multi", lambda: shooting(M=5)),
        ilqr=cached("ilqr", lambda: ilqr(us0=first_shot(ILQR_N, ILQR_T))),
        gd=cached("gd", lambda: gradient_descent(us0=first_shot(ILQR_N, ILQR_T), iters=1000)))
