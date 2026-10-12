"""Replanning, real-time search and bug algorithms of this Note (no output when run on its own).

The room is chapter RO-04's: 0.5 m cells, 76 free, start cell S (4, 2), goal cell G (7, 7) under the door, 8-connected
moves of 0.5 m and 0.707 m that never cut the corner of a blocked cell (searchkit.py). A box of 1.0 m x 0.5 m stands at
x 2.0 to 3.0 m, y 2.0 to 2.5 m, on the robot's route; the map does not show it, and the robot sees it only when it is
within one cell (0.5 m) of a box cell.

- Grid: the room at any cell size (0.5 / k m), with extra blocked cells the robot has seen;
- astar: A* from scratch with the octile heuristic, counting the cells taken off the open list;
- DStarLite: D* Lite (Koenig and Likhachev 2002), backward from G, with a log of every cell it takes off its queue;
- drive: the robot driving to G, replanning with D* Lite when it sees box cells, and counting what A* from scratch
  would have taken off its open list at the same moments;
- lrta, rtaa: real-time search (Korf 1990; Koenig and Likhachev 2006) with the box unknown until seen;
- bug geometry: Bug 1 and Bug 2 (Lumelsky and Stepanov 1987) for the robot's centre around the obstacles grown by its
  0.25 m radius."""
import heapq
import math

import numpy as np
from searchkit import BLOCKED, C, GOAL, START

INF = math.inf
ORDER = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
BOX_M = (2.0, 3.0, 2.0, 2.5)                       # x0, x1, y0, y1 of the box, in m


