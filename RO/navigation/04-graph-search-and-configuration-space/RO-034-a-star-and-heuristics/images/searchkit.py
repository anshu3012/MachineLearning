"""The search algorithms of this Note on the room grid (no output when run on its own).

The grid: RO-009's room in 0.5 m cells, 14 x 8 = 112 cells; a cell is blocked when any part of it is covered by the
table, the cabinet or a pole (occupancy share above 0): 36 blocked, 76 free. A cell is named (i, j): column i from
x = 0.5 i to 0.5 i + 0.5 m, row j from y = 0.5 j to 0.5 j + 0.5 m. Start cell (4, 2): x 2.0-2.5, y 1.0-1.5; goal cell
(7, 7): x 3.5-4.0, y 3.5-4.0, just under the door. 8-connected moves, 0.5 m straight and 0.707 m diagonal; a diagonal
move may not cut the corner of a blocked cell (both side cells must be free).

Every search here is written the same way, with an open list (a heap ordered by a key) and a closed list, and returns
a dict with the path, its cost and the order in which cells were expanded (taken off the open list)."""
import heapq
import math

import numpy as np
from roommap import CAB, H, POLE_R, POLES, TABLE, W
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

C = 0.5
NX, NY = int(round(W / C)), int(round(H / C))
START, GOAL = (4, 2), (7, 7)
S2 = math.sqrt(2) * C                       # one diagonal move, 0.7071 m

_obst = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                    + [Point(p).buffer(POLE_R, quad_segs=256) for p in POLES.values()])
SHARE = np.array([[box(i * C, j * C, (i + 1) * C, (j + 1) * C).intersection(_obst).area / C ** 2
                   for i in range(NX)] for j in range(NY)])
BLOCKED = SHARE > 0                         # BLOCKED[j, i]


def free(c):
    i, j = c
    return 0 <= i < NX and 0 <= j < NY and not BLOCKED[j, i]


ORDER = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


def neighbours(c):
    """Free 8-connected neighbours of cell c with the move's length; no cutting the corner of a blocked cell."""
    i, j = c
    out = []
    for dx, dy in ORDER:
        n = (i + dx, j + dy)
        if not free(n):
            continue
        if dx and dy and not (free((i + dx, j)) and free((i, j + dy))):
            continue
        out.append((n, S2 if dx and dy else C))
    return out


def octile(a, b=GOAL):
    """Length of the shortest 8-connected route from a to b on an empty grid: diagonals first, then straight."""
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return S2 * min(dx, dy) + C * (max(dx, dy) - min(dx, dy))


def straight(a, b=GOAL):
    """Straight-line distance between the two cell centres, in m."""
    return C * math.hypot(a[0] - b[0], a[1] - b[1])


def zero(a, b=GOAL):
    return 0.0


def path_cost(p):
    return sum(C * math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(p, p[1:]))


def best_first(start=START, goal=GOAL, h=octile, wg=1.0, wh=1.0, trace=False, nbrs=neighbours):
    """One loop for Dijkstra (wg 1, wh 0), greedy best-first (wg 0, wh 1), A* (1, 1) and weighted A* (1, eps).
    key = wg g + wh h. Ties are broken by the smaller h, then by the earlier insertion (Lague's tie rule).
    trace: also record a snapshot (open, closed, g, parent, current) after every expansion."""
    g, parent, closed, order, snaps = {start: 0.0}, {start: None}, set(), [], []
    tick = 0
    heap = [(wg * 0 + wh * h(start, goal), h(start, goal), tick, start)]
    while heap:
        f, hh, _, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        order.append(cur)
        if cur == goal:
            if trace:
                snaps.append(dict(cur=cur, closed=list(order), open=_open(heap, closed), g=dict(g), parent=dict(parent)))
            break
        for n, step in nbrs(cur):
            if n in closed:
                continue
            ng = g[cur] + step
            if n not in g or ng < g[n] - 1e-12:
                g[n], parent[n] = ng, cur
                tick += 1
                heapq.heappush(heap, (wg * ng + wh * h(n, goal), h(n, goal), tick, n))
        if trace:
            snaps.append(dict(cur=cur, closed=list(order), open=_open(heap, closed), g=dict(g), parent=dict(parent)))
    path = _path(parent, goal) if goal in closed else None
    return dict(path=path, cost=g.get(goal) if path else None, order=order, g=g, parent=parent, snaps=snaps)


