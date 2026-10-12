"""The room's search problems for RO-032 and RO-033 (no output when run on its own).

The grid: RO-009's room in 0.5 m cells, 14 x 8 = 112 cells. A cell is blocked when any part of it is covered by the
table, the cabinet or a pole (occupancy share above 0): 36 blocked, 76 free. A cell is named (i, j): column i from
x = 0.5 i to 0.5 i + 0.5 m, row j from y = 0.5 j to 0.5 j + 0.5 m. Start cell (4, 2): x 2.0-2.5, y 1.0-1.5 (the robot
at (2, 1) stands on its lower-left corner); goal cell (7, 7): x 3.5-4.0, y 3.5-4.0, just under the door.
Moves: 4-connected (left, down, up, right; 0.5 m each) or 8-connected (adds diagonals of 0.707 m, which may not cut
the corner of a blocked cell). Neighbours are always tried in the order dx, dy from (-1, -1) to (1, 1).

The waypoint graph: seven points of the same room joined when the straight line between them misses the table and
the cabinet and is at most 2.8 m long, so that the graph is small enough to trace by hand.

Every search records snapshots for the animations; the notebook checks every number the Notes quote."""
import heapq
import math
from collections import deque

import numpy as np
from roommap import CAB, POLE_R, POLES, TABLE
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

C = 0.5
NX, NY = 14, 8
START, GOAL = (4, 2), (7, 7)
_obst = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                    + [Point(p).buffer(POLE_R, quad_segs=256) for p in POLES.values()])
SHARE = np.array([[box(i * C, j * C, (i + 1) * C, (j + 1) * C).intersection(_obst).area / C ** 2
                   for i in range(NX)] for j in range(NY)])
BLOCKED = SHARE > 0                                     # BLOCKED[j, i]
STEPS8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
STEPS4 = [s for s in STEPS8 if 0 in s]                  # left, down, up, right


def centre(c):
    return ((c[0] + 0.5) * C, (c[1] + 0.5) * C)


def free(c):
    i, j = c
    return 0 <= i < NX and 0 <= j < NY and not BLOCKED[j, i]


FREE = [(i, j) for j in range(NY) for i in range(NX) if free((i, j))]


def neighbours(c, steps=STEPS4):
    """Free neighbours of cell c with each move's length; a diagonal may not cut the corner of a blocked cell."""
    i, j = c
    out = []
    for dx, dy in steps:
        n = (i + dx, j + dy)
        if not free(n) or (dx and dy and not (free((i + dx, j)) and free((i, j + dy)))):
            continue
        out.append((n, C * math.hypot(dx, dy)))
    return out


def path_to(parent, goal):
    p, c = [], goal
    while c is not None:
        p.append(c)
        c = parent[c]
    return p[::-1]


def length(p):
    return sum(C * math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(p, p[1:]))


def bfs(steps=STEPS4, start=START, goal=GOAL, nbrs=None):
    """Breadth-first search: the frontier is a queue (first in, first out). A neighbour joins the frontier only if it
    has never been reached (not on the frontier, not visited). The goal test is made when a vertex is taken off.
    Snapshot after every expansion: the vertex taken off, the visited list, the queue (front first), the parents."""
    nbrs = nbrs or (lambda c: neighbours(c, steps))
    parent, queue, visited, snaps = {start: None}, deque([start]), [], []
    while queue:
        cur = queue.popleft()
        visited.append(cur)
        if cur != goal:
            for n, _ in nbrs(cur):
                if n not in parent:
                    parent[n] = cur
                    queue.append(n)
        snaps.append(dict(cur=cur, visited=list(visited), frontier=list(queue), parent=dict(parent)))
        if cur == goal:
            break
    return dict(path=path_to(parent, goal) if goal in visited else None, visited=visited, snaps=snaps, parent=parent)


def dfs(steps=STEPS4, start=START, goal=GOAL):
    """Depth-first search: the frontier is a stack (last in, first out); the first neighbour in the order is pushed
    last, so it is tried first. Same rule as bfs for which neighbours join. Snapshot after every expansion; the stack
    is listed top first; dead = this expansion added nothing (a dead end: the search backs up)."""
    parent, stack, visited, snaps = {start: None}, [start], [], []
    while stack:
        cur = stack.pop()
        visited.append(cur)
        kids = []
        if cur != goal:
            kids = [n for n, _ in neighbours(cur, steps) if n not in parent]
            for n in reversed(kids):
                parent[n] = cur
                stack.append(n)
        snaps.append(dict(cur=cur, visited=list(visited), frontier=stack[::-1], parent=dict(parent),
                          dead=not kids and cur != goal))
        if cur == goal:
            break
    return dict(path=path_to(parent, goal) if goal in visited else None, visited=visited, snaps=snaps)


def dfs_battery(charge, full_state, start=START, goal=GOAL):
    """Depth-first search when each 0.5 m move uses one unit of charge and the robot starts with `charge` units.
    full_state False: the search state is the cell alone, so a cell reached once is never tried again.
    full_state True: the search state is (cell, charge left), so the same cell with more charge is a new state.
    Snapshot after every expansion: (cell, charge left) taken off, the visited states."""
    key = (lambda c, b: (c, b)) if full_state else (lambda c, b: c)
    parent, stack, visited, snaps = {key(start, charge): None}, [(start, charge)], [], []
    found = None
    while stack:
        cur, b = stack.pop()
        visited.append((cur, b))
        kids = []
        if cur == goal:
            found = (cur, b)
        elif b > 0:
            kids = [(n, b - 1) for n, _ in neighbours(cur) if key(n, b - 1) not in parent]
            for n, nb in reversed(kids):
                parent[key(n, nb)] = (cur, b)
                stack.append((n, nb))
        snaps.append(dict(cur=(cur, b), visited=list(visited), stack=[s for s in stack[::-1]]))
        if found:
            break
    path = None
    if found:
        path, s = [], found
        while s is not None:
            path.append(s[0])
            s = parent[key(*s)]
        path = path[::-1]
    return dict(path=path, visited=visited, snaps=snaps, found=found)


