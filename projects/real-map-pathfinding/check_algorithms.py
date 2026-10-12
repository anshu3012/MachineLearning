"""Checks every search on each street map in data/ against networkx (plain asserts; one line per map).

    python check_algorithms.py"""
import copy
import math
import random

import networkx as nx

from streets import DATA, load_map, to_grid
import algorithms as A                     # noqa: E402  (found through the path streets.py adds)
from run import SEARCHES, ON_GRID, closure_drive, time_runs

close = lambda a, b: math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6)


def connected(m, route, start, goal):
    """The route starts at start, ends at goal, and each step is one street (or one grid move)."""
    return route[0] == start and route[-1] == goal and all(b in m.neighbours(a) for a, b in zip(route, route[1:]))


def check_map(name):
    sm = load_map(name)
    grid = to_grid(sm)
    G = sm.G
    best = nx.shortest_path_length(G, sm.start, sm.goal, weight="length")
    r = {key: f(sm, grid) for key, f in SEARCHES}
    for key in ("dijkstra", "a_star", "bidirectional", "anytime_a_star"):
        assert close(r[key].length, best), (name, key, r[key].length, best)
    assert len(r["bfs"].route) - 1 == nx.shortest_path_length(G, sm.start, sm.goal), name
    assert r["weighted_a_star"].length <= 2.0 * best + 1e-6, name
    ida_goal = r["ida_star"].notes["goal"]
    assert close(r["ida_star"].length, nx.shortest_path_length(G, sm.start, ida_goal, weight="length")), name
    if r["multi_goal"]:
        nearest = min(nx.shortest_path_length(G, sm.start, g, weight="length") for g in sm.goals)
        assert close(r["multi_goal"].length, nearest) and r["multi_goal"].route[-1] in sm.goals, name
        each = A.a_star_each(sm, sm.start, sm.goals)       # one A* run per goal finds the same nearest goal
        assert close(each.length, nearest) and connected(sm, each.route, sm.start, each.route[-1]), name
        print(f"{name}: nearest goal {nearest:,.0f} m; one A* per goal explores {each.notes['explored']:,} streets, "
              f"multi-goal A* {r['multi_goal'].explored:,}")
    grid_best = nx.shortest_path_length(grid.to_networkx(), grid.start, grid.goal, weight="length")
    assert close(r["grid_a_star"].length, grid_best) and close(r["jps"].length, grid_best), name
    assert r["theta_star"].length <= grid_best + 1e-6, name
    theta = r["theta_star"].route
    assert theta[0] == grid.start and theta[-1] == grid.goal
    assert all(grid.line_of_sight(a, b) for a, b in zip(theta, theta[1:])), name
    for key, res in r.items():
        if res is None or key == "theta_star":
            continue
        m = grid if key in ON_GRID else sm
        end = {"multi_goal": res.route[-1], "ida_star": ida_goal}.get(key, m.goal)
        assert connected(m, res.route, m.start, end), (name, key)

    mt = copy.copy(sm)
    mt.weight = "travel_time"
    timed, _ = time_runs(mt)
    fastest = nx.shortest_path_length(G, sm.start, sm.goal, weight="travel_time")
    for key, res in timed.items():
        assert close(res.length, fastest), (name, key, res.length, fastest)
        assert connected(mt, res.route, mt.start, mt.goal), (name, key)
    counts = [res.explored for res in timed.values()]
    assert counts == sorted(counts, reverse=True), (name, counts)
    # chapter RO-06: D* Lite's repair after a closure equals networkx and A* from scratch
    run, closed = closure_drive(sm)
    e = run.notes["replans"][0]
    open_G = G.copy()
    open_G.remove_edges_from(closed)
    left = nx.shortest_path_length(open_G, e["pos"], sm.goal, weight="length")
    assert close(e["dstar"].length, left) and close(e["astar"].length, left), name
    assert run.route[-1] == sm.goal and all(open_G.has_edge(a, b) for a, b in zip(run.route[e["move"]:],
                                                                                run.route[e["move"] + 1:]))
    # the contraction hierarchy gives the fastest times, for the trip and for 200 random trips
    ch = A.contraction_hierarchy(mt)
    q = A.ch_query(ch, mt.start, mt.goal)
    assert close(q.length, fastest) and connected(mt, q.route, mt.start, mt.goal), name
    rng, nodes, taken = random.Random(0), mt.nodes(), [0, 0]
    for _ in range(200):
        s, t = rng.choice(nodes), rng.choice(nodes)
        q2, d2 = A.ch_query(ch, s, t), A.dijkstra(mt, s, t)
        assert close(q2.length, d2.length) and connected(mt, q2.route, s, t), (name, s, t)
        taken = [taken[0] + q2.visited, taken[1] + d2.visited]
    print(f"{name}: closure of {len(closed)} streets: D* Lite repair = A* from scratch = networkx, "
          f"{left:,.0f} m left; contraction hierarchy = networkx on the trip and 200 random trips, taking off "
          f"{taken[0] / 200:.1f} intersections on average against Dijkstra's {taken[1] / 200:.1f}")
    print(f"{name}: all {len([x for x in r.values() if x])} searches pass, shortest {best:,.0f} m; "
          f"grid A* = JPS = {grid_best:,.0f} m, Theta* {r['theta_star'].length:,.0f} m; "
          f"travel time {fastest:.1f} s with all 4 heuristics, explored {counts}")


if __name__ == "__main__":
    for path in sorted(DATA.glob("*.graphml.gz")):
        check_map(path.name.removesuffix(".graphml.gz"))
