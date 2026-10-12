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
    ("raise", node, old, new)      LRTA* raised its guess at node
side is 0, except in bidirectional search and the contraction hierarchy query, where the search from the goal uses
side 1 (D* Lite uses side 1 for a number that rises).

A new search is a new function that fills a Log and returns a Result; the drawing code needs nothing new. The
heuristics (guesses of the cost still to go) are near the end: zero, manhattan, straight_line, octile, landmarks
and exact; a_star(m, start, goal, heuristic) takes any of them. Chapter RO-06's methods come last: walking downhill
on the cost-to-go (navigation function), value iteration, D* Lite and a replanning drive, LRTA*, fast marching, and
contraction hierarchies."""
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


def a_star_each(m, start, goals):
    """The plain way to the nearest goal: one A* run per goal, then keep the shortest route. Every run starts
    afresh, so the work adds up. The log is the runs one after another, each ending with the route it found;
    notes["runs"] holds (goal, route cost, edges explored, nodes visited) for each run."""
    log, runs, best = Log(), [], None
    for goal in goals:
        r = a_star(m, start, goal)
        log.extend(r.log)
        log.append(("route", r.route, r.length))
        runs.append((goal, r.length, r.explored, r.visited))
        if r.route and (best is None or r.length < best.length):
            best = r
    return Result("A* once per goal", best.route if best else [], best.length if best else 0.0, log,
                  {"runs": runs, "explored": sum(x[2] for x in runs)})


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


# ---------------------------------------------------------------- cost-to-go maps (chapter RO-06)
# A backward search from the goal gives every node its cost-to-go, the cost of its cheapest route to the goal:
# costs_from(m, goal) above does it with Dijkstra (the wavefront in metres). The functions below walk down those
# numbers, compute them by value iteration, keep them right while the map changes (D* Lite), learn them on the
# move (LRTA*), or compute them for a front that may cross the cells at any angle (fast marching).

def downhill(m, V, node):
    """The navigation function's rule: the neighbour with the smallest move + cost-to-go (ties to the smaller
    cost-to-go). Each step lowers the cost-to-go by exactly the move made."""
    return min(m.neighbours(node), key=lambda n: (round(m.cost(node, n) + V.get(n, INF), 9), V.get(n, INF)))


def walk_downhill(m, V, start):
    """The route from start that follows downhill() until the cost-to-go is 0 (the goal)."""
    route = [start]
    while V[route[-1]] > 0:
        route.append(downhill(m, V, route[-1]))
    return route


def value_iteration(m, goal):
    """Value iteration: every node starts at infinity (the goal at 0). A sweep visits the nodes in m.nodes() order
    (on a grid: row by row from the top, left to right) and sets each to its smallest move + neighbour's value, in
    place, so a node already uses values given earlier in the same sweep. Sweeps repeat until one changes nothing.
    Returns the values and one record per sweep: (the values after it, the nodes that got their first value, the
    nodes whose value fell)."""
    nodes = [n for n in m.nodes() if n != goal]
    V = {n: INF for n in nodes}
    V[goal] = 0.0
    sweeps = []
    while True:
        first, fell = [], []
        for x in nodes:
            best = min((m.cost(x, n) + V[n] for n in m.neighbours(x)), default=INF)
            if best < V[x] - 1e-12:
                (first if V[x] == INF else fell).append(x)
                V[x] = best
        sweeps.append((dict(V), first, fell))
        if not first and not fell:
            return V, sweeps


class DStarLite:
    """D* Lite (Koenig and Likhachev 2002): the cost-to-go to the goal, kept from a backward search and repaired
    when the map changes. g[s] is the number a node holds; its lookahead rhs(s) is the smallest move + neighbour's
    g. A node whose g differs from its lookahead waits in a priority queue with the key
    (min(g, rhs) + h(robot, s) + km, min(g, rhs)), so the nodes on the robot's side are fixed first. A node taken off
    either falls to its lookahead (final, as in Dijkstra) or, if its way got longer, rises to infinity and waits
    to fall later. The map m is read at every call: change it (block a cell, close a street), then call changed()
    with the nodes whose moves changed. Moves must cost the same both ways.
    log: ("visit", node, 0) when a number falls, ("visit", node, 1) when it rises, ("look", node, n, True, side)
    for each neighbour n whose lookahead is then rechecked."""

    def __init__(self, m, start, goal):
        self.m, self.start, self.goal, self.last, self.km = m, start, goal, start, 0.0
        self.g, self.rhs = {}, {goal: 0.0}
        self.queue, self.queued = [], {}           # heap of (key, order, node); node -> its current key
        self.pushed = 0
        self.log = Log()
        self._push(goal)

    def G(self, s):
        return self.g.get(s, INF)

    def R(self, s):
        return self.rhs.get(s, INF)

    def key(self, s):
        """Rounded, so that two keys equal in exact arithmetic tie and the second part decides (else rounding
        noise can stop the repair one node too early)."""
        k = min(self.G(s), self.R(s))
        return (round(k + self.m.heuristic(self.start, s) + self.km, 9), round(k, 9))

    def _push(self, s):
        self.queued[s] = self.key(s)
        heapq.heappush(self.queue, (self.queued[s], self.pushed, s))
        self.pushed += 1

    def update(self, s):
        """Recompute the lookahead of s; queue s if it now disagrees with its number."""
        if s != self.goal:
            self.rhs[s] = min((self.m.cost(s, n) + self.G(n) for n in self.m.neighbours(s)), default=INF)
        self.queued.pop(s, None)
        if self.G(s) != self.R(s):
            self._push(s)

    def _top(self):
        while self.queue:
            k, _, s = self.queue[0]
            if self.queued.get(s) == k:
                return k, s
            heapq.heappop(self.queue)              # an old copy
        return (INF, INF), None

    def compute(self):
        """Take nodes off the queue until the robot's node agrees with its lookahead and no queued key is smaller
        than its key. Returns how many nodes were taken off."""
        n = 0
        while True:
            k, s = self._top()
            if s is None or not (k < self.key(self.start) or self.R(self.start) != self.G(self.start)):
                return n
            heapq.heappop(self.queue)
            del self.queued[s]
            if k < self.key(s):                    # its key grew since it was queued: queue it again
                self._push(s)
                continue
            n += 1
            rise = self.G(s) <= self.R(s)
            self.g[s] = INF if rise else self.R(s)
            self.log.visit(s, int(rise))
            if rise:
                self.update(s)
            for p in self.m.neighbours(s):
                self.log.look(s, p, True, int(rise))
                self.update(p)

    def moved(self, pos):
        """The robot is now at pos. km keeps the keys made before the move comparable with new ones."""
        self.km += self.m.heuristic(self.last, pos)
        self.last = self.start = pos

    def changed(self, nodes):
        """The moves of these nodes changed (a cell blocked, a street closed): recheck their lookaheads."""
        for s in nodes:
            self.update(s)

    def step(self):
        """The robot's next node: downhill on the numbers, or None if no route is left."""
        if self.G(self.start) == INF:
            return None
        return downhill(self.m, self.g, self.start)


