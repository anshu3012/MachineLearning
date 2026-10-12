"""Probabilistic roadmaps on the room of RO-009 (no output when run on its own). The robot is the 0.25 m disk of
RO-037, so its C-space is the floor (x, y) and its obstacle region is every obstacle grown by 0.25 m (cspace.py).
A world for a wider robot (the same robot carrying a round tray, radius 0.5 m) gives the narrow passage.

Pieces: free tests and segment checks that count every configuration checked (edge resolution of RO-038: points
at most EPS apart, checked in halving order, stopping at the first collision); the basic PRM in two phases (sample N
free milestones, then try each milestone's k nearest neighbours, MR 10.5.2); the query phase with A*; the
visibility roadmap (guards and connectors, LaValle 5.6.2); Gaussian and bridge-test sampling (LaValle 5.6.3);
and lazy collision checking (Hauser ch.10)."""
import heapq
from math import ceil

import numpy as np
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from shapely.geometry import LineString

import cspace as c

START = (2.0, 1.0)                 # the robot's dock (RO-009)
DOOR = (3.6, 4.0)                  # the doorway centre (RO-037)
CABINET = (5.9, 2.0)               # beside the cabinet
CORNER = (6.6, 0.4)                # the corner behind the green pole
TRIPS = [("dock", START, "door", DOOR), ("door", DOOR, "cabinet", CABINET),
         ("cabinet", CABINET, "corner", CORNER), ("corner", CORNER, "dock", START)]
EPS = 0.05                         # longest step between two checked configurations on an edge (m)
K = 10                             # neighbours tried per milestone
BOX = (0.0, 0.0, c.W, c.H)         # the sampling box: the room's floor


def halving(n):
    """Indexes 0..n of n equal steps in halving order: both ends, the middle, the quarter points, ..."""
    out, seen, todo = [0, n], {0, n}, [(0, n)]
    while todo:
        nxt = []
        for lo, hi in todo:
            if hi - lo < 2:
                continue
            m = (lo + hi) // 2
            if m not in seen:
                out.append(m)
                seen.add(m)
            nxt += [(lo, m), (m, hi)]
        todo = nxt
    return out


