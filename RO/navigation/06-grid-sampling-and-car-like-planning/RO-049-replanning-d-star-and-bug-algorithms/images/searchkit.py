"""The room grid and the searches of chapter RO-04, copied from RO-034 (no output when run on its own).

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
    return sorted({c for *_, c in heap if c not in closed})


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
