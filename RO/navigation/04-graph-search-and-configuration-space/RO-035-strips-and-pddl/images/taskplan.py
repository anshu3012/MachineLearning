"""The task of this Note (no output when run on its own): carry the cup from the table to the door. Facts, the 12
STRIPS actions (precondition, add list, delete list), applying an action, forward search (breadth-first and A*),
and the routes on the room's 0.5 m grid that carry out each move action."""
import math
from collections import deque
from heapq import heappop, heappush
from itertools import permutations

import numpy as np
from roommap import CAB, H, POLE_R, POLES, TABLE, W
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

PLACES = ["start", "table", "door"]
FACTS = [f"robot-at {p}" for p in PLACES] + [f"cup-at {p}" for p in PLACES] + ["holding-cup", "hand-empty"]
INIT = frozenset({"robot-at start", "cup-at table", "hand-empty"})
GOAL = frozenset({"cup-at door"})


def actions():
    """The 12 ground actions as (name, precondition, add list, delete list), in the order the search tries them."""
    out = []
    for a, b in permutations(PLACES, 2):
        out.append((f"move {a} {b}", {f"robot-at {a}"}, {f"robot-at {b}"}, {f"robot-at {a}"}))
    for p in PLACES:
        out.append((f"pick-up {p}", {f"robot-at {p}", f"cup-at {p}", "hand-empty"}, {"holding-cup"},
                    {f"cup-at {p}", "hand-empty"}))
    for p in PLACES:
        out.append((f"put-down {p}", {f"robot-at {p}", "holding-cup"}, {f"cup-at {p}", "hand-empty"},
                    {"holding-cup"}))
    return [(n, frozenset(pre), frozenset(add), frozenset(de)) for n, pre, add, de in out]


ACTIONS = actions()


def applicable(s, act):
    """An action applies when the state holds every fact of its precondition."""
    return act[1] <= s


def apply(s, act):
    """The next state: remove the delete list, then add the add list."""
    return (s - act[3]) | act[2]


def successors(s):
    return [(a[0], apply(s, a)) for a in ACTIONS if applicable(s, a)]


def reachable():
    """Every state reachable from INIT (breadth-first, no goal test)."""
    seen, q = {INIT}, deque([INIT])
    while q:
        s = q.popleft()
        for _, t in successors(s):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def bfs():
    """Breadth-first forward search; the goal test is made when a state is taken from the frontier.
    Returns the plan and a log of steps: (state taken, its new children with the actions, frontier after)."""
    parent = {INIT: None}
    q = deque([INIT])
    log = []
    while q:
        s = q.popleft()
        if GOAL <= s:
            log.append((s, [], list(q)))
            break
        kids = []
        for name, t in successors(s):
            if t not in parent:
                parent[t] = (s, name)
                q.append(t)
                kids.append((name, t))
        log.append((s, kids, list(q)))
    plan, t = [], s
    while parent[t]:
        t, name = parent[t]
        plan.append(name)
    return plan[::-1], log, parent


def h_actions_left(s):
    """Fewest actions still needed (each named action must happen at least once), so it never overestimates."""
    if "cup-at door" in s:
        return 0
    if "holding-cup" in s:
        return 1 + ("robot-at door" not in s)                      # (move to the door) + put down
    cup = next(f.split()[1] for f in s if f.startswith("cup-at"))
    return 3 + (f"robot-at {cup}" not in s)                         # (move to the cup) + pick up + move + put down


def astar(h=h_actions_left):
    """A* forward search with every action costing 1. Returns the plan and the order states were expanded."""
    g = {INIT: 0}
    parent = {INIT: None}
    heap, n = [(h(INIT), 0, 0, INIT)], 1
    closed = []
    while heap:
        f, gs, _, s = heappop(heap)
        if s in closed:
            continue
        closed.append(s)
        if GOAL <= s:
            break
        for name, t in successors(s):
            if t not in g or gs + 1 < g[t]:
                g[t] = gs + 1
                parent[t] = (s, name)
                heappush(heap, (gs + 1 + h(t), gs + 1, n, t))
                n += 1
    plan, t = [], s
    while parent[t]:
        t, name = parent[t]
        plan.append(name)
    return plan[::-1], closed


