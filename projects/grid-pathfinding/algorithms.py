"""Path-finding algorithms, one function each, written against the map interface in map_interface.py.

Every function takes a map m and only asks it four things: m.neighbours(node), m.cost(a, b), m.heuristic(a, b) and,
for jump point search and Theta*, which need a grid, m.passable(col, row) and m.line_of_sight(a, b). So the same
functions run on the warehouse grid, a maze, or the streets of Chicago.

Every function returns a Result: the route (a list of nodes from start to goal), its cost (metres, or seconds on a
travel-time map), and a log of what the search did, step by step, which the drawing code replays. The log holds tuples:
    ("visit", node, side)          node is taken off the frontier and its moves are looked at
    ("look", a, b, added, side)    the move a -> b is looked at; added is True if b went onto the frontier
                                   (or got a shorter cost there)
    ("scan", cell)                 jump point search stepped over this cell while looking for a jump point
    ("round", text)                a new round starts (iterative deepening, anytime A*): the drawing starts afresh
    ("route", nodes, length)       a round found this route
side is 0, except in bidirectional search, where the search from the goal uses side 1.

A new search is a new function that fills a Log and returns a Result; the drawing code needs nothing new. The
heuristics (guesses of the cost still to go) are near the end: zero, manhattan, straight_line, octile, landmarks
and exact; a_star(m, start, goal, heuristic) takes any of them."""
import heapq
import math
from collections import deque
from dataclasses import dataclass, field

INF = math.inf


@dataclass
class Result:
    name: str
    route: list                     # nodes from start to goal; [] if there is no route
    length: float                   # cost along the route: metres (or seconds on a travel-time map)
    log: list                       # what the search did, in order (see the top of this file)
    notes: dict = field(default_factory=dict)   # extra numbers, e.g. the rounds of anytime A*

    @property
    def visited(self):
        """How many times a node was taken off the frontier and expanded."""
        return sum(1 for e in self.log if e[0] == "visit")

    @property
    def explored(self):
        """How many different edges (moves between two nodes) the search looked at."""
        return len({frozenset(e[1:3]) for e in self.log if e[0] == "look"})


class Log(list):
    def visit(self, node, side=0):
        self.append(("visit", node, side))

    def look(self, a, b, added, side=0):
        self.append(("look", a, b, added, side))


def walk_back(parent, node):
    """Follow the parent links from node back to the start, then turn the list around."""
    route = []
    while node is not None:
        route.append(node)
        node = parent[node]
    return route[::-1]


def result(name, m, parent, goal, log, **notes):
    route = walk_back(parent, goal) if goal in parent else []
    return Result(name, route, m.route_length(route), log, notes)


# ---------------------------------------------------------------- searches that ignore the cost of a move

