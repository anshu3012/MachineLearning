"""Plain checks of the planners, on every world in worlds/ (run: python check_planners.py)."""
import math
import tempfile
from pathlib import Path

import networkx as nx
import numpy as np
import shapely
from PIL import Image

from collision import bisection_order
from planners import path_length

FINE = 0.001  # m: the paths are re-checked with test points 1 mm apart


def assert_free(space, path, name):
    """Every straight piece of the path, re-checked with test points 1 mm apart, keeps the robot clear."""
    for a, b in zip(path, path[1:]):
        t = np.linspace(0, 1, max(2, math.ceil(math.dist(a, b) / FINE) + 1))
        xs, ys = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
        assert shapely.contains_xy(space.cfree, xs, ys).all(), f"{name}: segment {a}-{b} hits an obstacle"


def check(space, results):
    """Asserts on one run of each planner (the dict from run.run_all). Returns the planners that found no path."""
    for name, r in results.items():
        path = r["path"]
        if not path:
            continue
        assert path[0] == space.start and path[-1] == space.goal, f"{name}: path does not join start to goal"
        assert_free(space, path, name)
        assert math.isclose(r["length"], path_length(space, path)), name
    costs = [e["cost"] for e in results["RRT*"]["events"] if e["cost"] is not None]
    assert all(c1 <= c0 for c0, c1 in zip(costs, costs[1:])), "RRT* cost rose"
    assert not costs or math.isclose(costs[-1], results["RRT*"]["length"])
    missing = [name for name, r in results.items() if not r["path"]]
    if "PRM" in missing:
        return missing
    roadmap = nx.Graph()
    for p, nbrs in results["PRM"]["graph"].items():
        roadmap.add_weighted_edges_from((p, x, w) for x, w in nbrs.items())
    best = nx.shortest_path_length(roadmap, space.start, space.goal, weight="weight")  # Dijkstra, from networkx
    assert math.isclose(results["PRM"]["length"], best), "PRM route is not the shortest in its roadmap"
    return missing


def check_grid_loader():
    """A 6 x 4 grid map with 0.5 m cells and a wall: the loader must put the wall, start and goal where the pixels
    are, in the grid project's coordinates (cell centres at multiples of 0.5 m)."""
    from world import grid_to_world
    px = np.full((4, 6, 3), 255, np.uint8)
    px[0:3, 3] = 0  # a wall in column 3, rows 0-2 (the top three rows)
    px[3, 0] = (0, 255, 0)  # start: bottom-left cell
    px[0, 5] = (255, 0, 0)  # goal: top-right cell
    with tempfile.TemporaryDirectory() as tmp:
        Image.fromarray(px).save(Path(tmp) / "tiny.png")
        (Path(tmp) / "tiny.json").write_text('{"label": "Tiny", "cell_m": 0.5}')
        w = grid_to_world(Path(tmp) / "tiny.png")
    assert w["bounds"] == [-0.25, -0.25, 2.75, 1.75] and w["name"] == "Tiny"
    assert w["start"] == [0.0, 0.0] and w["goal"] == [2.5, 1.5]
    wall = shapely.union_all([shapely.box(*o) for o in w["obstacles"]])
    assert wall.bounds == (1.25, 0.25, 1.75, 1.75) and math.isclose(wall.area, 0.75)


