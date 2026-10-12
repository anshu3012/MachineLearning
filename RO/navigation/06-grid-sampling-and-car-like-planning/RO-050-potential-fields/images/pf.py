"""Potential fields for this Note (no output when run on its own): the room of RO-009 seen in the disk robot's C-space
(cspace.py, footprint radius 0.25 m), an attractive bowl centred on the doorway centre, a repulsive hill round each
obstacle, gradient descent, the randomized potential field (random walks), a harmonic potential on a grid, and the
Rimon-Koditschek navigation function on a sphere-world version of the room."""
import numpy as np
import shapely
from shapely.geometry import Point
from shapely.ops import nearest_points

import cspace as c

GOAL = np.array(c.GOAL)                  # the doorway centre (3.6, 4.0)
START = np.array(c.START[:2])            # the robot at (2, 1)
START2 = np.array([4.0, 0.5])            # the second start: between the table and the bottom wall
ZETA = 1.0                               # attractive gain (1/m^2): U_att = 1/2 ZETA |q - goal|^2
ETA = 0.02                               # repulsive gain (m^2)
QSTAR = 0.5                              # influence distance (m): an obstacle pushes only within this clearance
STEP = 0.01                              # gradient-descent step factor alpha (m^2 per unit of U)
MAXSTEP = 0.05                           # longest step (m)


def obstacles():
    """The nine obstacles: table, cabinet (one body), two poles, five wall slabs."""
    T, R1, R2, pink, green = c.furniture()
    return [T, R1.union(R2), pink, green] + c.walls()


OBS = obstacles()
for _o in OBS:
    shapely.prepare(_o)


def clearance_vec(q):
    """For each obstacle: the clearance d_i (distance from the centre to the obstacle minus the radius 0.25 m) and the
    unit vector pointing from the obstacle's nearest point to the centre (the way d_i grows fastest)."""
    p = Point(q[0], q[1])
    out = []
    for o in OBS:
        a, b = nearest_points(o, p)
        v = np.array([b.x - a.x, b.y - a.y])
        n = np.hypot(*v)
        out.append((n - c.R, v / n if n > 0 else np.zeros(2)))
    return out


def u_att(q):
    return 0.5 * ZETA * float(np.sum((np.asarray(q) - GOAL) ** 2))


def u_rep_one(d):
    return 0.0 if d > QSTAR else 0.5 * ETA * (1 / d - 1 / QSTAR) ** 2


def U(q):
    """Total potential: the bowl plus one hill per obstacle; infinite inside the obstacle region."""
    cl = clearance_vec(q)
    if min(d for d, _ in cl) <= 0:
        return np.inf
    return u_att(q) + sum(u_rep_one(d) for d, _ in cl)


def grad(q):
    q = np.asarray(q, float)
    g = ZETA * (q - GOAL)
    for d, n in clearance_vec(q):
        if d <= QSTAR:
            g += ETA * (1 / QSTAR - 1 / d) / d ** 2 * n
    return g


def descend(q0, n_max=8000, tol=1e-5, goal_tol=0.02):
    """Gradient descent: q <- q - alpha grad U, each step at most MAXSTEP long. Stops at the goal or when a step is
    shorter than tol (a minimum). Returns the list of points."""
    q = np.array(q0, float)
    pts = [q.copy()]
    for _ in range(n_max):
        s = -STEP * grad(q)
        L = np.hypot(*s)
        if L > MAXSTEP:
            s *= MAXSTEP / L
        q = q + s
        pts.append(q.copy())
        if np.hypot(*(q - GOAL)) < goal_tol or np.hypot(*s) < tol:
            break
    return np.array(pts)


def path_length(P):
    P = np.asarray(P)
    return float(np.sum(np.hypot(*np.diff(P, axis=0).T)))


def min_clearance(P):
    return min(min(d for d, _ in clearance_vec(p)) for p in P)


def free(q):
    return min(d for d, _ in clearance_vec(q)) > 0