class Grid:
    """The room at cell side h = 0.5 / k m; `seen` holds the box cells the robot has found."""

    def __init__(self, k=1):
        self.k, self.h = k, C / k
        self.base = np.repeat(np.repeat(~BLOCKED, k, axis=0), k, axis=1)
        self.ny, self.nx = self.base.shape
        self.seen = set()
        self.start = (START[0] * k + k // 2, START[1] * k + k // 2)
        self.goal = (GOAL[0] * k + k // 2, GOAL[1] * k + k // 2)

    def box_cells(self, box=BOX_M):
        x0, x1, y0, y1 = box
        return {(i, j) for j in range(self.ny) for i in range(self.nx) if self.base[j, i]
                and x0 < (i + 0.5) * self.h < x1 and y0 < (j + 0.5) * self.h < y1}

    def free(self, c):
        i, j = c
        return 0 <= i < self.nx and 0 <= j < self.ny and self.base[j, i] and c not in self.seen

    def nbrs(self, c):
        """Every grid neighbour of c with the move's cost: infinite if the move is not allowed."""
        i, j = c
        out = []
        for dx, dy in ORDER:
            n = (i + dx, j + dy)
            if not (0 <= n[0] < self.nx and 0 <= n[1] < self.ny):
                continue
            ok = self.free(c) and self.free(n) and (not (dx and dy) or (self.free((i + dx, j)) and self.free((i, j + dy))))
            out.append((n, (self.h * math.sqrt(2) if dx and dy else self.h) if ok else INF))
        return out

    def octile(self, a, b):
        dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
        return self.h * (math.sqrt(2) * min(dx, dy) + max(dx, dy) - min(dx, dy))

    def sense(self, pos, truth, reach=C):
        """Mark as seen every box cell within `reach` m of the robot's cell (along x and along y); return them."""
        r = int(round(reach / self.h))
        new = [c for c in truth if c not in self.seen and max(abs(c[0] - pos[0]), abs(c[1] - pos[1])) <= r]
        self.seen.update(new)
        return new


def astar(gr, start, goal):
    """A* from scratch, octile heuristic, ties to the smaller h. Returns (closed cells in order, cost, path)."""
    g, par, closed, order, t = {start: 0.0}, {start: None}, set(), [], 0
    heap = [(gr.octile(start, goal), gr.octile(start, goal), 0, start)]
    while heap:
        _, _, _, c = heapq.heappop(heap)
        if c in closed:
            continue
        closed.add(c)
        order.append(c)
        if c == goal:
            break
        for n, s in gr.nbrs(c):
            if s < INF and n not in closed and g[c] + s < g.get(n, INF) - 1e-12:
                g[n], par[n] = g[c] + s, c
                t += 1
                heapq.heappush(heap, (g[n] + gr.octile(n, goal), gr.octile(n, goal), t, n))
    p = [goal]
    while par[p[-1]] is not None:
        p.append(par[p[-1]])
    return order, g[goal], p[::-1]


class DStarLite:
    """D* Lite: g(s) is the cost-to-go a cell holds, rhs(s) its one-step lookahead, min over moves of (move + g(next)).
    A cell is inconsistent when the two differ; inconsistent cells wait in a priority queue ordered by the key
    [min(g, rhs) + h(robot, s) + km, min(g, rhs)]. `log` records every cell taken off the queue: (cell, 'raise' or
    'lower', old g, new g)."""

    def __init__(self, gr, start, goal, g=None):
        self.w, self.s, self.goal, self.km, self.last = gr, start, goal, 0.0, start
        self.g, self.rhs = (dict(g), dict(g)) if g else ({}, {goal: 0.0})
        self.U, self.inU, self.log = [], {}, []
        if not g:
            self._push(goal)

    def G(self, c):
        return self.g.get(c, INF)

    def R(self, c):
        return self.rhs.get(c, INF)

    def key(self, c):
        m = min(self.G(c), self.R(c))
        return (m + self.w.octile(self.s, c) + self.km, m)

    def _push(self, c):
        k = self.key(c)
        self.inU[c] = k
        heapq.heappush(self.U, (k, c))

    def update(self, c):
        if c != self.goal:
            self.rhs[c] = min((s + self.G(n) for n, s in self.w.nbrs(c)), default=INF)
        self.inU.pop(c, None)
        if self.G(c) != self.R(c):
            self._push(c)

    def _top(self):
        while self.U:
            k, c = self.U[0]
            if self.inU.get(c) == k:
                return k, c
            heapq.heappop(self.U)
        return (INF, INF), None

    def compute(self, trace=False):
        """Take cells off the queue until the robot's cell is consistent and no queued key is smaller than its key.
        Returns the number of cells taken off. trace: after each cell, store (g, rhs, queued cells) in self.snaps."""
        n = 0
        self.snaps = [(dict(self.g), dict(self.rhs), set(self.inU))] if trace else []
        while True:
            k, c = self._top()
            if c is None or not (k < self.key(self.s) or self.R(self.s) != self.G(self.s)):
                return n
            heapq.heappop(self.U)
            del self.inU[c]
            if k < self.key(c):
                self._push(c)
                continue
            n += 1
            old = self.G(c)
            if self.G(c) > self.R(c):
                self.g[c] = self.R(c)
                kind = 'lower'
            else:
                self.g[c] = INF
                self.update(c)
                kind = 'raise'
            self.log.append((c, kind, old, self.G(c), k))
            for p, _ in self.w.nbrs(c):
                self.update(p)
            if trace:
                self.snaps.append((dict(self.g), dict(self.rhs), set(self.inU)))

    def moved(self, pos):
        """The robot moved to pos: keys made with the old position stay comparable by adding km (D* Lite)."""
        self.km += self.w.octile(self.last, pos)
        self.last = self.s = pos

    def blocked(self, cells):
        """Cells just found blocked: recheck them and every neighbour, whose moves through them changed."""
        aff = set(cells)
        for c in cells:
            aff.update(n for n, _ in self.w.nbrs(c))
        for c in sorted(aff):
            self.update(c)

    def step(self):
        """The robot's next cell: the neighbour with the smallest move + g, ties to the smaller g, then the smaller
        cell index (the downhill rule of RO-048)."""
        return min(self.w.nbrs(self.s), key=lambda ns: (round(ns[1] + self.G(ns[0]), 9), self.G(ns[0]), ns[0]))[0]


def dijkstra_from_goal(gr):
    """Every free cell's cost-to-go to G on the grid as the robot knows it (the wavefront in metres of RO-048)."""
    d, pq, done = {gr.goal: 0.0}, [(0.0, gr.goal)], set()
    while pq:
        v, c = heapq.heappop(pq)
        if c in done:
            continue
        done.add(c)
        for n, s in gr.nbrs(c):
            if s < INF and v + s < d.get(n, INF) - 1e-12:
                d[n] = v + s
                heapq.heappush(pq, (v + s, n))
    return d


def drive(k=1, from_full=False):
    """The robot drives from S to G at cell side 0.5 / k m. It plans with D* Lite (from scratch, or starting from
    the full cost-to-go map if from_full), senses the box within 0.5 m before every move, and repairs when it sees
    new box cells. At the same moments, A* from scratch is run from the robot's cell for comparison. Returns a dict
    with the route, the first plan's counts and one record per replan."""
    gr = Grid(k)
    truth = gr.box_cells()
    if from_full:
        d = DStarLite(gr, gr.start, gr.goal, g=dijkstra_from_goal(gr))
        first = (0, 0)
    else:
        d = DStarLite(gr, gr.start, gr.goal)
        first = (d.compute(), len(astar(gr, gr.start, gr.goal)[0]))
    pos, route, events = gr.start, [gr.start], []
    while pos != gr.goal:
        new = gr.sense(pos, truth)
        if new:
            d.moved(pos)
            d.log = []
            d.blocked(new)
            n = d.compute()
            a_order, a_cost, a_path = astar(gr, pos, gr.goal)
            events.append(dict(step=len(route) - 1, pos=pos, new=new, dstar=n, dlog=list(d.log), astar=a_order,
                               g=d.G(pos), a_cost=a_cost, a_path=a_path, seen=set(gr.seen)))
        d.s = pos
        pos = d.step()
        route.append(pos)
    return dict(grid=gr, truth=truth, route=route, first=first, events=events,
                length=sum(gr.h * math.dist(a, b) for a, b in zip(route, route[1:])))


def lrta(k=1):
    """LRTA* with a lookahead of one move (Korf 1990, as in CMU 16-350): h starts as the octile distance; at each
    cell the robot senses, sets h(s) to the smallest move + h(next) if that is larger, and moves to that neighbour
    (ties to the smaller h, then the smaller cell index). Returns the route and one record per move."""
    gr = Grid(k)
    truth, h = gr.box_cells(), {}
    H = lambda c: h.get(c, gr.octile(c, gr.goal))
    pos, route, log = gr.start, [gr.start], []
    while pos != gr.goal:
        gr.sense(pos, truth)
        cand = sorted((round(s + H(n), 9), H(n), n) for n, s in gr.nbrs(pos) if s < INF)
        best, _, nxt = cand[0]
        log.append(dict(pos=pos, h_old=H(pos), h_new=max(H(pos), best), cand=cand, nxt=nxt, seen=set(gr.seen)))
        h[pos] = max(H(pos), best)
        pos = nxt
        route.append(pos)
    return route, log


def rtaa(N, k=1):
    """RTAA* (Koenig and Likhachev 2006): from the robot's cell, A* takes at most N cells off its open list; s is the
    best cell left on the open list, with f(s) = g(s) + h(s); every cell u taken off gets h(u) = f(s) - g(u); the
    robot moves along the found path to s, stopping early if it sees a box cell on that path. Returns the route, the
    total cells taken off, and one record per search."""
    gr = Grid(k)
    truth, h = gr.box_cells(), {}
    H = lambda c: h.get(c, gr.octile(c, gr.goal))
    pos, route, log, total = gr.start, [gr.start], [], 0
    while pos != gr.goal:
        gr.sense(pos, truth)
        g, par, closed, t = {pos: 0.0}, {pos: None}, [], 0
        heap = [(H(pos), H(pos), 0, pos)]
        while heap and len(closed) < N:
            f, hh, tt, c = heapq.heappop(heap)
            if c in closed:
                continue
            if c == gr.goal:
                heapq.heappush(heap, (f, hh, tt, c))
                break
            closed.append(c)
            for n, s in gr.nbrs(c):
                if s < INF and n not in closed and g[c] + s < g.get(n, INF) - 1e-12:
                    g[n], par[n] = g[c] + s, c
                    t += 1
                    heapq.heappush(heap, (g[n] + H(n), H(n), t, n))
        while heap[0][3] in closed:
            heapq.heappop(heap)
        f, _, _, best = heap[0]
        total += len(closed)
        upd = {u: (H(u), max(H(u), f - g[u])) for u in closed}
        for u in closed:
            h[u] = max(H(u), f - g[u])
        p = [best]
        while par[p[-1]] is not None:
            p.append(par[p[-1]])
        p = p[::-1]
        log.append(dict(pos=pos, closed=list(closed), best=best, f=f, g=dict(g), upd=upd, path=p))
        for c in p[1:]:
            pos = c
            route.append(pos)
            gr.sense(pos, truth)
            if pos == gr.goal or any(x in gr.seen for x in p):
                break
    return route, total, log


# ---- Bug algorithms: the robot's centre as a point, obstacles grown by the robot's radius (RO-037) -------------
R_ROBOT = 0.25
BUG_START, BUG_GOAL = (2.0, 1.0), (3.6, 4.0)       # the robot's position and the middle of the doorway, in m


def bug_obstacle():
    """The box and the table grown by the robot's radius; the gap between them is narrower than the robot, so the
    two grown shapes join into one obstacle."""
    from roommap import TABLE
    from shapely.geometry import Polygon, box
    from shapely.ops import unary_union
    x0, x1, y0, y1 = BOX_M
    return unary_union([Polygon(TABLE), box(x0, y0, x1, y1)]).buffer(R_ROBOT, quad_segs=32)


def bug_paths(n=4001):
    """Bug 1 and Bug 2 from BUG_START to BUG_GOAL, turning left at the obstacle (it stays on the robot's right).
    Returns a dict with the hit point, the boundary, both routes as point lists and their lengths."""
    from shapely.geometry import LineString, Point
    ob = bug_obstacle()
    ring = ob.exterior
    L = ring.length
    cross = ring.intersection(LineString([BUG_START, BUG_GOAL]))
    pts = sorted(((p.x, p.y) for p in getattr(cross, 'geoms', [cross])), key=lambda p: math.dist(p, BUG_START))
    hit, exitp = pts[0], pts[-1]
    s_hit = ring.project(Point(hit))
    sgn = -1 if ring.is_ccw else 1                   # turning left = clockwise round the obstacle

    def at(s):
        q = ring.interpolate((s_hit + sgn * s) % L)
        return (q.x, q.y)

    ss = np.linspace(0, L, n)
    loop = [at(s) for s in ss]
    dist = [math.dist(p, BUG_GOAL) for p in loop]
    i = int(np.argmin(dist))
    s_close = ss[i]
    back = loop[:i + 1] if s_close <= L - s_close else loop[i:][::-1]
    s_leave = ((ring.project(Point(exitp)) - s_hit) * sgn) % L
    j = int(np.searchsorted(ss, s_leave))
    bug1 = [BUG_START] + loop + back[1:] + [BUG_GOAL]
    bug2 = [BUG_START] + loop[:j] + [exitp, BUG_GOAL]
    to_hit = math.dist(BUG_START, hit)
    return dict(obstacle=ob, perimeter=L, hit=hit, exit=exitp, close=loop[i], close_dist=dist[i], s_close=s_close,
                s_leave=s_leave, bug1=bug1, bug2=bug2, d=math.dist(BUG_START, BUG_GOAL),
                len1=to_hit + L + min(s_close, L - s_close) + dist[i],          # along the boundary, not the chords
                len2=to_hit + s_leave + math.dist(exitp, BUG_GOAL))
