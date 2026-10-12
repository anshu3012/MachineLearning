"""Sampling-based planners for this Note (no output when run on its own): the disk robot's C-space of the room
(cspace.py: obstacles grown by 0.25 m), segment checking by edge resolution (RO-038), RRT, a random-walk tree,
RRT*, RRT-Connect, and the shortest route by a visibility graph for comparison."""
import heapq

import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon

import cspace as c

START = np.array([4.0, 0.5])             # between the table and the bottom wall, where gradient descent got stuck
GOAL = np.array(c.GOAL)                  # the doorway centre (3.6, 4.0)
ETA = 0.5                                # longest step of steer (m)
EPS = 0.05                               # edge resolution: segment check points at most this far apart (m)
GOAL_BIAS = 0.05                         # chance that a sample is the goal itself
BOX = (0.0, c.W, 0.0, c.H)               # samples are drawn evenly over the room's floor
COBS = c.cobs_disk()
shapely.prepare(COBS)


class Counter:
    checks = 0                           # configurations tested for collision


def free_pts(P):
    P = np.atleast_2d(P)
    Counter.checks += len(P)
    inside = (P[:, 0] > 0) & (P[:, 0] < c.W) & (P[:, 1] > 0) & (P[:, 1] < c.H + 0.3)
    return inside & ~shapely.intersects_xy(COBS, P[:, 0], P[:, 1])


def free(q):
    return bool(free_pts(q)[0])


def seg_free(a, b):
    """Edge resolution: test n + 1 evenly spaced points, n = ceil(length / EPS)."""
    L = float(np.hypot(*(b - a)))
    n = max(1, int(np.ceil(L / EPS)))
    t = np.linspace(0, 1, n + 1)[:, None]
    return bool(np.all(free_pts(a + t * (b - a))))


def steer(q_near, q_rand, eta=ETA):
    d = q_rand - q_near
    L = float(np.hypot(*d))
    return q_rand.copy() if L <= eta else q_near + eta * d / L


def sample(rng, bias=GOAL_BIAS):
    if rng.random() < bias:
        return GOAL.copy(), True
    return np.array([rng.uniform(BOX[0], BOX[1]), rng.uniform(BOX[2], BOX[3])]), False


def path_from(nodes, parent, k):
    out = []
    while k != -1:
        out.append(nodes[k])
        k = parent[k]
    return np.array(out[::-1])


def length(P):
    P = np.asarray(P)
    return float(np.sum(np.hypot(*np.diff(P, axis=0).T)))


def rrt(rng, n_max=5000, stop_at_goal=True, log=False, bias=GOAL_BIAS, n_nodes=None):
    """Plain RRT (LaValle 5.5; MR 10.5): sample, nearest node, steer at most ETA, check the edge, add it.
    The goal is joined once a new node is within ETA of it and that last edge is free.
    Returns dict(nodes, parent, goal index or None, samples used, events if log)."""
    nodes, parent = [START.copy()], [-1]
    events, goal_k = [], None
    for i in range(1, n_max + 1):
        if n_nodes is not None and len(nodes) >= n_nodes:
            break
        q_rand, is_goal = sample(rng, bias)
        N = np.array(nodes)
        k = int(np.argmin(np.hypot(*(N - q_rand).T)))
        q_new = steer(nodes[k], q_rand)
        ok = free(q_new) and seg_free(nodes[k], q_new)
        if log:
            events.append(dict(i=i, q_rand=q_rand, goal_sample=is_goal, near=k, q_new=q_new, ok=ok))
        if not ok:
            continue
        nodes.append(q_new)
        parent.append(k)
        if goal_k is None and np.hypot(*(q_new - GOAL)) <= ETA and seg_free(q_new, GOAL):
            nodes.append(GOAL.copy())
            parent.append(len(nodes) - 2)
            goal_k = len(nodes) - 1
            if log:
                events[-1]["goal"] = True
            if stop_at_goal:
                return dict(nodes=np.array(nodes), parent=parent, goal=goal_k, samples=i, events=events)
    return dict(nodes=np.array(nodes), parent=parent, goal=goal_k, samples=i, events=events)