def u_grid(h=0.02):
    """The potential on a grid of spacing h over the room (np.inf inside the obstacle region). Returns xs, ys, U."""
    xs = np.arange(0, c.W + 1e-9, h)
    ys = np.arange(0, c.H + 1e-9, h)
    X, Y = np.meshgrid(xs, ys)
    pts = shapely.points(X.ravel(), Y.ravel())
    Ug = 0.5 * ZETA * ((X - GOAL[0]) ** 2 + (Y - GOAL[1]) ** 2)
    hit = np.zeros(X.shape, bool)
    for o in OBS:
        d = shapely.distance(o, pts).reshape(X.shape) - c.R
        hit |= d <= 0
        near = (d > 0) & (d <= QSTAR)
        Ug[near] += 0.5 * ETA * (1 / d[near] - 1 / QSTAR) ** 2
    Ug[hit] = np.inf
    return xs, ys, Ug


WALK_STEP = 0.05                         # random-walk step per coordinate (m)
WALK_LEN = (100, 400)                    # each walk's step limit is drawn evenly from this range
K_WALKS = 20                             # failed walks before backtracking


def random_walk(q0, u_stop, rng, n_steps):
    """Each step moves x and y by +-WALK_STEP (a coin toss each); a step into the obstacle region is thrown away
    and tried again. Stops early once U is below u_stop. Returns the points."""
    q = np.array(q0, float)
    pts = [q.copy()]
    for _ in range(n_steps):
        while True:
            nq = q + WALK_STEP * rng.choice([-1, 1], size=2)
            if 0 < nq[0] < c.W and 0 < nq[1] < c.H and free(nq):
                break
        q = nq
        pts.append(q.copy())
        if U(q) < u_stop:
            break
    return np.array(pts)


def randomized(q0, rng, max_walks=200):
    """The randomized potential field (LaValle 5.4.3): descend; when stuck, random walk, then descend again; after
    K_WALKS failed walks, restart from a random point of an earlier walk. Returns a list of (mode, points)."""
    parts = [("descend", descend(q0))]
    q = parts[-1][1][-1]
    fails, walk_pts, walks = 0, [], 0
    while np.hypot(*(q - GOAL)) > 0.05 and walks < max_walks:
        u_stuck = U(q)
        L = int(rng.integers(WALK_LEN[0], WALK_LEN[1] + 1))
        w = random_walk(q, u_stuck, rng, L)
        walks += 1
        walk_pts.extend(w[1:])
        parts.append(("walk", w))
        d = descend(w[-1])
        parts.append(("descend", d))
        if np.hypot(*(d[-1] - GOAL)) <= 0.05:
            q = d[-1]
            break
        if U(d[-1]) < u_stuck - 1e-6:
            fails, q = 0, d[-1]
            continue
        fails += 1
        q = d[-1]
        if fails >= K_WALKS:
            b = walk_pts[int(rng.integers(len(walk_pts)))]
            parts.append(("backtrack", np.array([q, b])))
            d = descend(b)
            parts.append(("descend", d))
            q, fails = d[-1], 0
    return parts


H_GRID = 0.05                            # harmonic potential: grid spacing (m)


def harmonic_setup(h=H_GRID):
    """Grid nodes over the room; free = the centre is in free space. The goal node (the doorway centre) is held at 0,
    obstacle nodes and the outside of the grid at 1. Returns xs, ys, free mask, goal index (j, i)."""
    xs = np.arange(0, c.W + 1e-9, h)
    ys = np.arange(0, c.H + 1e-9, h)
    X, Y = np.meshgrid(xs, ys)
    pts = shapely.points(X.ravel(), Y.ravel())
    d = np.min([shapely.distance(o, pts) for o in OBS], axis=0).reshape(X.shape) - c.R
    fr = d > 0
    g = (int(round(GOAL[1] / h)), int(round(GOAL[0] / h)))
    return xs, ys, fr, g