def _open(heap, closed):
    cells = {c for *_, c in heap if c not in closed}
    return sorted(c for c in cells if c != "V") + (["V"] if "V" in cells else [])    # "V": the virtual goal


def _path(parent, goal):
    p, c = [], goal
    while c is not None:
        p.append(c)
        c = parent[c]
    return p[::-1]


def dijkstra(**kw):
    return best_first(h=zero, wg=1.0, wh=0.0, **kw)


def greedy(**kw):
    return best_first(wg=0.0, wh=1.0, **kw)


def astar(h=octile, eps=1.0, **kw):
    return best_first(h=h, wg=1.0, wh=eps, **kw)


def free_cells():
    return [(i, j) for j in range(NY) for i in range(NX) if free((i, j))]


def dist_from(src):
    """Exact shortest distance from src to every free cell (a full Dijkstra run, no goal)."""
    d = {src: 0.0}
    heap = [(0.0, src)]
    done = set()
    while heap:
        dd, c = heapq.heappop(heap)
        if c in done:
            continue
        done.add(c)
        for n, s in neighbours(c):
            if dd + s < d.get(n, math.inf) - 1e-12:
                d[n] = dd + s
                heapq.heappush(heap, (d[n], n))
    return d


def bidirectional(start=START, goal=GOAL):
    """Bidirectional Dijkstra as in Devadas (MIT 6.006 lecture 18). The grid's moves cost the same both ways, so the
    backward search from the goal uses the same moves. Alternate one expansion forward, one backward; stop when some
    cell w has been taken off both open lists. w need not lie on a shortest route: the answer is the smallest
    gf(x) + gb(x) over every cell x that both searches have reached."""
    side = [dict(g={start: 0.0}, par={start: None}, heap=[(0.0, 0, start)], closed=[]),
            dict(g={goal: 0.0}, par={goal: None}, heap=[(0.0, 0, goal)], closed=[])]
    tick, frames, turn, w = 0, [], 0, None
    while w is None:
        s, o = side[turn], side[1 - turn]
        while s["heap"][0][2] in s["closed"]:
            heapq.heappop(s["heap"])
        dd, _, cur = heapq.heappop(s["heap"])
        s["closed"].append(cur)
        if cur in o["closed"]:
            w = cur
        else:
            for n, st in neighbours(cur):
                if dd + st < s["g"].get(n, math.inf) - 1e-12:
                    s["g"][n], s["par"][n] = dd + st, cur
                    tick += 1
                    heapq.heappush(s["heap"], (dd + st, tick, n))
        frames.append(dict(turn=turn, cur=cur, closed=[list(side[0]["closed"]), list(side[1]["closed"])],
                           open=[sorted(set(side[k]["g"]) - set(side[k]["closed"])) for k in (0, 1)]))
        turn = 1 - turn
    both = set(side[0]["g"]) & set(side[1]["g"])
    x = min(both, key=lambda c: (side[0]["g"][c] + side[1]["g"][c], c))
    cost = side[0]["g"][x] + side[1]["g"][x]
    path = _path(side[0]["par"], x) + _path(side[1]["par"], x)[::-1][1:]
    return dict(path=path, cost=cost, frames=frames, w=w, w_cost=side[0]["g"][w] + side[1]["g"][w], x=x,
                gf=side[0]["g"], gb=side[1]["g"], expanded=len(side[0]["closed"]) + len(side[1]["closed"]))