class World:
    """The room for a disk robot of radius r: its obstacle region, a free test and a counted segment check."""

    def __init__(self, r=c.R):
        self.r = r
        self.cobs = c.cobs_disk(r)
        shapely.prepare(self.cobs)
        self.checks = 0                                     # configurations checked so far

    def free_xy(self, xs, ys):
        xs, ys = np.atleast_1d(xs), np.atleast_1d(ys)
        inside = (xs >= 0) & (xs <= c.W) & (ys >= 0) & (ys <= c.H + 0.5)
        return inside & ~shapely.intersects_xy(self.cobs, xs, ys)

    def free(self, q, count=True):
        if count:
            self.checks += 1
        return bool(self.free_xy(q[0], q[1])[0])

    def seg_points(self, a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        n = max(1, ceil(np.linalg.norm(b - a) / EPS - 1e-9))
        t = np.arange(n + 1) / n
        return a + t[:, None] * (b - a), halving(n)

    def seg_free(self, a, b, count=True):
        """Edge resolution: check points at most EPS apart in halving order; stop at the first collision.
        Returns (free, number of configurations checked)."""
        P, order = self.seg_points(a, b)
        ok = self.free_xy(P[:, 0], P[:, 1])
        bad = [i for i, j in enumerate(order) if not ok[j]]
        used = len(order) if not bad else bad[0] + 1
        if count:
            self.checks += used
        return not bad, used

    def seg_free_exact(self, a, b):
        return not self.cobs.intersects(LineString([a, b]))

    def sample(self, rng):
        """One uniform sample of the box; returns (q, free)."""
        q = (rng.uniform(BOX[0], BOX[2]), rng.uniform(BOX[1], BOX[3]))
        return q, self.free(q)


def sample_free(world, rng, n, log=None):
    """Phase 1: draw uniform samples until n are free. log gets (q, free) for every draw."""
    V = []
    while len(V) < n:
        q, ok = world.sample(rng)
        if log is not None:
            log.append((q, ok))
        if ok:
            V.append(q)
    return V


def connect(world, V, k=K, log=None):
    """Phase 2 (MR 10.5.2): for each milestone, try a straight edge to each of its k nearest milestones; an edge is
    added if edge resolution finds it free. Each pair is tried once. log gets (i, j, free, checks)."""
    V = np.asarray(V)
    tree = cKDTree(V)
    tried, E = set(), []
    for i in range(len(V)):
        _, idx = tree.query(V[i], k=min(k + 1, len(V)))
        for j in idx[1:]:
            key = (min(i, j), max(i, j))
            if key in tried:
                continue
            tried.add(key)
            ok, used = world.seg_free(V[i], V[j])
            if log is not None:
                log.append((key[0], key[1], ok, used))
            if ok:
                E.append(key)
    return E


def build(world, rng, n, k=K):
    V = sample_free(world, rng, n)
    return V, connect(world, V, k)


def components(nv, E):
    if not E:
        return nv, np.arange(nv)
    a = np.array(E)
    M = coo_matrix((np.ones(len(a)), (a[:, 0], a[:, 1])), shape=(nv, nv))
    return connected_components(M, directed=False)


def astar(V, E, s, g):
    """A* on the roadmap with straight-line edge costs and the straight-line distance to g as heuristic.
    Returns (vertex list, length, expanded count) or (None, inf, expanded)."""
    V = np.asarray(V)
    nbr = {i: [] for i in range(len(V))}
    for i, j in E:
        d = float(np.linalg.norm(V[i] - V[j]))
        nbr[i].append((j, d))
        nbr[j].append((i, d))
    h = lambda i: float(np.linalg.norm(V[i] - V[g]))
    gbest, parent, done = {s: 0.0}, {s: None}, set()
    pq = [(h(s), s)]
    while pq:
        _, i = heapq.heappop(pq)
        if i in done:
            continue
        done.add(i)
        if i == g:
            path = [i]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return path[::-1], gbest[g], len(done)
        for j, d in nbr[i]:
            if gbest[i] + d < gbest.get(j, np.inf):
                gbest[j], parent[j] = gbest[i] + d, i
                heapq.heappush(pq, (gbest[j] + h(j), j))
    return None, np.inf, len(done)


def query(world, V, E, s, g, k=K, log=None):
    """Query phase: try straight edges from s and from g to their k nearest milestones, then A* on the joined graph.
    Returns (path as points or None, length, edges added for s and g)."""
    V = list(map(tuple, V))
    tree = cKDTree(np.asarray(V))
    VV, EE, extra = V + [tuple(s), tuple(g)], list(E), []
    for qi, q in ((len(V), s), (len(V) + 1, g)):
        _, idx = tree.query(q, k=min(k, len(V)))
        for j in np.atleast_1d(idx):
            ok, used = world.seg_free(q, V[j])
            if log is not None:
                log.append((qi, j, ok, used))
            if ok:
                EE.append((j, qi))
                extra.append((qi, j))
    path, L, _ = astar(VV, EE, len(V), len(V) + 1)
    return ([VV[i] for i in path] if path else None), L, extra


def visible_share(world, q, h=0.05):
    """Share of the free floor that sees q along a free straight segment (on a grid of spacing h)."""
    xs, ys = np.meshgrid(np.arange(h / 2, c.W, h), np.arange(h / 2, c.H, h))
    xs, ys = xs.ravel(), ys.ravel()
    ok = world.free_xy(xs, ys)
    xs, ys = xs[ok], ys[ok]
    segs = shapely.linestrings(np.stack([np.stack([xs, ys], 1), np.tile(q, (len(xs), 1))], 1))
    vis = ~shapely.intersects(world.cobs, segs)
    return float(vis.mean()), xs, ys, vis


def accessible_share(world, V, k=K, h=0.1):
    """Share of the free floor (grid of spacing h) that reaches one of its k nearest milestones by a free segment."""
    xs, ys = np.meshgrid(np.arange(h / 2, c.W, h), np.arange(h / 2, c.H, h))
    xs, ys = xs.ravel(), ys.ravel()
    ok = world.free_xy(xs, ys)
    P = np.stack([xs[ok], ys[ok]], 1)
    V = np.asarray(V)
    _, idx = cKDTree(V).query(P, k=min(k, len(V)))
    idx = idx.reshape(len(P), -1)
    acc = np.zeros(len(P), bool)
    for col in range(idx.shape[1]):
        todo = ~acc
        segs = shapely.linestrings(np.stack([P[todo], V[idx[todo, col]]], 1))
        acc[np.where(todo)[0][~shapely.intersects(world.cobs, segs)]] = True
    return float(acc.mean()), P, acc


# ---- sampling strategies for narrow passages (LaValle 5.6.3; Hauser ch.10; WPI RBE550 L11)
def gaussian_sample(world, rng, sigma):
    """Gaussian sampling: q1 uniform, q2 = q1 plus normal noise of standard deviation sigma in x and y;
    keep the free one if exactly one of the two is free. Returns (q kept or None, q1, q2)."""
    q1 = (rng.uniform(BOX[0], BOX[2]), rng.uniform(BOX[1], BOX[3]))
    q2 = (q1[0] + rng.normal(0, sigma), q1[1] + rng.normal(0, sigma))
    f1, f2 = world.free(q1), world.free(q2)
    if f1 != f2:
        return (q1 if f1 else q2), q1, q2
    return None, q1, q2


def bridge_sample(world, rng, sigma):
    """Bridge test: q1 uniform; if q1 collides, q2 = q1 plus normal noise; if q2 collides too, keep the midpoint
    m if it is free. Returns (m or None, q1, q2, m)."""
    q1 = (rng.uniform(BOX[0], BOX[2]), rng.uniform(BOX[1], BOX[3]))
    if world.free(q1):
        return None, q1, None, None
    q2 = (q1[0] + rng.normal(0, sigma), q1[1] + rng.normal(0, sigma))
    if world.free(q2):
        return None, q1, q2, None
    m = ((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2)
    return (m if world.free(m) else None), q1, q2, m


def sample_strategy(world, rng, n, strategy, sigma=0.3, mix=0.5):
    """n milestones by one strategy: 'uniform', 'gaussian', or 'bridge' (a share mix of bridge-test milestones,
    the rest uniform, as bridge-test planners mix them, Hsu et al. 2003). Returns (milestones, draws)."""
    V, draws = [], 0
    while len(V) < n:
        draws += 1
        if strategy == "uniform" or (strategy == "bridge" and rng.uniform() > mix):
            q, ok = world.sample(rng)
            if ok:
                V.append(q)
        elif strategy == "gaussian":
            q = gaussian_sample(world, rng, sigma)[0]
            if q is not None:
                V.append(q)
        else:
            q = bridge_sample(world, rng, sigma)[0]
            if q is not None:
                V.append(q)
    return V, draws


# ---- visibility roadmap (LaValle 5.6.2): guards see no other guard; connectors see guards of two components
def visibility_roadmap(world, rng, n_samples, log=None):
    guards, comp, conns, E = [], [], [], []            # comp[i]: component label of guard i
    G = lambda: np.asarray(guards)
    for _ in range(n_samples):
        q, ok = world.sample(rng)
        if not ok:
            if log is not None:
                log.append(("collision", q, []))
            continue
        seen = []
        for i, gq in enumerate(guards):
            free, _ = world.seg_free(q, gq)
            if free:
                seen.append(i)
        labels = sorted({comp[i] for i in seen})
        if not seen:
            guards.append(q)
            comp.append(max(comp, default=-1) + 1)
            kind, links = "guard", []
        elif len(labels) >= 2:
            links = [next(i for i in seen if comp[i] == lab) for lab in labels]
            conns.append(q)
            keep = labels[0]
            for i in range(len(comp)):
                if comp[i] in labels:
                    comp[i] = keep
            E += [(q, guards[i]) for i in links]
            kind = "connector"
        else:
            kind, links = "discarded", seen
        if log is not None:
            log.append((kind, q, [guards[i] for i in links] if kind != "discarded" else [guards[i] for i in seen]))
    return guards, conns, E, comp


# ---- lazy collision checking (Hauser ch.10, "Lazy collision checking in PRMs")
def lazy_query(world, V, k, s, g, log=None):
    """Lazy PRM: join each milestone (and s, g) to its k nearest without checking edges; search; check only the
    edges of the found path, from the start; delete a colliding edge and search again. Returns (path points, length,
    number of edges checked, number of searches)."""
    VV = [tuple(p) for p in V] + [tuple(s), tuple(g)]
    A = np.asarray(VV)
    tree = cKDTree(A)
    E = set()
    for i in range(len(A)):
        _, idx = tree.query(A[i], k=min(k + 1, len(A)))
        for j in idx[1:]:
            E.add((min(i, j), max(i, j)))
    s_i, g_i = len(VV) - 2, len(VV) - 1
    known_ok, checked, searches = set(), 0, 0
    while True:
        searches += 1
        path, L, _ = astar(VV, sorted(E), s_i, g_i)
        if path is None:
            return None, np.inf, checked, searches
        bad = None
        for a, b in zip(path, path[1:]):
            key = (min(a, b), max(a, b))
            if key in known_ok:
                continue
            ok, used = world.seg_free(VV[a], VV[b])
            checked += 1
            if log is not None:
                log.append((searches, [VV[i] for i in path], key, ok))
            if ok:
                known_ok.add(key)
            else:
                bad = key
                break
        if bad is None:
            return [VV[i] for i in path], L, checked, searches
        E.discard(bad)