def tree_paths(nbrs, start, goal, depth):
    """Every path from start that never visits a vertex twice, level by level up to `depth` moves; a path that has
    reached the goal is not extended. Returns a list of paths (each a list of vertices), in level order."""
    level, out = [[start]], [[start]]
    for _ in range(depth):
        nxt = [p + [n] for p in level if p[-1] != goal for n, _ in nbrs(p[-1]) if n not in p]
        out += nxt
        level = nxt
    return out


def dijkstra(nbrs, start, goal, stop_at_goal=True):
    """Dijkstra's algorithm with a binary heap (Python's heapq). Each entry is (tentative cost, insertion number,
    vertex): equal costs come out in the order they went in. A vertex whose cost drops is pushed again; its old
    entry stays in the heap and is skipped when it comes out (lazy deletion). The goal test is made when a vertex is
    settled (taken off). Snapshot after every settled vertex: the vertex, its cost, the settled list, the costs and
    parents so far, the live heap entries (cost, vertex) in order, the raw heap array, and the improvements made."""
    g, parent, settled, snaps, tick = {start: 0.0}, {start: None}, [], [], 0
    heap, pops = [(0.0, 0, start)], 0
    while heap:
        cost, _, cur = heapq.heappop(heap)
        pops += 1
        if cur in settled:
            continue
        settled.append(cur)
        improved, added = [], []
        if not (stop_at_goal and cur == goal):
            for n, w in nbrs(cur):
                if n in settled:
                    continue
                new = cost + w
                if new < g.get(n, math.inf) - 1e-12:
                    if n in g:
                        improved.append((n, g[n], new))
                    else:
                        added.append((n, new))
                    g[n], parent[n] = new, cur
                    tick += 1
                    heapq.heappush(heap, (new, tick, n))
        live = sorted((c, t, v) for c, t, v in heap if v not in settled and abs(g[v] - c) < 1e-12)
        snaps.append(dict(cur=cur, cost=cost, settled=list(settled), g=dict(g), parent=dict(parent),
                          queue=[(c, v) for c, _, v in live], heap=[(c, v) for c, _, v in heap],
                          improved=improved, added=added, pops=pops))
        if stop_at_goal and cur == goal:
            break
    return dict(path=path_to(parent, goal) if goal in settled else None, cost=g.get(goal), settled=settled,
                snaps=snaps, g=g, parent=parent)


# ---- the waypoint graph -------------------------------------------------------------------------------------------
WP = {"S": (2.0, 1.0), "A": (3.0, 1.0), "B": (5.0, 1.0), "C": (5.5, 2.5), "D": (3.5, 3.0), "P": (1.0, 3.0),
      "G": (3.6, 4.0)}
WP_NAME = {"S": "start", "A": "table corner", "B": "table corner", "C": "table corner", "D": "table corner",
           "P": "pink pole", "G": "door"}
WP_MAX = 2.8
_table, _cab = Polygon(TABLE), unary_union([box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB])


def _clear(a, b):
    """True when the segment a-b runs only through free space or along an obstacle's edge, and passes no pole other
    than one it ends at."""
    seg = LineString([WP[a], WP[b]])
    for ob in (_table, _cab):
        inside = seg.intersection(ob)
        if inside.length > 1e-9 and inside.difference(ob.boundary.buffer(1e-9)).length > 1e-9:
            return False
    for px, py in POLES.values():
        if (px, py) not in (WP[a], WP[b]) and seg.distance(Point(px, py)) < POLE_R:
            return False
    return True


def wp_dist(a, b):
    return math.dist(WP[a], WP[b])


WP_EDGES = sorted((a, b) for a in WP for b in WP if a < b and wp_dist(a, b) <= WP_MAX and _clear(a, b))


def wp_nbrs(v):
    """Neighbours of waypoint v in alphabetical order, with the edge's length in m."""
    out = [(b if a == v else a) for a, b in WP_EDGES if v in (a, b)]
    return [(n, wp_dist(v, n)) for n in sorted(out)]


# ---- a binary min-heap that records its own steps -----------------------------------------------------------------
class MinHeap:
    """A binary min-heap stored in a list: the children of entry i sit at 2i + 1 and 2i + 2, its parent at
    (i - 1) // 2. Every swap is recorded in self.steps as (what, list after the swap, the two indexes swapped)."""

    def __init__(self, items=()):
        self.a, self.steps = list(items), []

    def push(self, item):
        self.a.append(item)
        i = len(self.a) - 1
        self.steps.append(("place", list(self.a), (i, i)))
        while i > 0 and self.a[(i - 1) // 2][0] > self.a[i][0]:
            p = (i - 1) // 2
            self.a[p], self.a[i] = self.a[i], self.a[p]
            self.steps.append(("sift up", list(self.a), (p, i)))
            i = p

    def pop(self):
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self.steps.append(("last to root", list(self.a), (0, 0)))
            i = 0
            while True:
                kids = [k for k in (2 * i + 1, 2 * i + 2) if k < len(self.a)]
                if not kids:
                    break
                k = min(kids, key=lambda k: self.a[k][0])
                if self.a[k][0] >= self.a[i][0]:
                    break
                self.a[i], self.a[k] = self.a[k], self.a[i]
                self.steps.append(("sift down", list(self.a), (i, k)))
                i = k
        return top