def coverage(nodes, r=0.5):
    """Share of the free space within r of some node of the tree (on a 0.05 m grid of free points)."""
    xs = np.arange(0.025, c.W, 0.05)
    ys = np.arange(0.025, c.H, 0.05)
    X, Y = np.meshgrid(xs, ys)
    F = ~shapely.intersects_xy(COBS, X, Y)
    P = np.c_[X[F], Y[F]]
    N = np.asarray(nodes)
    near = np.zeros(len(P), bool)
    for k in range(0, len(N), 200):
        near |= (np.hypot(P[:, None, 0] - N[None, k:k + 200, 0], P[:, None, 1] - N[None, k:k + 200, 1]) <= r).any(1)
    return float(near.mean())


def walk_tree(rng, n_nodes):
    """The random-walk tree of MR 10.5: pick a random node of the tree and step ETA in a random direction."""
    nodes, parent = [START.copy()], [-1]
    while len(nodes) < n_nodes:
        k = int(rng.integers(len(nodes)))
        a = rng.uniform(0, 2 * np.pi)
        q_new = nodes[k] + ETA * np.array([np.cos(a), np.sin(a)])
        if free(q_new) and seg_free(nodes[k], q_new):
            nodes.append(q_new)
            parent.append(k)
    return dict(nodes=np.array(nodes), parent=parent)


def free_area():
    xs = np.arange(0.005, c.W, 0.01)
    ys = np.arange(0.005, c.H, 0.01)
    X, Y = np.meshgrid(xs, ys)
    return float((~shapely.intersects_xy(COBS, X, Y)).sum() * 1e-4)


GAMMA = 4.0                              # Karaman-Frazzoli lower bound for d = 2 is 3.79 here (free area 15.0 m²)


def radius(n, gamma=None, eta=ETA):
    g = GAMMA if gamma is None else gamma
    return min(g * np.sqrt(np.log(n) / n), eta) if n > 1 else eta


def rrt_star(rng, n_max=2000, record=(), log=False):
    """RRT* (Karaman and Frazzoli 2011, Algorithm 6): as RRT, but the new node takes as parent the near node (within
    radius(n)) that gives it the cheapest cost from the start, and then each near node is rewired through the new
    node when that is cheaper. The goal is a node like any other once reached. record: sample counts at which the
    best cost to the goal is stored."""
    nodes, parent, cost = [START.copy()], [-1], [0.0]
    goal_k, best = None, {}
    events = []
    for i in range(1, n_max + 1):
        q_rand, is_goal = sample(rng)
        N = np.array(nodes)
        dist = np.hypot(*(N - q_rand).T)
        k = int(np.argmin(dist))
        q_new = steer(nodes[k], q_rand)
        ev = dict(i=i, q_rand=q_rand, near=k, q_new=q_new, ok=False, rewired=[], parent=None, r=None)
        if free(q_new) and seg_free(nodes[k], q_new):
            n = len(nodes)
            r = radius(n + 1)
            dn = np.hypot(*(N - q_new).T)
            near = [int(j) for j in np.nonzero(dn <= r + 1e-12)[0]]
            p, cmin = k, cost[k] + float(dn[k])
            for j in near:
                cj = cost[j] + float(dn[j])
                if cj < cmin - 1e-12 and seg_free(nodes[j], q_new):
                    p, cmin = j, cj
            nodes.append(q_new)
            parent.append(p)
            cost.append(cmin)
            new = len(nodes) - 1
            ev.update(ok=True, parent=p, r=r, near_set=near, new=new)
            for j in near:
                if j == p:
                    continue
                cj = cmin + float(dn[j])
                if cj < cost[j] - 1e-12 and seg_free(q_new, nodes[j]):
                    old = parent[j]
                    parent[j] = new
                    delta = cost[j] - cj
                    _lower(parent, cost, j, delta)
                    ev["rewired"].append((j, old))
            if goal_k is None and np.hypot(*(q_new - GOAL)) < 1e-9:
                goal_k = new
        if log:
            ev["goal_cost"] = cost[goal_k] if goal_k is not None else None
            events.append(ev)
        if i in record:
            best[i] = cost[goal_k] if goal_k is not None else np.inf
    return dict(nodes=np.array(nodes), parent=parent, cost=np.array(cost), goal=goal_k, best=best, events=events)


def _lower(parent, cost, j, delta):
    """Lower the cost of node j and of every node below it in the tree by delta."""
    kids = {}
    for a, b in enumerate(parent):
        kids.setdefault(b, []).append(a)
    stack = [j]
    while stack:
        a = stack.pop()
        cost[a] -= delta
        stack.extend(kids.get(a, []))


