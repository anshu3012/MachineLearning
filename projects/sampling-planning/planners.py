"""Four sampling-based planners: RRT, RRT*, RRT-Connect and PRM. PRM searches its roadmap with the grid project's A*.

The planners never see the world. They only call a `space`:
  space.sample(rng)          a random point (rng is a random.Random, so every run is seeded)
  space.distance(a, b)       length of the straight segment from a to b
  space.steer(a, b, step)    the point at most `step` from a toward b
  space.free(p)              True if the robot fits at p
  space.segment_free(a, b)   True if the robot can drive straight from a to b
  space.checks               how many point tests have been made so far
Points are (x, y) tuples. Each planner returns a dict: path (list of points, or None), length, samples, checks,
time (s) and events, one per step, which the animations replay."""
import heapq
import math
import random
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "grid-pathfinding"))
from algorithms import a_star  # noqa: E402  (projects/grid-pathfinding: A* on any map with its interface)
from map_interface import Map  # noqa: E402


def path_length(space, path):
    return sum(space.distance(a, b) for a, b in zip(path, path[1:]))


def branch(parent, p):
    """The tree path from p back to the root: p, its parent, its parent's parent, ..."""
    out = [p]
    while parent[out[-1]] is not None:
        out.append(parent[out[-1]])
    return out


def nearest(points, q, space):
    return min(points, key=lambda p: space.distance(p, q))


class Log:
    """Records one event per step, stamped with the collision checks and time used so far."""

    def __init__(self, space):
        self.space, self.checks0, self.t0, self.events = space, space.checks, time.perf_counter(), []

    def add(self, **event):
        event.update(checks=self.space.checks - self.checks0, time=time.perf_counter() - self.t0)
        self.events.append(event)

    def result(self, path, samples, **extra):
        last = self.events[-1]
        return dict(path=path, length=path_length(self.space, path) if path else None, samples=samples,
                    checks=last["checks"], time=last["time"], events=self.events, **extra)


def rrt(space, start, goal, step, seed=0, goal_bias=0.05, max_samples=5000):
    """RRT (LaValle 1998): grow one tree from the start, one step toward each random sample."""
    rng = random.Random(seed)
    parent, log = {start: None}, Log(space)
    for i in range(1, max_samples + 1):
        q = goal if rng.random() < goal_bias else space.sample(rng)  # 1. a random point, now and then the goal
        near = nearest(parent, q, space)  # 2. the tree node nearest to it
        new = space.steer(near, q, step)  # 3. one step from that node toward it
        ok = space.segment_free(near, new)  # 4. keep the step only if the robot can drive it
        added = []
        if ok:
            parent[new] = near
            added.append((new, near))
            if new != goal and space.distance(new, goal) <= step and space.segment_free(new, goal):
                parent[goal] = new  # 5. the goal is one free step away: join it
                added.append((goal, new))
        log.add(sample=q, near=near, new=new, ok=ok, set=added)
        if goal in parent:
            return log.result(branch(parent, goal)[::-1], i)
    return log.result(None, max_samples)


def rrt_star(space, start, goal, step, gamma, seed=0, goal_bias=0.05, samples=1500):
    """RRT* (Karaman and Frazzoli 2011): RRT that joins each new node through its cheapest neighbour, then rewires
    neighbours through the new node when that is shorter. It keeps sampling after it reaches the goal."""
    rng = random.Random(seed)
    parent, log = {start: None}, Log(space)

    def cost(p):  # length of the tree path from the start to p
        return path_length(space, branch(parent, p))

    def insert(new, near, radius):
        """Add new through its cheapest free neighbour, rewire neighbours through it. Returns the edges set."""
        if new in parent or not space.segment_free(near, new):
            return None
        close = [x for x in parent if space.distance(x, new) <= radius]
        best, best_cost = near, cost(near) + space.distance(near, new)
        for c, x in sorted((cost(x) + space.distance(x, new), x) for x in close):  # cheapest first
            if c >= best_cost:
                break
            if space.segment_free(x, new):
                best, best_cost = x, c
                break
        parent[new] = best
        edges = [(new, best)]
        for x in close:  # rewire: route x through new if that is shorter
            if x != best and best_cost + space.distance(new, x) < cost(x) and space.segment_free(new, x):
                parent[x] = new
                edges.append((x, new))
        return edges

    for i in range(1, samples + 1):
        q = goal if goal not in parent and rng.random() < goal_bias else space.sample(rng)
        near = nearest(parent, q, space)
        new = space.steer(near, q, step)
        n = len(parent) + 1
        radius = min(gamma * math.sqrt(math.log(n) / n), step)  # the neighbourhood shrinks as the tree grows
        added = insert(new, near, radius)
        if added and goal not in parent and space.distance(new, goal) <= step:
            added += insert(goal, new, radius) or []
        log.add(sample=q, near=near, new=new, ok=added is not None, set=added or [], radius=radius,
                cost=cost(goal) if goal in parent else None)
    return log.result(branch(parent, goal)[::-1] if goal in parent else None, samples)