def line_of_sight(a, b, sub=200):
    """True when the straight segment between the centres of cells a and b crosses no blocked cell (checked on sub
    points per 0.5 m of segment, plus the exact corner test: a segment through a cell corner may not squeeze between
    two blocked cells)."""
    (x0, y0), (x1, y1) = [((c[0] + 0.5) * C, (c[1] + 0.5) * C) for c in (a, b)]
    L = math.hypot(x1 - x0, y1 - y0)
    n = max(2, int(L / C * sub))
    for t in np.linspace(0, 1, n + 1):
        x, y = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
        fx, fy = x / C, y / C
        i, j = int(math.floor(fx)), int(math.floor(fy))
        cells = {(i, j)}
        if abs(fx - round(fx)) < 1e-9:
            cells.add((int(round(fx)) - 1, j))
        if abs(fy - round(fy)) < 1e-9:
            cells.add((i, int(round(fy)) - 1))
        if any(not free(c) for c in cells if 0 <= c[0] < NX and 0 <= c[1] < NY):
            return False
    return True


def theta_star(start=START, goal=GOAL, h=straight, trace=False):
    """Theta* (Nash et al.): A* whose expanded cell may hand its own parent to a neighbour when the parent can see the
    neighbour, so a path is a chain of straight segments between cell centres at any angle."""
    g, parent, closed, order, snaps, tick = {start: 0.0}, {start: start}, set(), [], [], 0
    heap = [(h(start, goal), 0, start)]
    shortcuts = []
    while heap:
        f, _, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        order.append(cur)
        if cur == goal:
            break
        for n, step in neighbours(cur):
            if n in closed:
                continue
            p = parent[cur]
            if p != cur and line_of_sight(p, n):
                cand, par = g[p] + straight(p, n), p
            else:
                cand, par = g[cur] + step, cur
            if cand < g.get(n, math.inf) - 1e-12:
                g[n], parent[n] = cand, par
                if par != cur:
                    shortcuts.append((cur, n, par))
                tick += 1
                heapq.heappush(heap, (cand + h(n, goal), tick, n))
        if trace:
            snaps.append(dict(cur=cur, closed=list(order), g=dict(g), parent=dict(parent)))
    p, c = [goal], goal
    while c != start:
        c = parent[c]
        p.append(c)
    return dict(path=p[::-1], cost=g[goal], order=order, snaps=snaps, shortcuts=shortcuts)


def ida_star(start=START, goal=GOAL, h=octile):
    """IDA* (Korf 1985): depth-first search that stops a branch once g + h passes a limit; each round raises the limit
    to the smallest g + h that passed it. The only memory is the current path (cycles on it are skipped)."""
    limit, rounds = h(start, goal), []
    while True:
        visits, nxt, found, paths, cuts = [], [math.inf], [None], [], []

        def dfs(path, gg):
            c = path[-1]
            f = gg + h(c, goal)
            if f > limit + 1e-9:
                nxt[0] = min(nxt[0], f)
                cuts.append((len(visits), c, f))
                return False
            visits.append(c)
            paths.append(list(path))
            if c == goal:
                found[0] = (list(path), gg)
                return True
            for n, s in neighbours(c):
                if n in path:
                    continue
                path.append(n)
                if dfs(path, gg + s):
                    return True
                path.pop()
            return False

        dfs([start], 0.0)
        rounds.append(dict(limit=limit, visits=visits, found=found[0], next=nxt[0], paths=paths, cuts=cuts))
        if found[0]:
            return rounds
        limit = nxt[0]