def harmonic_solve(h=H_GRID):
    """Exact solution of the grid equations: every free node equals the average of its four neighbours."""
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve
    xs, ys, fr, g = harmonic_setup(h)
    ny, nx = fr.shape
    unk = fr.copy()
    unk[g] = False
    idx = -np.ones(fr.shape, int)
    idx[unk] = np.arange(unk.sum())
    A = lil_matrix((unk.sum(), unk.sum()))
    b = np.zeros(unk.sum())
    for j, i in zip(*np.nonzero(unk)):
        k = idx[j, i]
        A[k, k] = 4
        for jj, ii in ((j - 1, i), (j + 1, i), (j, i - 1), (j, i + 1)):
            if 0 <= jj < ny and 0 <= ii < nx and unk[jj, ii]:
                A[k, idx[jj, ii]] = -1
            elif 0 <= jj < ny and 0 <= ii < nx and (jj, ii) == g:
                b[k] += 0.0
            else:
                b[k] += 1.0
    phi = np.ones(fr.shape)
    phi[unk] = spsolve(A.tocsr(), b)
    phi[g] = 0.0
    return xs, ys, fr, g, phi


def gauss_seidel(h=H_GRID, sweeps=(0, 1)):
    """Gauss-Seidel sweeps from phi = 1 everywhere except the goal (0): each free node in turn becomes the average of
    its four neighbours' latest values. Returns {sweep number: phi} for the requested sweep numbers."""
    xs, ys, fr, g = harmonic_setup(h)
    ny, nx = fr.shape
    P = np.ones((ny + 2, nx + 2))                  # padded: outside the grid stays 1
    P[g[0] + 1, g[1] + 1] = 0.0
    unk = fr.copy()
    unk[g] = False
    U2 = np.zeros((ny + 2, nx + 2), bool)
    U2[1:-1, 1:-1] = unk
    J, I = np.nonzero(U2)
    red = (J + I) % 2 == 0                         # red-black order: same result as one full Gauss-Seidel sweep order
    out = {}
    want = set(sweeps)
    for s in range(max(sweeps) + 1):
        if s in want:
            out[s] = P[1:-1, 1:-1].copy()
        for m in (red, ~red):
            j, i = J[m], I[m]
            P[j, i] = 0.25 * (P[j - 1, i] + P[j + 1, i] + P[j, i - 1] + P[j, i + 1])
    return xs, ys, fr, g, out


SW_C0, SW_R0 = np.array([3.5, 2.0]), 3.3       # sphere world: the free disk for the robot's centre
SW_OBS = [(np.array([4.2, 1.9]), 1.3),          # the table, grown by 0.25 m, as a disk of about its area
          (np.array([1.0, 3.0]), 0.35),         # the pink pole, grown by 0.25 m
          (np.array([6.0, 0.8]), 0.35)]         # the green pole, grown by 0.25 m


def _rk_parts(q):
    q = np.asarray(q, float)
    gam = np.sum((q - GOAL) ** 2, axis=-1)
    dgam = 2 * (q - GOAL)
    bs = [SW_R0 ** 2 - np.sum((q - SW_C0) ** 2, axis=-1)] + [np.sum((q - cc) ** 2, axis=-1) - r ** 2 for cc, r in SW_OBS]
    dbs = [-2 * (q - SW_C0)] + [2 * (q - cc) for cc, _ in SW_OBS]
    beta = np.prod(bs, axis=0)
    dbeta = sum(db * np.asarray(np.prod([bb for m, bb in enumerate(bs) if m != k], axis=0))[..., None]
                for k, db in enumerate(dbs))
    inside = np.all([bb > 0 for bb in bs], axis=0)
    return gam, dgam, beta, dbeta, inside


def rk(q, kappa):
    """Rimon-Koditschek navigation function on the sphere world: gamma / (gamma^kappa + beta)^(1/kappa), with gamma
    the squared distance to the goal and beta the product of the obstacle functions, each 0 on its boundary."""
    gam, _, beta, _, inside = _rk_parts(q)
    with np.errstate(invalid="ignore", divide="ignore"):
        phi = gam / (gam ** kappa + beta) ** (1 / kappa)
    return np.where(inside, phi, np.nan)