def rrt_connect(space, start, goal, step, seed=0, max_samples=5000):
    """RRT-Connect (Kuffner and LaValle 2000): one tree from the start, one from the goal. Each round one tree takes a
    step toward a random sample, then the other tree steps straight at that new node until it gets there or is
    blocked. The trees swap roles every round."""
    rng = random.Random(seed)
    trees, log = [{start: None}, {goal: None}], Log(space)
    for i in range(1, max_samples + 1):
        a, b = (i - 1) % 2, i % 2  # tree a extends, tree b connects
        q = space.sample(rng)
        near = nearest(trees[a], q, space)
        new = space.steer(near, q, step)
        ok = space.segment_free(near, new) and new not in trees[a]
        if ok:
            trees[a][new] = near
        log.add(tree=a, sample=q, near=near, new=new, ok=ok, set=[(new, near)] if ok else [])
        if not ok:
            continue
        p, added = nearest(trees[b], new, space), []
        while p != new:  # connect: keep stepping toward new
            s = space.steer(p, new, step)
            if not space.segment_free(p, s):
                break
            trees[b][s] = p
            added.append((s, p))
            p = s
        log.add(tree=b, sample=None, near=None, new=new, ok=p == new, set=added)
        if p == new:  # the trees meet at new
            path = branch(trees[0], new)[::-1] + branch(trees[1], new)[1:]
            return log.result(path, i)
    return log.result(None, max_samples)


def prm(space, start, goal, n=500, k=10, seed=0):
    """PRM (Kavraki et al. 1996): 1. place n samples in free space, 2. join each to its k nearest samples when the
    segment between them is free (the roadmap), 3. join the start and the goal the same way and search with A*."""
    rng = random.Random(seed)
    nodes, log, drawn = [], Log(space), 0
    while len(nodes) < n:  # 1. samples that land on an obstacle are thrown away
        q = space.sample(rng)
        drawn += 1
        ok = space.free(q)
        if ok:
            nodes.append(q)
        log.add(phase="sample", sample=q, ok=ok)
    graph, tried = {p: {} for p in nodes}, set()

    def join(p, candidates):
        edges = []
        for x in candidates:
            if (x, p) in tried or x == p:
                continue
            tried.add((p, x))
            if space.segment_free(p, x):
                graph[p][x] = graph[x][p] = space.distance(p, x)
                edges.append((p, x))
        return edges

    def k_nearest(p):
        return heapq.nsmallest(k, (x for x in nodes if x != p), key=lambda x: space.distance(p, x))

    for p in nodes:  # 2. the roadmap
        log.add(phase="connect", node=p, edges=join(p, k_nearest(p)))
    edges = []
    for p in (start, goal):  # 3. the query
        graph[p] = {}
        edges += join(p, k_nearest(p))
    path = a_star(Roadmap(graph), start, goal).route or None
    log.add(phase="query", edges=edges, path=path)
    return log.result(path, drawn, graph=graph, k=k)


class Roadmap(Map):
    """PRM's roadmap {node: {neighbour: edge length}} behind the grid project's map interface, so that project's A*
    can search it. A node is a point; its straight-line distance to the goal is A*'s guess."""

    def __init__(self, graph):
        self.graph = graph

    def nodes(self):
        return list(self.graph)

    def neighbours(self, node):
        return list(self.graph[node])

    def cost(self, a, b):
        return self.graph[a][b]

    def xy(self, node):
        return node