def short(s):
    """A state written in a few letters: robot place / cup place (or 'held')."""
    r = next(f.split()[1] for f in s if f.startswith("robot-at"))
    c = "held" if "holding-cup" in s else next(f.split()[1] for f in s if f.startswith("cup-at"))
    return r, c


# ---------------------------------------------------------------- the room's grid, for the routes of the move actions
C = 0.5
NX, NY = int(round(W / C)), int(round(H / C))
CELL = {"start": (4, 2), "table": (5, 3), "door": (7, 7)}           # (column, row): x 2.0-2.5 y 1.0-1.5 and so on
SPOT = {"start": (2.0, 1.0), "table": (2.75, 1.75), "door": (3.75, 3.75)}   # where the robot stands at each place
CUP = (3.45, 1.85)                                                  # the cup on the table


def shares():
    obst = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                       + [Point(p).buffer(POLE_R, quad_segs=256) for p in POLES.values()])
    return np.array([[box(i * C, j * C, (i + 1) * C, (j + 1) * C).intersection(obst).area / C ** 2
                      for i in range(NX)] for j in range(NY)])


BLOCKED = shares() > 1e-12


def bfs_route4(a, b):
    """A shortest route of free cells from cell a to cell b with 4-connected moves (breadth-first search)."""
    prev = {a: None}
    q = deque([a])
    while q:
        c = q.popleft()
        if c == b:
            break
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < NX and 0 <= n[1] < NY and not BLOCKED[n[1], n[0]] and n not in prev:
                prev[n] = c
                q.append(n)
    path, c = [], b
    while c is not None:
        path.append(c)
        c = prev[c]
    return path[::-1]


def grid_route(a, b):
    """A shortest route from cell a to cell b with 8-connected moves (0.5 m straight, 0.707 m diagonal) that may
    not cut the corner of a blocked cell (Dijkstra's algorithm; A* returns the same length). Returns (length, cells)."""
    dist, prev, heap = {a: 0.0}, {a: None}, [(0.0, a)]
    while heap:
        d, u = heappop(heap)
        if u == b:
            break
        if d > dist[u]:
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                v = (u[0] + dx, u[1] + dy)
                if (dx, dy) == (0, 0) or not (0 <= v[0] < NX and 0 <= v[1] < NY) or BLOCKED[v[1], v[0]]:
                    continue
                if dx and dy and (BLOCKED[u[1], u[0] + dx] or BLOCKED[u[1] + dy, u[0]]):
                    continue
                w = C * math.hypot(dx, dy)
                if d + w < dist.get(v, math.inf):
                    dist[v], prev[v] = d + w, u
                    heappush(heap, (d + w, v))
    path, c = [], b
    while c is not None:
        path.append(c)
        c = prev[c]
    return dist[b], path[::-1]


if __name__ == "__main__":
    assert len(FACTS) == 8 and 2 ** len(FACTS) == 256 and len(ACTIONS) == 12
    print(len(reachable()), "reachable states")
    plan, log, parent = bfs()
    print("BFS plan", plan, "expanded", len(log), "generated", len(parent))
    for s, kids, q in log:
        print(short(s), [(n, short(t)) for n, t in kids], [short(t) for t in q])
    p2, closed = astar()
    print("A* plan", p2, "expanded", len(closed), [short(s) for s in closed])
    print("blocked", BLOCKED.sum(), "free", (~BLOCKED).sum())
    assert BLOCKED.sum() == 36 and len(bfs_route4(CELL["start"], CELL["door"])) - 1 == 8
    for a, b in (("start", "door"), ("start", "table"), ("table", "door")):
        d, r = grid_route(CELL[a], CELL[b])
        print(a, b, round(d, 3), "m", r)