def drive(m, discover):
    """The robot drives from m.start to m.goal planning with D* Lite on map m, its map of the world. Before every
    move, discover(pos) may change m (a cell found blocked, a street found closed) and returns the nodes whose moves
    changed; D* Lite then repairs its numbers, and A* from scratch runs from the robot's node at the same moment for
    comparison. Returns a Result: the route driven; notes["first"] = (D* Lite's first plan, A*'s first plan) and
    notes["replans"] = one dict per replan (move: moves driven so far, pos, changed, dstar: the repair, astar: A*
    from scratch). Each plan is a Result whose route is the plan from the robot's node and whose log is that
    plan's work, so .visited counts the nodes taken off its queue."""
    d = DStarLite(m, m.start, m.goal)

    def plan(pos):
        route = walk_downhill(m, d.g, pos) if d.G(pos) < INF else []
        return Result("D* Lite", route, d.G(pos), d.log)

    d.compute()
    first = (plan(m.start), a_star(m, m.start, m.goal))
    pos, route, replans, driven = m.start, [m.start], [], 0.0
    while pos != m.goal:
        changed = discover(pos)
        if changed:
            d.moved(pos)
            d.log = Log()
            d.changed(changed)
            d.compute()
            replans.append(dict(move=len(route) - 1, pos=pos, changed=changed, dstar=plan(pos),
                                astar=a_star(m, pos, m.goal)))
        d.start = pos
        pos = d.step()
        if pos is None:
            break
        driven += m.cost(route[-1], pos)       # summed while driving: a move driven may close later
        route.append(pos)
    return Result("D* Lite", route, driven, first[0].log, {"first": first, "replans": replans})