def jps(start=START, goal=GOAL, h=octile, trace=False):
    """Jump point search (Harabor and Grimm 2011) on the same 8-connected grid with no corner cutting: from each
    expanded cell, jump straight or diagonally and stop only at the goal or at a cell with a forced neighbour; only
    those jump points enter the open list. Variant for grids that forbid corner cutting: a diagonal jump also scans
    both straight directions at every step, and a straight jump stops where a side cell opens up behind an obstacle."""
    def jump(c, d):
        dx, dy = d
        steps = []
        while True:
            n = (c[0] + dx, c[1] + dy)
            if not free(n) or (dx and dy and not (free((c[0] + dx, c[1])) and free((c[0], c[1] + dy)))):
                return None, steps
            steps.append(n)
            if n == goal:
                return n, steps
            x, y = n
            if dx and dy:
                for d2 in ((dx, 0), (0, dy)):
                    j, _ = jump(n, d2)
                    if j is not None:
                        return n, steps
            elif dx:
                if (free((x, y + 1)) and not free((x - dx, y + 1))) or (free((x, y - 1)) and not free((x - dx, y - 1))):
                    return n, steps
            else:
                if (free((x + 1, y)) and not free((x + 1, y - dy))) or (free((x - 1, y)) and not free((x - 1, y - dy))):
                    return n, steps
            c = n

    def dirs(c, p):
        if p is None:
            return ORDER
        dx = (c[0] > p[0]) - (c[0] < p[0])
        dy = (c[1] > p[1]) - (c[1] < p[1])
        x, y = c
        out = []
        if dx and dy:
            out = [(dx, 0), (0, dy), (dx, dy)]
        elif dx:
            out = [(dx, 0)]
            for s in (1, -1):
                if free((x, y + s)) and not free((x - dx, y + s)):
                    out += [(0, s), (dx, s)]
        else:
            out = [(0, dy)]
            for s in (1, -1):
                if free((x + s, y)) and not free((x + s, y - dy)):
                    out += [(s, 0), (s, dy)]
        return out

    g, parent, closed, order, jumps, tick = {start: 0.0}, {start: None}, set(), [], [], 0
    heap = [(h(start, goal), h(start, goal), 0, start)]
    while heap:
        f, _, _, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        order.append(cur)
        if cur == goal:
            break
        for d in dirs(cur, parent[cur]):
            jp, steps = jump(cur, d)
            jumps.append(dict(frm=cur, d=d, steps=steps, jp=jp))
            if jp is None or jp in closed:
                continue
            ng = g[cur] + path_cost([cur, jp])
            if ng < g.get(jp, math.inf) - 1e-12:
                g[jp], parent[jp] = ng, cur
                tick += 1
                heapq.heappush(heap, (ng + h(jp, goal), h(jp, goal), tick, jp))
    return dict(path=_path(parent, goal), cost=g[goal], order=order, jumps=jumps)


def ara_star(eps_list=(2.5, 1.2, 1.0), start=START, goal=GOAL, h=octile):
    """ARA* (Likhachev, Gordon and Thrun 2003): weighted A* runs with eps falling; each run keeps the g values of the
    last run and re-expands only cells whose g has dropped since they were expanded (the INCONS list). A run stops,
    like weighted A*, when the goal comes off the open list, or when no open cell's key is below the goal's g (then
    no open cell can improve the route under this eps). Returns one record per eps."""
    g, parent = {start: 0.0}, {start: None}
    key = lambda c, e: g[c] + e * h(c, goal)
    open_, incons, out = {start}, set(), []
    for e in eps_list:
        open_ |= incons
        incons, closed, order = set(), set(), []
        heap = [(key(c, e), h(c, goal), i, c) for i, c in enumerate(sorted(open_))]
        heapq.heapify(heap)
        tick = len(heap)
        while heap:
            k, _, _, cur = heap[0]
            if cur not in open_ or abs(k - key(cur, e)) > 1e-9:
                heapq.heappop(heap)
                continue
            if goal in g and cur != goal and k >= g[goal] - 1e-12:
                break
            heapq.heappop(heap)
            open_.discard(cur)
            closed.add(cur)
            order.append(cur)
            if cur == goal:
                break
            for n, s in neighbours(cur):
                if g[cur] + s < g.get(n, math.inf) - 1e-12:
                    g[n], parent[n] = g[cur] + s, cur
                    if n in closed:
                        incons.add(n)
                    else:
                        open_.add(n)
                        tick += 1
                        heapq.heappush(heap, (key(n, e), h(n, goal), tick, n))
        out.append(dict(eps=e, order=order, path=_path(parent, goal), cost=g[goal], open=sorted(open_ | incons)))
    return out


