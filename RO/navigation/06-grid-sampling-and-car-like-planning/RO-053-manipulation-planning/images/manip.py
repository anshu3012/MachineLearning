"""The arm, the cup and the table of this Note (no output when run on its own). Side view of one vertical plane.

The arm is the 2R arm of RO-036: link 1 of 0.3 m turns about the shoulder at (0, 0), link 2 of 0.2 m turns about the
elbow; theta1 is measured from the horizontal, theta2 from the direction of link 1 (both in degrees here). A suction
gripper at the hand holds the cup by its lid, and a wrist keeps the cup upright, so a held cup hangs straight below the
hand. The table top is 0.1 m below the shoulder; the robot's body is level with it, so everything below y = -0.1 m is
solid. A bottle 0.14 m tall stands between the cup's spot A and its goal spot B.

Modes (Hauser ch.12, "Multi-modal motion planning"; LaValle 7.3.2): in a transit mode the cup rests at a spot and is
an obstacle; in the transfer mode it hangs from the hand and moves with it. Each mode has its own free space."""
import heapq

import numpy as np
import shapely
from scipy.spatial import cKDTree
from shapely.geometry import LineString, box

L1, L2 = 0.3, 0.2                     # link lengths (m), as in RO-036
TOP = -0.10                           # height of the table top and of the robot's top (m)
CUP_W, CUP_H = 0.06, 0.08             # the cup: width and height (m)
A_X, B_X = 0.18, 0.42                 # centre lines of the cup's spots A and B (m)
BOTTLE = (0.31, 0.35, TOP, 0.04)      # x0, x1, y0, y1 (m): 0.14 m tall
HOME = (90.0, 0.0)                    # the arm straight up
TOUCH = 1e-3                          # touching is allowed (at a grasp or a placing), overlapping is not (m)


def floor():
    return box(-1.0, -1.0, 1.0, TOP)


def bottle():
    return box(*[BOTTLE[i] for i in (0, 2, 1, 3)])


def cup_at(xc, ybottom=TOP):
    """The cup standing with its bottom centre at (xc, ybottom)."""
    return box(xc - CUP_W / 2, ybottom, xc + CUP_W / 2, ybottom + CUP_H)


def held_cup(hand):
    """The cup hanging below the hand: its lid's centre at the hand."""
    return box(hand[0] - CUP_W / 2, hand[1] - CUP_H, hand[0] + CUP_W / 2, hand[1])


def lid(xc):
    """Where the hand must be to hold the cup standing at xc: the centre of its lid."""
    return (xc, TOP + CUP_H)


def fk(t1, t2):
    """Elbow and hand for joint angles in degrees (arrays allowed)."""
    a1, a12 = np.radians(t1), np.radians(np.asarray(t1) + np.asarray(t2))
    ex, ey = L1 * np.cos(a1), L1 * np.sin(a1)
    return (ex, ey), (ex + L2 * np.cos(a12), ey + L2 * np.sin(a12))