def lrta_star(m, start, goal, heuristic=None, learned=None, max_moves=100_000):
    """LRTA*, learning real-time A* (Korf 1990), with a lookahead of one move. The robot's guess of each node's
    cost to the goal starts as heuristic(node, goal) (default m.heuristic). At each node it raises the node's guess
    to the smallest move + neighbour's guess, if that is larger, and moves to that neighbour (ties to the smaller
    guess). learned holds the raised guesses; pass the same dict again to run another trial with what was learned.
    The log has ("visit", node, 0) per move and ("raise", node, old, new) per raised guess."""
    heuristic = heuristic or m.heuristic
    h = {} if learned is None else learned
    H = lambda n: h.get(n, heuristic(n, goal))
    log, route = Log(), [start]
    while route[-1] != goal and len(route) <= max_moves:
        node = route[-1]
        log.visit(node)
        nxt = min(m.neighbours(node), key=lambda n: (round(m.cost(node, n) + H(n), 9), H(n)))
        best = m.cost(node, nxt) + H(nxt)
        if best > H(node) + 1e-12:
            log.append(("raise", node, H(node), best))
            h[node] = best
        route.append(nxt)
    return Result("LRTA*", route, m.route_length(route), log,
                  {"raised": sum(1 for e in log if e[0] == "raise"), "learned": dict(h)})


def fast_marching(m, goal):
    """Fast marching (Sethian 1996) on a grid: the arrival time, at 1 m/s, of a front that leaves the centre of the
    goal's cell and may cross the cells at any angle. The loop is Dijkstra's: the cell with the smallest tentative
    time is accepted and never changed. Only the update differs: a cell's time comes from a = the smaller time of its
    left and right neighbours and b = the smaller of its upper and lower ones at once,
        T = (a + b + sqrt(2 h^2 - (a - b)^2)) / 2,   h the cell side,
    or the smaller of a and b plus h when only one is known or they differ by h or more. Needs m.passable and m.cell.
    Returns {cell: time} and the cells in the order they were accepted."""
    h, T, done, order = m.cell, {goal: 0.0}, set(), []
    frontier = [(0.0, goal)]
    while frontier:
        t, u = heapq.heappop(frontier)
        if u in done:
            continue
        done.add(u)
        order.append(u)
        c, r = u
        for v in ((c + 1, r), (c - 1, r), (c, r + 1), (c, r - 1)):
            if v in done or not m.passable(*v):
                continue
            a = min(T.get((v[0] - 1, v[1]), INF) if (v[0] - 1, v[1]) in done else INF,
                    T.get((v[0] + 1, v[1]), INF) if (v[0] + 1, v[1]) in done else INF)
            b = min(T.get((v[0], v[1] - 1), INF) if (v[0], v[1] - 1) in done else INF,
                    T.get((v[0], v[1] + 1), INF) if (v[0], v[1] + 1) in done else INF)
            if abs(a - b) < h:
                new = (a + b + math.sqrt(2 * h * h - (a - b) ** 2)) / 2
            else:
                new = min(a, b) + h
            if new < T.get(v, INF):
                T[v] = new
                heapq.heappush(frontier, (new, v))
    return T, order


# ---------------------------------------------------------------- contraction hierarchies (chapter RO-06)

def _witness(arcs, alive, src, skip, limit):
    """Dijkstra from src over the nodes still in the graph, never through skip, stopping beyond limit."""
    d, frontier, done = {src: 0.0}, [(0.0, 0, src)], set()
    pushed = 1
    while frontier:
        du, _, u = heapq.heappop(frontier)
        if u in done or du > limit:
            continue
        done.add(u)
        for v, c in arcs[u].items():
            if v != skip and v in alive and du + c < d.get(v, INF):
                d[v] = du + c
                heapq.heappush(frontier, (d[v], pushed, v))
                pushed += 1
    return d


def _needed(arcs, alive, v):
    """The shortcuts that contracting v needs: for each two neighbours u, w of v still in the graph, the way
    u-v-w unless a witness search finds a way from u to w, avoiding v, that is no slower."""
    nb = [u for u in arcs[v] if u in alive]
    need = []
    for i, u in enumerate(nb[:-1]):
        targets = nb[i + 1:]
        d = _witness(arcs, alive, u, v, arcs[u][v] + max(arcs[v][w] for w in targets))
        need += [(u, w, arcs[u][v] + arcs[v][w]) for w in targets
                 if d.get(w, INF) > arcs[u][v] + arcs[v][w] + 1e-9]
    return need, len(nb)