def multi_goal(goals, start=START, extra=None, trace=False):
    """A* to whichever of several goal cells is cheapest: every goal cell gets an edge to one extra vertex, the
    virtual goal V, of 0 m or of extra[goal] m for a worse goal; h(n) = the smallest of octile(n, goal) + that
    goal's edge, which never overestimates the cost to V (CMU 16-350; Patel, Heuristics)."""
    V, extra = "V", extra or {}
    def nb(c):
        out = neighbours(c)
        return out + [(V, extra.get(c, 0.0))] if c in goals else out
    def h(c, _):
        return 0.0 if c == V else min(octile(c, q) + extra.get(q, 0.0) for q in goals)
    return best_first(start=start, goal=V, h=h, nbrs=nb, trace=trace)


def moving_goal(walk, speed=0.5, start=START):
    """A* over states (cell, time) to meet a person whose walk is known: walk[k] is the person's cell from second k
    to second k + 1 (LaValle 7.1.1: a state holds the place and the time; time only moves forward). Moves: straight
    (0.5 m) or diagonal (0.707 m) at `speed` m/s, or wait one second; the cost is time. A state (cell, t) with the
    person in that cell at t gets a 0 s edge to the virtual goal V. h = octile distance to the nearest cell of the
    walk / speed, which never overestimates the time to any meeting. Times are rounded to 1e-9 s so that equal times
    give one state."""
    V = "V"
    def nb(s):
        c, t = s
        out = []
        for n, step in neighbours(c) + [(c, speed * 1.0)]:          # the last one: wait one second
            tt = round(t + step / speed, 9)
            if tt < len(walk):                                      # the walk ends: no meeting after it
                out.append(((n, tt), step / speed))
        if walk[math.floor(t + 1e-9)] == c:
            out.append((V, 0.0))
        return out
    def h(s, _):
        return 0.0 if s == V else min(octile(s[0], q) for q in walk) / speed
    return best_first(start=(start, 0.0), goal=V, h=h, nbrs=nb)


# The five-waypoint roadmap of Section 6: the robot S, waypoints A, B, C in free floor, the doorway centre G, in m.
RM = dict(S=(2.0, 1.0), A=(2.5, 2.5), B=(1.3, 2.35), C=(2.6, 3.4), G=(3.6, 4.0))
RM_EDGES = [("S", "A"), ("S", "B"), ("A", "C"), ("B", "C"), ("C", "G")]


def rm_len(a, b):
    return math.dist(RM[a], RM[b])


def rm_astar(h):
    """A* with a closed list on the roadmap (edges both ways). h: dict of guesses. Returns the steps for the
    animation: what comes off the open list, the open list after it, and whether a better route was skipped."""
    nb = {v: [] for v in RM}
    for a, b in RM_EDGES:
        nb[a].append(b)
        nb[b].append(a)
    g, parent, closed, steps = {"S": 0.0}, {"S": None}, set(), []
    heap, tick = [(h["S"], 0, "S")], 0
    while heap:
        f, _, cur = heapq.heappop(heap)
        if cur in closed or f > g[cur] + h[cur] + 1e-12:
            continue
        closed.add(cur)
        skipped = []
        if cur != "G":
            for n in sorted(nb[cur]):
                ng = g[cur] + rm_len(cur, n)
                if n in closed:
                    if ng < g[n] - 1e-12:
                        skipped.append((n, ng))
                    continue
                if n not in g or ng < g[n] - 1e-12:
                    g[n], parent[n] = ng, cur
                    tick += 1
                    heapq.heappush(heap, (ng + h[n], tick, n))
        steps.append(dict(cur=cur, g=dict(g), closed=sorted(closed), skipped=skipped,
                          open={v: (g[v], h[v], g[v] + h[v]) for v in g if v not in closed}))
        if cur == "G":
            break
    p, c = [], "G"
    while c is not None:
        p.append(c)
        c = parent[c]
    return dict(steps=steps, cost=g["G"], path=p[::-1])