def rk_grad(q, kappa):
    gam, dgam, beta, dbeta, _ = _rk_parts(q)
    S = gam ** kappa + beta
    gam, S = np.asarray(gam)[..., None], np.asarray(S)[..., None]
    return dgam * S ** (-1 / kappa) - (1 / kappa) * gam * S ** (-1 / kappa - 1) * (kappa * gam ** (kappa - 1) * dgam + dbeta)


def rk_descend(q0, kappa, step=0.01, n_max=4000, goal_tol=0.02):
    """Gradient descent on the navigation function with steps of fixed length 0.01 m (its gradient is tiny where it
    is flat). Stops at the goal, or when the direction turns back (a minimum)."""
    q = np.array(q0, float)
    pts = [q.copy()]
    last = None
    for _ in range(n_max):
        g = rk_grad(q, kappa)
        n = np.hypot(*g)
        if n == 0:
            break
        d = -g / n
        if last is not None and d @ last < -0.5:
            break
        q = q + step * d
        pts.append(q.copy())
        last = d
        if np.hypot(*(q - GOAL)) < goal_tol:
            break
    return np.array(pts)


def grid_descent(phi, fr, start, h=H_GRID, goal=None):
    """Steepest descent on the grid: from the node nearest the start, step to the lowest of the 8 neighbouring free
    nodes while it is lower. Returns the visited points (m) and whether the goal node was reached."""
    ny, nx = fr.shape
    j, i = int(round(start[1] / h)), int(round(start[0] / h))
    g = goal or (int(round(GOAL[1] / h)), int(round(GOAL[0] / h)))
    pts = [(i * h, j * h)]
    while (j, i) != g:
        best, bj, bi = phi[j, i], None, None
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                jj, ii = j + dj, i + di
                if (dj or di) and 0 <= jj < ny and 0 <= ii < nx and fr[jj, ii] and phi[jj, ii] < best:
                    best, bj, bi = phi[jj, ii], jj, ii
        if bj is None:
            return np.array(pts), False
        j, i = bj, bi
        pts.append((i * h, j * h))
    return np.array(pts), True


SADDLES = [(2.924, 0.601), (5.167, 0.632), (0.521, 2.842)]     # found with a root finder in the notebook
TRAP = (3.600, 0.593)                                          # the one local minimum other than the doorway


def shortest_route(a=START2, b=GOAL, margin=0.001, quad=16):
    """Length of the shortest route between a and b in free space: a visibility graph over the corners of the
    obstacles grown by 0.25 m (+ a hair), searched with Dijkstra's algorithm. Returns (length, points)."""
    import heapq
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    grown = unary_union([p.buffer(c.R + margin, quad_segs=quad) for p in c.pieces()])
    test = unary_union([p.buffer(c.R, quad_segs=64) for p in c.pieces()])
    shapely.prepare(test)
    verts = [np.array(a), np.array(b)]
    for g in getattr(grown, "geoms", [grown]):
        for ring in [g.exterior] + list(g.interiors):
            for x, y in list(ring.coords)[:-1]:
                if 0 < x < c.W and 0 < y < c.H and not test.intersects(Point(x, y)):
                    verts.append(np.array([x, y]))
    V = np.array(verts)
    n = len(V)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if not test.intersects(LineString([V[i], V[j]])):
                d = float(np.hypot(*(V[i] - V[j])))
                adj[i].append((j, d))
                adj[j].append((i, d))
    dist, prev, pq = [np.inf] * n, [-1] * n, [(0.0, 0)]
    dist[0] = 0.0
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v], prev[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    path, k = [], 1
    while k != -1:
        path.append(V[k])
        k = prev[k]
    return dist[1], np.array(path[::-1])