def bfs(m, start, goal):
    """Breadth-first search: a first-in, first-out queue, so nodes are visited in rings of 1 move, 2 moves, ...
    The route has the fewest moves (not the fewest metres)."""
    log, parent = Log(), {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        log.visit(u)
        if u == goal:
            break
        for v in m.neighbours(u):
            added = v not in parent
            log.look(u, v, added)
            if added:
                parent[v] = u
                queue.append(v)
    return result("Breadth-first search", m, parent, goal, log)


def dfs(m, start, goal):
    """Depth-first search: a last-in, first-out stack, so it follows one way as far as it goes before backing up.
    It finds a route, but often a long one."""
    log, parent, done = Log(), {start: None}, set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in done:
            continue                           # an old copy of a node already visited
        done.add(u)
        log.visit(u)
        if u == goal:
            break
        for v in m.neighbours(u):
            added = v not in done
            log.look(u, v, added)
            if added:
                parent[v] = u                  # the last node to push v is the one v will be reached from
                stack.append(v)
    return result("Depth-first search", m, parent, goal, log)


# ---------------------------------------------------------------- best-first searches with a priority queue

def best_first(m, start, goal, priority, name, heuristic=None):
    """The loop shared by Dijkstra, greedy best-first, A* and weighted A*: always expand the frontier node with the
    smallest priority(g, h), where g = cost from the start so far and h = the heuristic's guess of the cost still
    to go (by default m.heuristic, the straight line). Only the priority differs between them."""
    heuristic = heuristic or m.heuristic
    log, parent, g, done = Log(), {start: None}, {start: 0.0}, set()
    h = heuristic(start, goal)
    frontier = [(priority(0.0, h), h, 0, start)]   # (priority, h, order pushed, node): ties go to the smaller h
    pushed = 1
    while frontier:
        _, _, _, u = heapq.heappop(frontier)
        if u in done:
            continue                           # an old copy with a longer cost
        done.add(u)
        log.visit(u)
        if u == goal:
            break
        for v in m.neighbours(u):
            new_g = g[u] + m.cost(u, v)
            added = v not in done and new_g < g.get(v, INF)
            log.look(u, v, added)
            if added:
                g[v], parent[v] = new_g, u
                h = heuristic(v, goal)
                heapq.heappush(frontier, (priority(new_g, h), h, pushed, v))
                pushed += 1
    return result(name, m, parent, goal, log)


def dijkstra(m, start, goal):
    """Dijkstra: expand the node with the smallest g, the metres from the start. Stops when the goal is expanded."""
    return best_first(m, start, goal, lambda g, h: g, "Dijkstra")


def greedy(m, start, goal):
    """Greedy best-first search: expand the node with the smallest h, the straight-line metres to the goal."""
    return best_first(m, start, goal, lambda g, h: h, "Greedy best-first")


def a_star(m, start, goal, heuristic=None, name="A*"):
    """A*: expand the node with the smallest f = g + h, the cost so far plus a guess of the cost still to go. If
    the guess never overestimates, the route is the shortest. heuristic(a, b) replaces m.heuristic if given."""
    return best_first(m, start, goal, lambda g, h: g + h, name, heuristic)


def weighted_a_star(m, start, goal, eps=2.0):
    """Weighted A*: f = g + eps * h. Trusting the guess more expands fewer nodes; the route is at most eps times
    the shortest."""
    return best_first(m, start, goal, lambda g, h: g + eps * h, f"Weighted A* (ε = {eps:g})")


def anytime_a_star(m, start, goal, eps_list=(2.5, 1.5, 1.0)):
    """Anytime A*: run weighted A* with eps falling. The first round gives a route quickly, each later round a
    shorter one, and eps = 1 gives the shortest. (A simple version: each round starts from scratch.)"""
    log, rounds = Log(), []
    for eps in eps_list:
        r = weighted_a_star(m, start, goal, eps)
        log.append(("round", f"ε = {eps:g}"))
        log.extend(r.log)
        log.append(("route", r.route, r.length))
        rounds.append((eps, r.length, r.visited))
    return Result("Anytime A*", r.route, r.length, log, {"rounds": rounds})


class WithVirtualGoal:
    """The map plus one extra node, the virtual goal, joined to each real goal by a move that costs 0 m. Reaching
    the virtual goal by the shortest route means reaching the nearest real goal by the shortest route."""
    VIRTUAL = "virtual goal"

    def __init__(self, m, goals):
        self.m, self.goals = m, set(goals)

    def neighbours(self, node):
        if node == self.VIRTUAL:
            return []
        return list(self.m.neighbours(node)) + ([self.VIRTUAL] if node in self.goals else [])

    def cost(self, a, b):
        return 0.0 if b == self.VIRTUAL else self.m.cost(a, b)

    def heuristic(self, a, b):
        if a == self.VIRTUAL:
            return 0.0
        return min(self.m.heuristic(a, g) for g in self.goals)   # straight line to the nearest real goal

    def route_length(self, route):
        return sum(self.cost(a, b) for a, b in zip(route, route[1:]))


def multi_goal_a_star(m, start, goals):
    """Multi-goal A*: the route to the nearest of several goals, found by one A* run to a virtual goal."""
    r = a_star(WithVirtualGoal(m, goals), start, WithVirtualGoal.VIRTUAL)
    V = WithVirtualGoal.VIRTUAL
    log = [e for e in r.log if V not in e[1:3]]
    route = [n for n in r.route if n != V]
    return Result("Multi-goal A*", route, m.route_length(route), log, {"reached": route[-1] if route else None})


# ---------------------------------------------------------------- bidirectional search

def bidirectional(m, start, goal):
    """Bidirectional Dijkstra: one search grows from the start (side 0), one from the goal (side 1), always the side
    whose next node is nearer its own end. Every time a node is reached from both sides we have a candidate route;
    we stop when the two next nodes together are at least as far as the best candidate. Moves must cost the same
    both ways (true for our grids and streets)."""
    log, ends = Log(), (start, goal)
    g = [{start: 0.0}, {goal: 0.0}]
    parent = [{start: None}, {goal: None}]
    done = [set(), set()]
    frontier = [[(0.0, 0, start)], [(0.0, 0, goal)]]
    pushed, best, meet = 1, INF, start if start == goal else None
    if start == goal:
        best = 0.0
    while frontier[0] and frontier[1] and frontier[0][0][0] + frontier[1][0][0] < best:
        side = 0 if frontier[0][0][0] <= frontier[1][0][0] else 1
        d, _, u = heapq.heappop(frontier[side])
        if u in done[side]:
            continue
        done[side].add(u)
        log.visit(u, side)
        for v in m.neighbours(u):
            new_g = d + m.cost(u, v)
            added = v not in done[side] and new_g < g[side].get(v, INF)
            log.look(u, v, added, side)
            if added:
                g[side][v], parent[side][v] = new_g, u
                heapq.heappush(frontier[side], (new_g, pushed, v))
                pushed += 1
                if v in g[1 - side] and new_g + g[1 - side][v] < best:
                    best, meet = new_g + g[1 - side][v], v
    if meet is None:
        return Result("Bidirectional search", [], 0.0, log)
    route = walk_back(parent[0], meet) + walk_back(parent[1], meet)[::-1][1:]
    return Result("Bidirectional search", route, m.route_length(route), log, {"meet": meet, "ends": ends})


# ---------------------------------------------------------------- iterative deepening A*

def ida_star(m, start, goal, max_visits=3_000_000):
    """IDA*: depth-first search that gives up on any route whose f = g + h is over a bound. If the goal is not
    found, the bound rises to the smallest f that went over it and the search starts again. It keeps only the
    current route in memory, but visits the same nodes again in every round. Stops after max_visits visits."""
    log, path, on_path = Log(), [start], {start}
    visits = 0

    def search(g, bound):
        """Returns None when the goal is reached, otherwise the smallest f that went over the bound."""
        nonlocal visits
        u = path[-1]
        f = g + m.heuristic(u, goal)
        if f > bound:
            return f
        log.visit(u)
        visits += 1
        if u == goal:
            return None
        if visits >= max_visits:
            return INF
        smallest = INF
        for v in m.neighbours(u):
            if v in on_path:
                continue                       # never walk in a circle
            log.look(u, v, True)
            path.append(v)
            on_path.add(v)
            t = search(g + m.cost(u, v), bound)
            if t is None:
                return None
            smallest = min(smallest, t)
            path.pop()
            on_path.discard(v)
        return smallest

    bound, rounds = m.heuristic(start, goal), 0
    while True:
        log.append(("round", f"bound {bound:.1f} m"))
        rounds += 1
        t = search(0.0, bound)
        if t is None:
            return Result("IDA*", list(path), m.route_length(path), log, {"rounds": rounds})
        if t == INF:                           # no route, or gave up
            return Result("IDA*", [], 0.0, log, {"rounds": rounds, "gave up": visits >= max_visits})
        bound = t


def ida_star_in_reach(m, start, goal, max_visits=1_000_000):
    """IDA* to the goal; if it gives up after max_visits visits, IDA* to the node halfway along A*'s route instead,
    and so on. The result's notes say which goal it reached and what it gave up on (goal, visits, rounds)."""
    route, gave_up = a_star(m, start, goal).route, []
    while True:
        r = ida_star(m, start, route[-1], max_visits)
        if r.route:
            r.notes.update(goal=route[-1], gave_up=gave_up)
            return r
        gave_up.append((route[-1], r.visited, r.notes["rounds"]))
        route = route[: len(route) // 2 + 1]


# ---------------------------------------------------------------- heuristics: guesses of the cost still to go
# Each takes the map and returns h(a, b). A* finds the shortest route if h never overestimates (admissible); the
# closer h is to the true cost, the fewer nodes A* expands.

def zero(m):
    """No guess at all: A* becomes Dijkstra."""
    return lambda a, b: 0.0


def manhattan(m):
    """Metres east-west plus metres north-south: exact for a robot that can only move along the axes, but too
    big for a diagonal move (it counts 2 cells where the move is 1.41), so on our 8-way grid it can overestimate."""
    return lambda a, b: abs(m.xy(a)[0] - m.xy(b)[0]) + abs(m.xy(a)[1] - m.xy(b)[1])


def straight_line(m):
    """The straight-line distance (the default heuristic of every map)."""
    return lambda a, b: math.dist(m.xy(a), m.xy(b))


def octile(m):
    """The length of the best route on an empty 8-way grid: diagonal steps for the shorter side, straight steps
    for the rest. Exact when nothing is in the way, never too big."""
    def h(a, b):
        dx, dy = abs(m.xy(a)[0] - m.xy(b)[0]), abs(m.xy(a)[1] - m.xy(b)[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    return h


def costs_from(m, source):
    """Dijkstra over the whole map without a goal: the cheapest cost from source to every node."""
    dist, frontier = {source: 0.0}, [(0.0, 0, source)]
    pushed = 1
    while frontier:
        d, _, u = heapq.heappop(frontier)
        if d > dist[u]:
            continue
        for v in m.neighbours(u):
            if d + m.cost(u, v) < dist.get(v, INF):
                dist[v] = d + m.cost(u, v)
                heapq.heappush(frontier, (dist[v], pushed, v))
                pushed += 1
    return dist


def landmarks(m, landmark_nodes):
    """ALT (A*, landmarks, triangle inequality): costs from a few landmarks L to every node are worked out once.
    For any a, b: cost(a -> b) >= |cost(L -> b) - cost(L -> a)|, so the largest of these is a guess that never
    overestimates. Moves must cost the same both ways."""
    tables = [costs_from(m, L) for L in landmark_nodes]
    return lambda a, b: max(abs(t[b] - t[a]) for t in tables)


def far_apart(m, k, first=None):
    """k landmarks spread over the map: each next one is the node whose cost from the nearest chosen one is
    largest (the first is the node farthest from `first`, or from any node)."""
    first = first if first is not None else next(iter(m.nodes()))
    d = costs_from(m, first)
    chosen = [max(d, key=d.get)]
    nearest = costs_from(m, chosen[0])
    while len(chosen) < k:
        chosen.append(max(nearest, key=nearest.get))
        new = costs_from(m, chosen[-1])
        nearest = {n: min(nearest[n], new[n]) for n in nearest}
    return chosen


def exact(m, goal):
    """The true cost still to go, from one Dijkstra run backwards from the goal (moves cost the same both ways).
    The perfect heuristic: A* then expands little more than the route itself. It only works for this one goal."""
    to_goal = costs_from(m, goal)
    return lambda a, b: to_goal[a]


# ---------------------------------------------------------------- grid-only searches

def jump_point_search(m, start, goal):
    """Jump point search (JPS): A* on a grid that skips the cells in between. From a node it scans straight or
    diagonally across open floor and only stops ("jumps") at a cell where a shorter route could turn: the goal, or
    a cell next to an obstacle corner. The route and its length are the same as grid A*'s; far fewer nodes go
    onto the frontier. Needs m.passable(col, row). Diagonal moves never cut a corner, as in the grid."""
    log, parent, g, done = Log(), {start: None}, {start: 0.0}, set()
    free = m.passable

    def jump(c, r, dc, dr):
        """Step from (c, r) in direction (dc, dr) until a jump point; return it, or None at a dead end."""
        while True:
            if dc and dr and not (free(c + dc, r) and free(c, r + dr)):
                return None                    # the diagonal step would cut a corner
            c, r = c + dc, r + dr
            if not free(c, r):
                return None
            log.append(("scan", (c, r)))
            if (c, r) == goal:
                return (c, r)
            if dc and dr:                      # diagonal: stop if a straight scan from here finds something
                if scan_straight(c, r, dc, 0) or scan_straight(c, r, 0, dr):
                    return (c, r)
            elif dc:                           # sideways: stop where a cell above or below opens up behind a wall
                if (free(c, r - 1) and not free(c - dc, r - 1)) or (free(c, r + 1) and not free(c - dc, r + 1)):
                    return (c, r)
            else:                              # up or down: the same, left and right
                if (free(c - 1, r) and not free(c - 1, r - dr)) or (free(c + 1, r) and not free(c + 1, r - dr)):
                    return (c, r)

    def scan_straight(c, r, dc, dr):
        return jump(c, r, dc, dr) is not None

    def directions(u):
        """The directions worth scanning from u, given the direction we arrived in (all 8 at the start)."""
        if parent[u] is None:
            return [(dc, dr) for dc in (-1, 0, 1) for dr in (-1, 0, 1) if dc or dr]
        (c, r), (pc, pr) = u, parent[u]
        dc, dr = (c > pc) - (c < pc), (r > pr) - (r < pr)
        if dc and dr:
            return [(dc, 0), (0, dr), (dc, dr)]
        if dc:
            return [(dc, 0), (dc, 1), (dc, -1), (0, 1), (0, -1)]
        return [(0, dr), (1, dr), (-1, dr), (1, 0), (-1, 0)]

    h = m.heuristic(start, goal)
    frontier, pushed = [(h, h, 0, start)], 1
    while frontier:
        _, _, _, u = heapq.heappop(frontier)
        if u in done:
            continue
        done.add(u)
        log.visit(u)
        if u == goal:
            break
        for dc, dr in directions(u):
            v = jump(u[0], u[1], dc, dr)
            if v is None:
                continue
            new_g = g[u] + math.dist(m.xy(u), m.xy(v))
            added = v not in done and new_g < g.get(v, INF)
            log.look(u, v, added)
            if added:
                g[v], parent[v] = new_g, u
                h = m.heuristic(v, goal)
                heapq.heappush(frontier, (new_g + h, h, pushed, v))
                pushed += 1
    jumps = walk_back(parent, goal) if goal in parent else []
    route = [jumps[0]] if jumps else []
    for a, b in zip(jumps, jumps[1:]):         # fill in the cells between jump points
        dc, dr = (b[0] > a[0]) - (b[0] < a[0]), (b[1] > a[1]) - (b[1] < a[1])
        c, r = a
        while (c, r) != b:
            c, r = c + dc, r + dr
            route.append((c, r))
    scanned = sum(1 for e in log if e[0] == "scan")
    return Result("Jump point search", route, m.route_length(route), log, {"jump points": jumps, "scanned": scanned})


def theta_star(m, start, goal):
    """Theta*: A* on a grid whose routes may run at any angle. When it reaches a neighbour v from u, it checks
    whether v can be seen in a straight line from u's parent; if so, v hangs on u's parent and the corner at u is
    cut. The route is a list of turning points. Needs m.line_of_sight(a, b)."""
    log, parent, g, done = Log(), {start: None}, {start: 0.0}, set()
    dist = lambda a, b: math.dist(m.xy(a), m.xy(b))
    h = m.heuristic(start, goal)
    frontier, pushed = [(h, h, 0, start)], 1
    while frontier:
        _, _, _, u = heapq.heappop(frontier)
        if u in done:
            continue
        done.add(u)
        log.visit(u)
        if u == goal:
            break
        for v in m.neighbours(u):
            if v in done:
                continue
            p = parent[u]
            if p is not None and m.line_of_sight(p, v):
                via, new_g = p, g[p] + dist(p, v)     # straight from u's parent: cut the corner at u
            else:
                via, new_g = u, g[u] + dist(u, v)
            added = new_g < g.get(v, INF)
            log.look(via, v, added)
            if added:
                g[v], parent[v] = new_g, via
                h = m.heuristic(v, goal)
                heapq.heappush(frontier, (new_g + h, h, pushed, v))
                pushed += 1
    route = walk_back(parent, goal) if goal in parent else []
    length = sum(dist(a, b) for a, b in zip(route, route[1:]))
    return Result("Theta*", route, length, log)