def check_extra():
    """The planners after the first four (run_extra.py), on the worlds their sections use."""
    import random

    from shapely.geometry import LineString

    import run_extra
    from bugs import bug1, bug2, free_piece
    from planners import bridge, gaussian, kinodynamic_rrt, lazy_prm, prm
    from potential import Field
    from world import load_world
    s = load_world("small-warehouse")
    f = Field(s)
    h = 1e-6  # the gradient formula agrees with the slope of U measured over 2 micrometres
    for q in [(2.0, 5.0), (6.0, 6.5), (12.0, 8.5)]:  # under the long shelf, in the gap, in the open
        slope = [(f.u((q[0] + h, q[1])) - f.u((q[0] - h, q[1]))) / (2 * h),
                 (f.u((q[0], q[1] + h)) - f.u((q[0], q[1] - h))) / (2 * h)]
        assert np.allclose(f.grad(q), slope, rtol=1e-5, atol=1e-6), q
    for q0 in [s.start, run_extra.SECOND_START]:  # descent never climbs and never touches an obstacle
        P = f.descend(q0)
        U = f.U(P[:, 0], P[:, 1])
        assert np.isfinite(U).all() and (np.diff(U) <= 1e-9).all(), q0
        assert_free(s, [tuple(p) for p in P], f"descent from {q0}")
    stuck = f.descend(s.start)[-1]
    assert np.hypot(*f.grad(stuck)) < 1e-3 and not f.at_goal(stuck), "the start should stop in a local minimum"
    parts = f.randomized(stuck, np.random.default_rng(run_extra.SEED), run_extra.WALK_STEP)
    assert f.at_goal(parts[-1][1][-1]), "the randomized field did not reach the goal"
    assert all(shapely.contains_xy(s.cfree, P[:, 0], P[:, 1]).all() for _, P in parts)

    o = load_world("office")  # the bugs: inside the free space, at the goal, within LaValle's limits
    poly = free_piece(o)
    rings = [poly.exterior, *poly.interiors]
    mline = LineString([o.start, o.goal])
    d = math.dist(o.start, o.goal)
    crossings = [len(getattr(r.intersection(mline), "geoms", [])) for r in rings]
    for r, limit in ((bug1(o), d + 1.5 * sum(x.length for x in rings)),
                     (bug2(o), d + 0.5 * sum(n * x.length for n, x in zip(crossings, rings)))):
        assert r["reached"] and r["path"][0] == o.start and r["length"] <= limit
        assert poly.buffer(1e-6).covers(LineString(r["path"]))
        if not r["bug1"]:  # Bug 2 leaves only on the start-goal line, nearer the goal than where it hit
            for (hit, hq), (leave, lq) in zip(r["marks"][::2], r["marks"][1::2]):
                assert mline.distance(shapely.Point(lq)) < 1e-6 and math.dist(lq, o.goal) < math.dist(hq, o.goal)

    rng = random.Random(0)  # what Gaussian and bridge-test sampling keep is what they say they keep
    for _ in range(3000):
        q, ok, pair = gaussian(0.25)(s, rng)
        assert all(s.free(p) == free for p, free in pair)
        assert not ok or (s.free(q) and sum(free for _, free in pair) == 1)
        q, ok, pair = bridge(1.0)(s, rng)
        assert not ok or (len(pair) == 3 and not pair[0][1] and not pair[1][1] and s.free(q))

    full, lz = (planner(s, s.start, s.goal, n=500, seed=run_extra.SEED) for planner in (prm, lazy_prm))
    assert math.isclose(full["length"], lz["length"]) and lz["checks"] < full["checks"] / 10, "lazy PRM"
    assert_free(s, lz["path"], "lazy PRM")

    k = kinodynamic_rrt(s, (*s.start, run_extra.START_HEADING), s.goal, seed=run_extra.SEED)
    xy = np.array(k["path"])
    assert shapely.contains_xy(s.cfree, xy[:, 0], xy[:, 1]).all() and math.dist(k["path"][-1], s.goal) <= 0.5
    for m, nxt in zip(k["motions"], k["motions"][1:] + [None]):
        turn = m[-1][2] - m[0][2]  # 1 s at -1, 0 or 1 rad/s, 1 m long, and the next arc starts where it ends
        assert min(abs(turn - w) for w in (-1, 0, 1)) < 1e-9
        assert math.isclose(sum(math.dist(a[:2], b[:2]) for a, b in zip(m, m[1:])), 1.0, rel_tol=1e-9)
        assert nxt is None or nxt[0] == m[-1]