def rrt_best(rng, record):
    """RRT that keeps growing after the first route and keeps the best route to the goal found so far (MR 10.5).
    Every new node within ETA of the goal with a free last edge offers a route."""
    nodes, parent, cost = [START.copy()], [-1], [0.0]
    best, out = np.inf, {}
    for i in range(1, max(record) + 1):
        q_rand, _ = sample(rng)
        N = np.array(nodes)
        k = int(np.argmin(np.hypot(*(N - q_rand).T)))
        q_new = steer(nodes[k], q_rand)
        if free(q_new) and seg_free(nodes[k], q_new):
            nodes.append(q_new)
            parent.append(k)
            cost.append(cost[k] + float(np.hypot(*(q_new - nodes[k]))))
            dg = float(np.hypot(*(q_new - GOAL)))
            if dg <= ETA and cost[-1] + dg < best and seg_free(q_new, GOAL):
                best = cost[-1] + dg
        if i in record:
            out[i] = best
    return out


def extend(T, q, eta=ETA):
    """One RRT step of tree T = (nodes list, parent list) towards q. Returns 'reached', 'advanced' or 'trapped'."""
    nodes, parent = T
    N = np.array(nodes)
    k = int(np.argmin(np.hypot(*(N - q).T)))
    q_new = steer(nodes[k], q, eta)
    if free(q_new) and seg_free(nodes[k], q_new):
        nodes.append(q_new)
        parent.append(k)
        return "reached" if np.hypot(*(q_new - q)) < 1e-9 else "advanced"
    return "trapped"


def rrt_connect(rng, n_max=5000, log=False):
    """RRT-Connect (Kuffner and LaValle 2000; CMU 16-350 slides 10-12): tree A extends one step towards a random
    sample; if a node was added, tree B CONNECTs to it (repeated steps until it reaches it or is blocked); then the
    trees swap. Returns the two trees (start tree first), the joining node indices and the samples used."""
    Ts = ([START.copy()], [-1])
    Tg = ([GOAL.copy()], [-1])
    A, B = Ts, Tg
    events = []
    for i in range(1, n_max + 1):
        q_rand = np.array([rng.uniform(BOX[0], BOX[1]), rng.uniform(BOX[2], BOX[3])])
        nA = len(A[0])
        s = extend(A, q_rand)
        ev = dict(i=i, q_rand=q_rand, a_is_start=A is Ts, added_a=len(A[0]) - nA, added_b=0, met=False)
        if s != "trapped":
            q_new = A[0][-1]
            nB = len(B[0])
            while True:
                s2 = extend(B, q_new)
                if s2 != "advanced":
                    break
            ev["added_b"] = len(B[0]) - nB
            if s2 == "reached":
                ev["met"] = True
                if log:
                    events.append(ev)
                ka, kb = len(A[0]) - 1, len(B[0]) - 1
                if A is Ts:
                    return dict(Ts=Ts, Tg=Tg, ks=ka, kg=kb, samples=i, events=events)
                return dict(Ts=Ts, Tg=Tg, ks=kb, kg=ka, samples=i, events=events)
        if log:
            events.append(ev)
        A, B = B, A
    return dict(Ts=Ts, Tg=Tg, ks=None, kg=None, samples=n_max, events=events)


def connect_path(res):
    ps = path_from(np.array(res["Ts"][0]), res["Ts"][1], res["ks"])
    pg = path_from(np.array(res["Tg"][0]), res["Tg"][1], res["kg"])
    return np.vstack([ps, pg[::-1][1:]])


def shortest_route(a=START, b=GOAL, margin=0.001, quad=16):
    """Shortest route between a and b in free space: a visibility graph over the corners of the obstacles grown by
    0.25 m (+ a hair), searched with Dijkstra's algorithm."""
    grown = shapely.ops.unary_union([p.buffer(c.R + margin, quad_segs=quad) for p in c.pieces()])
    test = shapely.ops.unary_union([p.buffer(c.R, quad_segs=64) for p in c.pieces()])
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
    dist = [np.inf] * n
    prev = [-1] * n
    dist[0] = 0.0
    pq = [(0.0, 0)]
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