def contraction_hierarchy(m):
    """Contraction hierarchy (Geisberger et al. 2008) of a map whose moves cost the same both ways. Nodes are
    removed (contracted) one at a time, least important first: the one with the smallest edge difference (shortcuts
    its removal adds minus the moves it removes) plus the number of its neighbours already contracted, re-checked
    just before it goes. Removing v adds a shortcut u-w with the cost of u-v-w for every two neighbours u, w still
    in the graph whose fastest way runs through v (no witness). Returns a dict: map, rank (node -> place in the
    order), arcs (node -> {neighbour: cost}: the moves plus the shortcuts), mid ((u, w) -> v for each shortcut),
    order, and shortcuts ((u, w, cost) in the order they were added, with the rank of the node that made them)."""
    arcs = {u: {v: m.cost(u, v) for v in m.neighbours(u)} for u in m.nodes()}
    alive, gone_nb = set(arcs), dict.fromkeys(arcs, 0)

    def prio(v):
        need, degree = _needed(arcs, alive, v)
        return len(need) - degree + gone_nb[v]

    queue = [(prio(v), i, v) for i, v in enumerate(arcs)]
    heapq.heapify(queue)
    rank, mid, order, shortcuts = {}, {}, [], []
    while queue:
        _, i, v = heapq.heappop(queue)
        p = prio(v)
        if queue and p > queue[0][0]:              # its priority grew: put it back
            heapq.heappush(queue, (p, i, v))
            continue
        for u, w, cost in _needed(arcs, alive, v)[0]:
            if cost < arcs[u].get(w, INF):
                arcs[u][w] = arcs[w][u] = cost
                mid[(u, w)] = mid[(w, u)] = v
                shortcuts.append((u, w, cost, len(order)))
        alive.discard(v)
        rank[v] = len(order)
        order.append(v)
        for u in arcs[v]:
            if u in alive:
                gone_nb[u] += 1
    return dict(map=m, rank=rank, arcs=arcs, mid=mid, order=order, shortcuts=shortcuts)


def unpack(ch, u, w):
    """The map's nodes along the arc u-w: a shortcut is replaced by its two halves, again and again."""
    if (u, w) not in ch["mid"]:
        return [u, w]
    v = ch["mid"][(u, w)]
    return unpack(ch, u, v)[:-1] + unpack(ch, v, w)


def ch_query(ch, start, goal):
    """The query on a contraction hierarchy: a search from the start (side 0) and one back from the goal (side 1),
    one node off each in turn, each following only arcs that climb to a higher rank. A node taken off by both gives
    a route; a search stops once its smallest cost is at least the best route so far. The route's shortcuts are
    unpacked into moves of the map. notes: the node where the searches met (top), the nodes each side took off,
    and the arcs of the route before unpacking (hops)."""
    rank, arcs = ch["rank"], ch["arcs"]
    log, d = Log(), ({start: 0.0}, {goal: 0.0})
    parent, done = ({start: None}, {goal: None}), (set(), set())
    frontier, pushed = ([(0.0, 0, start)], [(0.0, 0, goal)]), 1
    best, top, side = INF, None, 0
    while frontier[0] or frontier[1]:
        if frontier[side] and frontier[side][0][0] >= best:
            frontier[side].clear()                 # nothing on this side can give a faster route
        if not frontier[side]:
            side ^= 1
            continue
        du, _, u = heapq.heappop(frontier[side])
        if u in done[side]:
            continue
        done[side].add(u)
        log.visit(u, side)
        if u in done[1 - side] and du + d[1 - side][u] < best:
            best, top = du + d[1 - side][u], u
        for v, c in arcs[u].items():
            if rank[v] > rank[u]:
                added = du + c < d[side].get(v, INF)
                log.look(u, v, added, side)
                if added:
                    d[side][v], parent[side][v] = du + c, u
                    heapq.heappush(frontier[side], (du + c, pushed, v))
                    pushed += 1
        side ^= 1
    if top is None:
        return Result("Contraction hierarchy", [], 0.0, log)
    hops = walk_back(parent[0], top) + walk_back(parent[1], top)[::-1][1:]
    route = [start]
    for a, b in zip(hops, hops[1:]):
        route += unpack(ch, a, b)[1:]
    taken = [sum(1 for e in log if e[0] == "visit" and e[2] == s) for s in (0, 1)]
    return Result("Contraction hierarchy", route, ch["map"].route_length(route), log,
                  {"top": top, "taken": taken, "hops": hops})
