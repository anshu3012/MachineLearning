"""Checks every search against networkx on each map in maps/ (plain asserts; prints one line per map).

    python check_algorithms.py"""
import math
import random

import networkx as nx
import numpy as np

import algorithms as A
from grid import MAPS, Grid, load_grid
from run import SEARCHES, heuristic_runs

close = lambda a, b: math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def connected(m, route, start, goal):
    """The route starts at start, ends at goal, and each step is one move on the map."""
    return route[0] == start and route[-1] == goal and all(b in m.neighbours(a) for a, b in zip(route, route[1:]))


def check_map(m):
    G = m.to_networkx()
    best = nx.shortest_path_length(G, m.start, m.goal, weight="length")
    r = {key: f(m) for key, f in SEARCHES}
    for key in ("dijkstra", "a_star", "bidirectional", "anytime_a_star", "jps"):
        assert close(r[key].length, best), (m.name, key, r[key].length, best)
    assert len(r["bfs"].route) - 1 == nx.shortest_path_length(G, m.start, m.goal), m.name
    assert r["weighted_a_star"].length <= 2.0 * best + 1e-9, m.name
    assert all(length <= eps * best + 1e-9 for eps, length, _ in r["anytime_a_star"].notes["rounds"]), m.name
    nearest = min(nx.shortest_path_length(G, m.start, g, weight="length") for g in m.goals)
    assert close(r["multi_goal"].length, nearest) and r["multi_goal"].route[-1] in m.goals, m.name
    each = A.a_star_each(m, m.start, m.goals)              # one A* run per goal finds the same nearest goal
    assert close(each.length, nearest) and connected(m, each.route, m.start, each.route[-1]), m.name
    ida_goal = r["ida_star"].notes["goal"]
    assert close(r["ida_star"].length, nx.shortest_path_length(G, m.start, ida_goal, weight="length")), m.name
    assert r["theta_star"].length <= r["a_star"].length + 1e-9, m.name
    theta = r["theta_star"].route
    assert theta[0] == m.start and theta[-1] == m.goal and all(m.line_of_sight(a, b) for a, b in zip(theta, theta[1:]))
    for key, res in r.items():
        if key == "theta_star":
            continue
        end = {"multi_goal": res.route[-1], "ida_star": ida_goal}.get(key, m.goal)
        assert connected(m, res.route, m.start, end), (m.name, key)
        assert close(res.length, m.route_length(res.route)), (m.name, key)
    # heuristics: the admissible ones never overestimate and give the shortest route; tighter means fewer visits
    h, true = heuristic_runs(m), A.costs_from(m, m.goal)
    over = {k: max(getattr(A, k)(m)(n, m.goal) - true[n] for n in true) for k in ("straight_line", "octile", "manhattan")}
    assert over["straight_line"] <= 1e-9 and over["octile"] <= 1e-9, over
    for key in ("zero", "straight_line", "octile"):
        assert close(h[key].length, best), (m.name, key)
    assert h["zero"].visited >= h["straight_line"].visited >= h["octile"].visited, m.name
    if over["manhattan"] <= 1e-9:
        assert close(h["manhattan"].length, best)
    print(f"{m.name}: all {len(r)} searches and 4 heuristics pass; shortest route {best:.2f} m; "
          f"Theta* {r['theta_star'].length:.2f} m; Manhattan overestimates by up to {over['manhattan']:.2f} m, "
          f"its route {h['manhattan'].length:.2f} m; nearest goal {nearest:.2f} m: {each.visited} cells visited "
          f"by one A* per goal, {r['multi_goal'].visited} by multi-goal A*")


def check_random_floors(n=40, seed=0):
    """Jump point search must match A* and Theta* must not be longer, on many random floors too."""
    rng = random.Random(seed)
    for _ in range(n):
        free = np.array([[rng.random() > 0.3 for _ in range(24)] for _ in range(16)])
        cells = [(c, r) for r in range(16) for c in range(24) if free[r, c]]
        m = Grid(free, start=rng.choice(cells), goal=rng.choice(cells))
        a = A.a_star(m, m.start, m.goal)
        j = A.jump_point_search(m, m.start, m.goal)
        t = A.theta_star(m, m.start, m.goal)
        assert bool(a.route) == bool(j.route) == bool(t.route)
        if a.route:
            assert close(a.length, j.length) and connected(m, j.route, m.start, m.goal), (m.start, m.goal)
            assert t.length <= a.length + 1e-9
    print(f"{n} random floors: jump point search = A*, Theta* <= A*")


if __name__ == "__main__":
    for png in sorted(MAPS.glob("*.png")):
        if not png.stem.endswith("_preview"):
            check_map(load_grid(png))
    check_random_floors()
