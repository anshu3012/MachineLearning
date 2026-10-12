"""Checks every search against networkx on each map in maps/ (plain asserts; prints one line per map).

    python check_algorithms.py"""
import math
import random

import networkx as nx
import numpy as np

import algorithms as A
from grid import MAPS, Grid, finer, load_grid
from run import SEARCHES, heuristic_runs, lrta_trials, replanning_drive

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


def real_floor(m):
    """The floor as it really is, the hidden cells blocked, as a networkx graph."""
    free = m.free.copy()
    for c, r in m.hidden:
        free[r, c] = False
    return Grid(free, cell=m.cell).to_networkx()


def check_cost_to_go(m):
    """Chapter RO-06: the wavefront numbers are the networkx distances to G; walking downhill from any cell is as
    long as its number; value iteration ends at the same numbers; D* Lite's repaired numbers equal A* from scratch;
    LRTA*'s guesses never overestimate and its last trial is a shortest route; the contraction hierarchy finds the
    shortest routes."""
    G = m.to_networkx()
    true = nx.single_source_dijkstra_path_length(G, m.goal, weight="length")
    V = A.costs_from(m, m.goal)
    assert V.keys() == true.keys() and all(close(V[n], true[n]) for n in V), m.name
    for n in V:
        assert n == m.goal or min(V[k] for k in m.neighbours(n)) < V[n], (m.name, n)   # no dent but the goal
        assert close(m.route_length(A.walk_downhill(m, V, n)), V[n]), (m.name, n)
    VI, record = A.value_iteration(m, m.goal)
    assert not record[-1][1] and not record[-1][2] and all(close(VI[n], V[n]) for n in V), m.name
    replans = 0
    if m.hidden:
        run, seen_at = replanning_drive(m)
        real = real_floor(m)
        assert run.route[-1] == m.goal and not set(run.route) & set(m.hidden), m.name
        assert all(b in real.adj[a] for a, b in zip(run.route, run.route[1:])), m.name   # moves on the real floor
        assert run.length >= nx.shortest_path_length(real, m.start, m.goal, weight="length") - 1e-9
        for e in run.notes["replans"]:
            assert close(e["dstar"].length, e["astar"].length), (m.name, e["move"])
        assert sorted(c for cells in seen_at.values() for c in cells) == sorted(m.hidden), m.name
        replans = len(run.notes["replans"])
    first, last = lrta_trials(m)
    assert first.route[-1] == m.goal and close(last.length, true[m.start]), m.name
    assert all(h <= true[n] + 1e-9 for n, h in last.notes["learned"].items()), m.name
    ch = A.contraction_hierarchy(m)
    rng = random.Random(1)
    for _ in range(50):
        s, t = rng.choice(list(V)), rng.choice(list(V))
        q = A.ch_query(ch, s, t)
        assert close(q.length, nx.shortest_path_length(G, s, t, weight="length")) and connected(m, q.route, s, t)
    print(f"{m.name}: cost-to-go of {len(V)} cells = networkx, downhill walks = their numbers, value iteration "
          f"= Dijkstra after {len(record)} sweeps; " + (f"D* Lite = A* at {replans} replans; " if replans else "") +
          f"LRTA* settles after {last.notes['trial']} trials on the shortest route; contraction hierarchy = "
          "networkx on 50 trips")


def check_replanning_random(n=30, seed=2):
    """D* Lite on random floors with random hidden cells: at every replan its number at the robot equals A* from
    scratch, and the robot reaches the goal whenever the real floor has a route."""
    rng = random.Random(seed)
    done = 0
    for _ in range(n):
        free = np.array([[rng.random() > 0.2 for _ in range(20)] for _ in range(14)])
        cells = [(c, r) for r in range(14) for c in range(20) if free[r, c]]
        start, goal = rng.sample(cells, 2)
        hidden = [c for c in rng.sample(cells, 25) if c not in (start, goal)]
        m = Grid(free, start=start, goal=goal, hidden=hidden)
        if not A.a_star(m, start, goal).route:
            continue
        real = real_floor(m)
        run, _ = replanning_drive(m)
        reachable = goal in real and start in real and nx.has_path(real, start, goal)
        assert (run.route[-1] == goal) == reachable, (start, goal)
        for e in run.notes["replans"]:
            assert close(e["dstar"].length, e["astar"].length) or not e["astar"].route
        done += 1
    print(f"{done} random floors with hidden cells: D* Lite = A* from scratch at every replan")


def check_fast_marching():
    """On an empty floor, fast marching's arrival times come closer to the straight line than 8-connected
    Dijkstra's, and closer still on finer cells (RO-048 §7.2)."""
    errors = []
    for k in (1, 5):
        m = finer(Grid(np.ones((21, 31), bool), start=(0, 20), goal=(0, 20)), k)
        T, D = A.fast_marching(m, m.goal)[0], A.costs_from(m, m.goal)
        far = (30 * k + k // 2, 5 * k + k // 2)                 # 30 m across and 15 m up from the goal
        line = math.dist(m.xy(far), m.xy(m.goal))
        errors.append((T[far] / line - 1, D[far] / line - 1))
    (f1, d1), (f5, d5) = errors
    assert f1 < d1 and f5 < f1 and close(d1, d5), errors
    print(f"fast marching on an empty floor: {100 * f1:.1f} % long on 1 m cells, {100 * f5:.1f} % on 0.2 m cells; "
          f"8-connected Dijkstra {100 * d1:.1f} % on both")


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
            check_cost_to_go(load_grid(png))
    check_random_floors()
    check_replanning_random()
    check_fast_marching()