def ik(p):
    """Both joint-angle solutions (degrees) that put the hand at p."""
    x, y = p
    c2 = (x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    out = []
    for s in (1, -1):
        t2 = s * np.degrees(np.arccos(np.clip(c2, -1, 1)))
        k1, k2 = L1 + L2 * np.cos(np.radians(t2)), L2 * np.sin(np.radians(t2))
        t1 = np.degrees(np.arctan2(y, x) - np.arctan2(k2, k1))
        out.append((wrap(t1), wrap(t2)))
    return out


def wrap(t):
    return (np.asarray(t) + 180.0) % 360.0 - 180.0


def obstacles(mode):
    """Obstacles for the links in each mode: 'transit A', 'transit B', 'transfer', or 'arm' (the arm alone, as if
    the cup did not exist)."""
    obs = [floor(), bottle()]
    if mode == "transit A":
        obs.append(cup_at(A_X).buffer(-TOUCH))
    if mode == "transit B":
        obs.append(cup_at(B_X).buffer(-TOUCH))
    return shapely.union_all(obs)


def collide(t1, t2, mode):
    """True where the arm (and, in transfer, the cup it holds) overlaps an obstacle. Arrays of angles in degrees."""
    t1, t2 = np.atleast_1d(t1).astype(float), np.atleast_1d(t2).astype(float)
    (ex, ey), (hx, hy) = fk(t1, t2)
    O = obstacles(mode)
    shapely.prepare(O)
    z = np.zeros_like(t1)
    link1 = shapely.linestrings(np.stack([np.stack([z, z], 1), np.stack([ex, ey], 1)], 1))
    link2 = shapely.linestrings(np.stack([np.stack([ex, ey], 1), np.stack([hx, hy], 1)], 1))
    hit = shapely.intersects(O, link1) | shapely.intersects(O, link2)
    if mode == "transfer":
        cups = shapely.box(hx - CUP_W / 2, hy - CUP_H, hx + CUP_W / 2, hy)
        env = shapely.union_all([floor().buffer(-TOUCH), bottle()])
        shapely.prepare(env)
        hit |= shapely.intersects(env, cups) | shapely.intersects(cups, link1)
    return hit


def cspace_grid(mode, step=1.0):
    """Collision mask on a grid of joint angles from -180 to 180 degrees: rows theta2, columns theta1."""
    g = np.arange(-180, 180 + 1e-9, step)
    T1, T2 = np.meshgrid(g, g)
    return g, collide(T1.ravel(), T2.ravel(), mode).reshape(T1.shape)


def angdiff(a, b):
    return wrap(np.asarray(b) - np.asarray(a))


def dist(a, b):
    """Distance between two configurations on the torus: each joint the short way round (RO-038), in degrees."""
    d = angdiff(a, b)
    return float(np.hypot(*d)) if np.ndim(d) == 1 else np.hypot(d[..., 0], d[..., 1])


def interp(a, b, n):
    d = angdiff(a, b)
    t = np.linspace(0, 1, n)[:, None]
    return wrap(np.asarray(a) + t * d)


def seg_free(a, b, mode, step=1.0):
    """Edge resolution in joint space: configurations at most `step` degrees apart along the short way round."""
    n = max(2, int(np.ceil(dist(a, b) / step)) + 1)
    P = interp(a, b, n)
    return not collide(P[:, 0], P[:, 1], mode).any()


def prm_plan(mode, s, g, n=150, k=10, seed=0):
    """The PRM of RO-052 in the arm's C-space (a torus): n free milestones, k nearest by the wrap-around distance,
    then A* from s to g. Returns (path of configurations, length in degrees, milestones, edges)."""
    rng = np.random.default_rng(seed)
    V = []
    while len(V) < n:
        q = rng.uniform(-180, 180, 2)
        if not collide(q[0], q[1], mode)[0]:
            V.append(tuple(q))
    V = V + [tuple(s), tuple(g)]
    A = np.asarray(V)
    # the torus: copy every milestone 360 degrees to each side, so the k-d tree sees across the cut
    off = np.array([(i, j) for i in (-360, 0, 360) for j in (-360, 0, 360)])
    big = (A[None, :, :] + off[:, None, :]).reshape(-1, 2)
    tree = cKDTree(big)
    E, tried = {}, set()
    for i in range(len(V)):
        _, idx = tree.query(A[i], k=k + 1)
        for jj in idx[1:]:
            j = jj % len(V)
            key = (min(i, j), max(i, j))
            if j == i or key in tried:
                continue
            tried.add(key)
            if seg_free(V[i], V[j], mode):
                E[key] = dist(V[i], V[j])
    nbr = {i: [] for i in range(len(V))}
    for (i, j), d in E.items():
        nbr[i].append((j, d))
        nbr[j].append((i, d))
    si, gi = len(V) - 2, len(V) - 1
    best, par, pq, done = {si: 0.0}, {si: None}, [(dist(V[si], V[gi]), si)], set()
    while pq:
        _, i = heapq.heappop(pq)
        if i in done:
            continue
        done.add(i)
        if i == gi:
            break
        for j, d in nbr[i]:
            if best[i] + d < best.get(j, np.inf):
                best[j], par[j] = best[i] + d, i
                heapq.heappush(pq, (best[j] + dist(V[j], V[gi]), j))
    if gi not in done:
        return None, np.inf, V, E
    path = [gi]
    while par[path[-1]] is not None:
        path.append(par[path[-1]])
    return [V[i] for i in path[::-1]], best[gi], V, E


def shortcut(path, mode, rounds=200, seed=0):
    """Shorten a path by trying straight joint-space segments between random pairs of its points."""
    rng = np.random.default_rng(seed)
    P = [tuple(p) for p in path]
    for _ in range(rounds):
        if len(P) < 3:
            break
        i, j = sorted(rng.choice(len(P), 2, replace=False))
        if j - i < 2:
            continue
        if seg_free(P[i], P[j], mode):
            P = P[:i + 1] + P[j:]
    return P


def densify(path, step=2.0):
    """Configurations along a path at most `step` degrees apart (for drawing and animating)."""
    out = [tuple(path[0])]
    for a, b in zip(path, path[1:]):
        n = max(2, int(np.ceil(dist(a, b) / step)) + 1)
        out += [tuple(p) for p in interp(a, b, n)[1:]]
    return out


def cause_grid(mode, step=1.0):
    """Like cspace_grid, but each blocked configuration is coded by what it hits: 1 the table or the robot's top,
    2 the bottle, 3 the cup standing at A or B (transit modes); in transfer the held cup counts with what it hits.
    Rows theta2, columns theta1."""
    g = np.arange(-180, 180 + 1e-9, step)
    T1, T2 = np.meshgrid(g, g)
    t1, t2 = T1.ravel(), T2.ravel()
    (ex, ey), (hx, hy) = fk(t1, t2)
    z = np.zeros_like(t1)
    link1 = shapely.linestrings(np.stack([np.stack([z, z], 1), np.stack([ex, ey], 1)], 1))
    link2 = shapely.linestrings(np.stack([np.stack([ex, ey], 1), np.stack([hx, hy], 1)], 1))
    hit = lambda geom, *parts: np.any([shapely.intersects(geom, p) for p in parts], axis=0)
    parts = [link1, link2]
    code = np.zeros(len(t1), int)
    if mode == "transfer":
        cups = shapely.box(hx - CUP_W / 2, hy - CUP_H, hx + CUP_W / 2, hy)
        code[hit(floor(), *parts) | shapely.intersects(floor().buffer(-TOUCH), cups)] = 1
        code[hit(bottle(), *parts, cups)] = 2
        code[(code == 0) & shapely.intersects(cups, link1)] = 3
    else:
        code[hit(floor(), *parts)] = 1
        code[hit(bottle(), *parts)] = 2
        xc = A_X if mode == "transit A" else B_X
        code[hit(cup_at(xc).buffer(-TOUCH), *parts)] = 3
    return g, code.reshape(T1.shape)