def check_local():
    """From a path to a drive (local_planner.py, the run_extra.py sections band, local, sides, refine)."""
    import run_extra
    from local_planner import (A_MAX, L_AXLE, V_WHEEL, Clearance, Person, collocation, elastic_band, grid_route,
                               init_band, replay, rest_to_rest, run_loop, stop_and_turn, wrap)
    from planners import rrt
    from potential import path_length as length
    from run import shortest_possible
    from world import load_world
    s = load_world("small-warehouse")
    clear, best = Clearance(s), shortest_possible(s)
    pts, _, _ = grid_route(s, s.start, s.goal)  # A*'s route: every cell centre on it is free, never shorter than best
    assert (clear(pts[1:-1, 0], pts[1:-1, 1]) >= 0).all() and length(pts) >= best

    r = rrt(s, s.start, s.goal, s.step, run_extra.SEED)  # the band: same ends, free, shorter than RRT's path
    hist, P = elastic_band(r["path"], lambda x, y: clear(x, y) >= run_extra.BAND_MARGIN)
    assert tuple(P[0]) == s.start and tuple(P[-1]) == s.goal and length(P) < r["length"]
    assert_free(s, [tuple(p) for p in P], "elastic band")
    for Q, lo, hi, d in hist:  # every move stays within its bounds
        assert (d >= lo - 1e-9).all() and (d <= hi + 1e-9).all()

    route, start, goal, _ = run_extra.plan(s)
    T_stop, _, st = stop_and_turn(route.pts, start[2], goal[2])
    assert math.isclose(length(st[:, 1:3]), route.length) and math.isclose(st[-1, 0], T_stop)
    P0, D0 = init_band(route, np.array(start), np.array(goal))  # the resize rule: no time step over 0.4 s
    assert (D0 <= 0.4 + 1e-9).all() and len(P0) >= 3
    person = Person(**run_extra.PERSON)
    for who in (None, person):
        cycles, drive = run_loop(s, route, start, goal, who)
        t, x, y, th, v = drive.T
        assert math.dist(drive[-1, 1:3], goal[:2]) < 0.05 and abs(wrap(th[-1] - goal[2])) < 1e-9, "did not arrive"
        assert_free(s, [tuple(p) for p in drive[:, 1:3]], "local planner's drive")
        dt = np.diff(t)[:-1]  # the last step is the turn on the spot at the goal
        w = np.diff(th)[:-1] / dt
        assert (v <= V_WHEEL + 1e-9).all() and (v >= 0).all() and (np.abs(np.diff(v)[:-1]) / dt <= A_MAX + 1e-6).all()
        assert (v[1:-1] + np.abs(w) * L_AXLE / 2 <= V_WHEEL + 1e-6).all(), "a wheel went over 0.6 m/s"
        if who:
            seen = [(math.hypot(a - who.at(b)[0], c - who.at(b)[1]) - who.radius - s.radius) for b, a, c in
                    zip(t, x, y) if who.at(b)]
            assert min(seen) > 0.1 and drive[-1, 0] > free_arrival, "the robot touched the person"
        else:
            free_arrival = drive[-1, 0]

    case, (Pw, _, cw), (Pa, _, ca) = run_extra.sides(s, gifs=False)  # the warm start overlaps, the search passes
    assert case["gap"](Pw) < 0 < 0.1 < case["gap"](Pa) and ca < cw

    col = collocation(s, route, start, goal, keep=False)
    assert col["ok"] and np.abs(col["defects"]).max() < 1e-8
    X, U = col["X"], col["U"]
    assert (X[:, 3] <= V_WHEEL + 1e-6).all() and (np.abs(U[:, 0]) <= A_MAX + 1e-9).all()
    assert (X[:, 3] + np.abs(U[:, 1]) * L_AXLE / 2 <= V_WHEEL + 1e-6).all()
    assert (clear(X[:, 0], X[:, 1]) >= 0.01 - 1e-6).all()
    _, xs = replay(start, U, col["T"])
    assert math.dist(xs[-1, :2], goal[:2]) < 0.02 and (clear(xs[:, 0], xs[:, 1]) > 0).all()
    assert rest_to_rest(best) <= col["T"] < free_arrival < T_stop


if __name__ == "__main__":
    from run import run_all  # here, not at the top: run.py imports check from this file
    from world import WORLDS, load_world
    assert bisection_order(4) == [4, 0, 2, 1, 3] and sorted(bisection_order(7)) == list(range(8))
    check_grid_loader()
    for f in sorted(WORLDS.glob("*.json")):
        space = load_world(f)
        res = run_all(space)
        assert not check(space, res), f"{space.name}: a planner found no path"
        print(f"{space.name}: ok  " + "  ".join(f"{n} {r['length']:.1f} m" for n, r in res.items()))
    check_extra()
    print("potential field, randomized field, Bug 1, Bug 2, sampling, lazy PRM, kinodynamic RRT: ok")
    check_local()
    print("elastic band, local planner, warm starts, collocation: ok")
