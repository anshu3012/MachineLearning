"""The planners after the first four: print the numbers on the page and draw the animations.

  python run_extra.py                    every section
  python run_extra.py fields bugs        some sections: fields, walks, bugs, narrow, lazy, kinodynamic, band, local,
                                         sides, refine
  python run_extra.py --no-gifs          numbers only
Each section runs on one world (the small warehouse, or the office for the bugs); pass --world to try another."""
import argparse
import copy
import math
import statistics
from collections import Counter
from pathlib import Path

import numpy as np
from shapely.geometry import LineString

import run
from bugs import bug1, bug2, free_piece
from gifkit import GREEN, RED
from local_planner import (Clearance, Person, Route, collocation, corners_only, elastic_band, grid_route, init_band,
                           replay, rest_to_rest, run_loop, solve_band, stop_and_turn, wheels)
from planners import bridge, gaussian, kinodynamic_rrt, lazy_prm, prm, rrt, uniform
from potential import Field, path_length
from world import load_world

IMAGES = Path(__file__).parent / "images"
SEED = run.SEED
SECOND_START = (18.5, 1.5)  # the potential field's second robot: the far corner of the small warehouse
WALK_STEP = 0.25  # m, the random walk's step in x and in y
SAMPLERS = {"uniform": uniform, "Gaussian": gaussian(0.25), "bridge test": bridge(1.0)}
NARROW_N, NARROW_SEED = 100, 4  # the race: 100 points each; seed 4 has the commonest outcome of seeds 1-20
START_HEADING = math.pi / 2  # the kinodynamic RRT's robot starts facing up the map (+y)


def folder(space):
    out = IMAGES / space.key
    out.mkdir(parents=True, exist_ok=True)
    return out


def shortest_from(space, start):
    s = copy.copy(space)
    s.start = tuple(start)
    return run.shortest_possible(s)


def fields(space, gifs=True):
    """Potential field: two robots roll down U; one reaches the goal, one stops in a local minimum."""
    f = Field(space)
    a, b = f.descend(SECOND_START), f.descend(space.start)
    for name, q0, P in (("second robot", SECOND_START, a), ("robot at the start", space.start, b)):
        print(f"{name} from {q0}: U = {f.u(q0):.1f} m2, {len(P) - 1} steps, {path_length(P):.1f} m, ends at "
              f"({P[-1][0]:.2f}, {P[-1][1]:.2f}), U = {f.u(P[-1]):.1f} m2, at the goal: {f.at_goal(P[-1])}, "
              f"closest to an obstacle {f.clearance(P[:, 0], P[:, 1]).min():.3f} m")
    stop = b[-1]
    d = f.clearance([stop[0]], [stop[1]])[:, 0]
    pushes = [(i, f.obstacles[i].bounds, 0.02 * (1 / di - 2) / di ** 2) for i, di in enumerate(d) if di <= 0.5]
    print(f"at the stop: pull of the goal {math.dist(stop, f.goal):.3f} (straight up), pushes within 0.5 m: " +
          ", ".join(f"obstacle {bnds} at {d[i]:.3f} m pushes {p:.3f}" for i, bnds, p in pushes) +
          f"; |gradient| {np.hypot(*f.grad(stop)):.1e}")
    xs, ys = np.meshgrid(np.arange(0.25, space.bounds[2], 0.5), np.arange(0.25, space.bounds[3], 0.5))
    starts = [p for p in zip(xs.ravel(), ys.ravel()) if space.free(p)]
    ends = [f.descend(p)[-1] for p in starts]
    stuck = sum(np.hypot(*(e - stop)) < 0.05 for e in ends)
    goal = sum(f.at_goal(e) for e in ends)
    print(f"{len(starts)} starts 0.5 m apart: {goal} reach the goal, {stuck} ({100 * stuck / len(starts):.0f} percent)"
          f" stop in the local minimum, {len(starts) - goal - stuck} elsewhere")
    if gifs:
        import render_extra
        render_extra.animate_field(space, f, [(a, GREEN, f"green: at the goal, {path_length(a):.1f} m"),
                                              (b, RED, f"red: stuck at ({stop[0]:.1f}, {stop[1]:.1f}), U = "
                                                        f"{f.u(stop):.1f} m²")], folder(space) / "field")
    return f, a, b


def walks(space, gifs=True, seeds=range(1, 21)):
    """Randomized potential field from the local minimum: one run drawn, then the medians over seeds."""
    f = Field(space)
    stuck = f.descend(space.start)[-1]
    shortest = shortest_from(space, stuck)
    print(f"local minimum ({stuck[0]:.2f}, {stuck[1]:.2f}), U = {f.u(stuck):.3f} m2; shortest path from there "
          f"{shortest:.1f} m")
    x = stuck[0]  # the nearest start to its right, at the same height, from which the robot rolls to the goal
    while x < space.bounds[2] and not (space.free((x, stuck[1])) and f.at_goal(f.descend((x, stuck[1]))[-1])):
        x += 0.05
    print(f"at y = {stuck[1]:.2f} m, the first start to the right that rolls to the goal: x = {x:.2f} m, "
          f"{x - stuck[0]:.2f} m from the local minimum")

    def runs(step, seeds):
        out = []
        for seed in seeds:
            parts = f.randomized(stuck, np.random.default_rng(seed), step)
            out.append((parts, np.vstack([P for _, P in parts])))
        return out

    for step in (WALK_STEP, 0.1):
        rs = runs(step, seeds)
        ok = [(p, P) for p, P in rs if f.at_goal(P[-1])]
        n = [sum(m == "walk" for m, _ in p) for p, _ in rs]
        lengths = [path_length(P) for _, P in ok]
        print(f"walk step {step} m, seeds {seeds.start}-{seeds.stop - 1}: {len(ok)} of {len(rs)} reached the goal "
              f"within 200 walks; walks median {statistics.median(n):g}, most {max(n)}; "
              f"{sum(m == 'backtrack' for p, _ in rs for m, _ in p)} restarts" + (
                  f"; driven median {statistics.median(lengths):,.0f} m, 10th percentile "
                  f"{np.percentile(lengths, 10):,.0f} m, 90th {np.percentile(lengths, 90):,.0f} m" if ok else ""))
    parts = runs(WALK_STEP, [SEED])[0][0]
    ws = [P for m, P in parts if m == "walk"]
    print(f"seed {SEED}: {len(ws)} walks of {', '.join(str(len(P) - 1) for P in ws)} steps, the last ending at "
          f"({ws[-1][-1][0]:.2f}, {ws[-1][-1][1]:.2f}); {path_length(np.vstack([P for _, P in parts])):,.0f} m driven")
    if gifs:
        import render_extra
        render_extra.animate_random_walks(space, f, parts, folder(space) / "random_walk", shortest)


def bugs(space, gifs=True):
    """Bug 1 and Bug 2: lengths of every leg, the marks, and LaValle's limits."""
    shortest = run.shortest_possible(space)
    poly = free_piece(space)
    mline = LineString([space.start, space.goal])
    d = math.dist(space.start, space.goal)
    rings = [poly.exterior, *poly.interiors]
    crossings = [len(getattr(r.intersection(mline), "geoms", [r.intersection(mline)])) if r.intersects(mline) else 0
                 for r in rings]
    print(f"{space.name}: start {space.start}, goal {space.goal}, {d:.3f} m apart; shortest path {shortest:.1f} m; "
          f"edges round the obstacles {', '.join(f'{r.length:.3f}' for r in rings)} m, crossing the start-goal "
          f"line {crossings} times")
    limits = {"Bug 1": d + 1.5 * sum(r.length for r in rings),
              "Bug 2": d + 0.5 * sum(n * r.length for n, r in zip(crossings, rings))}
    out = {}
    for name, f in (("Bug 1", bug1), ("Bug 2", bug2)):
        r = out[name] = f(space)
        print(f"{name}: {r['length']:.3f} m (limit {limits[name]:.3f} m), reached {r['reached']}; legs " +
              ", ".join(f"{k} {sum(math.dist(a, b) for a, b in zip(p, p[1:])):.3f}" for k, p in r["legs"]) +
              "; marks " + ", ".join(f"{lab} ({q[0]:.2f}, {q[1]:.2f}) {math.dist(q, space.goal):.3f} m from the goal"
                                     for lab, q in r["marks"]))
    if gifs:
        import render_extra
        for name, r in out.items():
            render_extra.animate_bug(space, r, folder(space) / name.lower().replace(" ", ""), name, shortest)
    return out, limits


def narrow(space, gifs=True, seeds=range(1, 21)):
    """Narrow passage: uniform, Gaussian and bridge-test sampling, 100 points each, and uniform with 1,000."""
    best = run.shortest_possible(space)
    runs_ = {f"{name}, {n:,}": (draw, n) for name, draw, n in
             [(k, v, NARROW_N) for k, v in SAMPLERS.items()] + [("uniform", uniform, 1000)]}
    print(f"{'sampling':18} {'through the gap':>16} {'route found':>12} {'median draws':>13} {'median checks':>14}")
    through = {}
    for name, (draw, n) in runs_.items():
        rs = [prm(space, space.start, space.goal, n=n, seed=s, draw=draw) for s in seeds]
        through[name] = [(r["length"] or math.inf) < 2 * best for r in rs]
        gap = sum(through[name])
        print(f"{name:18} {gap:>10} of {len(rs)} {sum(r['path'] is not None for r in rs):>6} of {len(rs)} "
              f"{statistics.median(r['samples'] for r in rs):>13,.0f} "
              f"{statistics.median(r['checks'] for r in rs):>14,.0f}")
    outcomes = Counter(zip(*list(through.values())[:3]))  # the three ways with 100 points: through the gap or not
    (common, count), = outcomes.most_common(1)
    print(f"commonest outcome with 100 points ({', '.join(f'{k}: {gap}' for k, gap in zip(through, common))}): "
          f"{count} of {len(seeds)} seeds: "
          f"{', '.join(str(s) for s, *o in zip(seeds, *list(through.values())[:3]) if tuple(o) == common)}")
    race = {name: prm(space, space.start, space.goal, n=n, seed=NARROW_SEED, draw=draw)
            for name, (draw, n) in runs_.items()}
    print(f"seed {NARROW_SEED}: " + ", ".join(f"{k} {r['length']:.1f} m, {r['samples']:,} draws, {r['checks']:,} checks"
                                             for k, r in race.items()))
    if gifs:
        import render
        render.animate_race(space, race, folder(space) / "narrow", "blue dots: points kept · light blue: roadmap · "
                            "green: route · one shelf has the 0.8 m gap")
    return race


def lazy(space, gifs=True, seeds=range(1, 11)):
    """Lazy PRM against PRM on the same points: same route, far fewer checks."""
    n = run.prm_size(space)
    full, lz = prm(space, space.start, space.goal, n=n, seed=SEED), lazy_prm(space, space.start, space.goal, n=n,
                                                                             seed=SEED)
    edges = len(next(e["edges"] for e in lz["events"] if e["phase"] == "connect"))
    print(f"seed {SEED}, {n} points: PRM {full['checks']:,} checks, route {full['length']:.1f} m; lazy PRM "
          f"{lz['checks']:,} checks ({100 * lz['checks'] / full['checks']:.1f} percent), route {lz['length']:.1f} m, "
          f"{lz['searches']} searches, {lz['edge_checks']} edges checked of {edges:,}, "
          f"{sum(not ok for e in lz['events'] if e['phase'] == 'search' for _, ok in e['checked'])} collided")
    pairs = [(prm(space, space.start, space.goal, n=n, seed=s), lazy_prm(space, space.start, space.goal, n=n, seed=s))
             for s in seeds]
    print(f"seeds {seeds.start}-{seeds.stop - 1}: same route every time: "
          f"{all(math.isclose(a['length'], b['length']) for a, b in pairs)}; median checks PRM "
          f"{statistics.median(a['checks'] for a, _ in pairs):,.0f}, lazy PRM "
          f"{statistics.median(b['checks'] for _, b in pairs):,.0f}; median searches "
          f"{statistics.median(b['searches'] for _, b in pairs):g}")
    if gifs:
        import render_extra
        render_extra.animate_lazy(space, lz, folder(space) / "lazy_prm", full["checks"])
    return full, lz


def kinodynamic(space, gifs=True, seeds=range(1, 21)):
    """Kinodynamic RRT: drivable arcs of 1 m at 1 m/s, turning at -1, 0 or 1 rad/s."""
    start = (*space.start, START_HEADING)
    r = kinodynamic_rrt(space, start, space.goal, seed=SEED)
    straight = rrt(space, space.start, space.goal, space.step, SEED)
    turns = [abs((b[2] - a[2] + math.pi) % (2 * math.pi) - math.pi) for a, b in zip(r["poses"], r["poses"][1:])]
    print(f"seed {SEED}: {r['samples']:,} rounds, {sum(not e['ok'] for e in r['events']):,} thrown away, "
          f"{r['nodes']:,} nodes, path {r['length']:.1f} m in {len(r['motions'])} arcs "
          f"({sum(t > 0.5 for t in turns)} turning), {r['checks']:,} checks, {r['time']:.2f} s; "
          f"ends {math.dist(r['path'][-1], space.goal):.2f} m from the goal")
    corners = [abs(math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(b[1] - a[1], b[0] - a[0])))
               for a, b, c in zip(straight["path"], straight["path"][1:], straight["path"][2:])]
    corners = [min(t, 360 - t) for t in corners]
    print(f"RRT, seed {SEED}: path {straight['length']:.1f} m, {sum(t > 1 for t in corners)} corners, sharpest "
          f"{max(corners):.0f} degrees")
    rs = [kinodynamic_rrt(space, (*space.start, START_HEADING), space.goal, seed=s) for s in seeds]
    ok = [x for x in rs if x["path"]]
    print(f"seeds {seeds.start}-{seeds.stop - 1}: {len(ok)} of {len(rs)} reached the goal within 20,000 rounds; "
          f"median {statistics.median(x['samples'] for x in ok):,.0f} rounds, "
          f"{statistics.median(x['nodes'] for x in ok):,.0f} nodes, "
          f"path {statistics.median(x['length'] for x in ok):.1f} m, "
          f"{sum(x['length'] < 2 * run.shortest_possible(space) for x in ok)} through the gap")
    if gifs:
        import render_extra
        render_extra.animate_kinodynamic(space, r, folder(space) / "kinodynamic_rrt")
    return r


# ----------------------------------------------------------------------------------------------- from a path to a drive
BAND_MARGIN = 0.05  # m: the elastic band keeps the robot this far from every shelf
PERSON = dict(p0=(3.5, 9.9), p1=(4.3, 9.25), t0=15.8)  # steps out beside the end of the upper-left shelf, 1 m/s
SIDES_T, SIDES_PERSON = 16.8, (4.6, 8.8, 0.2)  # the cycle solved from two first guesses, and where the person stands
DRIVE_CROP = (0, 0, 8.5, 12.5)  # the part of the small warehouse the drives use


def plan(space):
    """The global plan: A* (the grid project's own) on 0.25 m cells, its straight runs merged. The robot starts at
    rest facing up the map and must stop at the goal facing along the plan's last piece."""
    pts, length, visited = grid_route(space, space.start, space.goal)
    route = Route(corners_only(pts))
    return route, (*space.start, START_HEADING), (*space.goal, route.point(route.length)[1]), visited


def tightest_radius(P):
    """The radius of the tightest turn of a polyline of short pieces: piece length over the change of heading."""
    d = np.diff(np.asarray(P), axis=0)
    th = np.arctan2(d[:, 1], d[:, 0])
    return min(((la + lb) / 2) / max(1e-12, abs((b - a + math.pi) % (2 * math.pi) - math.pi))
               for a, b, la, lb in zip(th, th[1:], np.hypot(*d.T), np.hypot(*d[1:].T)))


def band(space, gifs=True):
    """The elastic band smoothing RRT's path (seed 2)."""
    r = rrt(space, space.start, space.goal, space.step, SEED)
    clear = Clearance(space)
    hist, P = elastic_band(r["path"], lambda x, y: clear(x, y) >= BAND_MARGIN)
    best = run.shortest_possible(space)
    gaps = clear(P[:, 0], P[:, 1])
    print(f"RRT seed {SEED}: {r['length']:.1f} m, {len(r['path'])} points; band: {len(hist)} solves, {len(P)} points, "
          f"{path_length(P):.2f} m, tightest turn a circle of radius {tightest_radius(P):.2f} m, closest to a shelf "
          f"{gaps.min():.3f} m; shortest possible {best:.1f} m")
    print("length after each solve: " + ", ".join(f"{path_length(Q):.2f}" for Q, *_ in hist[1:]) +
          f", {path_length(P):.2f} m")
    h0, P0 = elastic_band(r["path"], lambda x, y: clear(x, y) >= BAND_MARGIN, w_len=0)
    print(f"second differences only (no length term): {len(h0)} solves, {path_length(P0):.2f} m, tightest turn a "
          f"circle of radius {tightest_radius(P0):.2f} m, lowest point y = {P0[:, 1].min():.2f} m (with the length "
          f"term {P[:, 1].min():.2f} m)")
    if gifs:
        import render_local
        render_local.animate_band(space, r["path"], hist, P, folder(space) / "elastic_band", best)
    return r, hist, P


def local(space, gifs=True):
    """The local planner on a receding horizon, without and with the person stepping out."""
    import time
    route, start, goal, visited = plan(space)
    print(f"global plan: A* on 0.25 m cells, {visited} cells expanded, {route.length:.2f} m, {len(route.pts)} points "
          f"where it turns; start {start[:2]} facing {math.degrees(start[2]):.0f} deg, goal {goal[:2]} facing "
          f"{math.degrees(goal[2]):.0f} deg")
    clear = Clearance(space)
    person = Person(**PERSON)
    t0 = time.perf_counter()
    free, free_drive = run_loop(space, route, start, goal)
    cyc, drive = run_loop(space, route, start, goal, person)
    per_cycle = (time.perf_counter() - t0) / (len(free) + len(cyc))
    for name, cs, dr in (("nobody", free, free_drive), ("person", cyc, drive)):
        print(f"{name:6}: arrived at {dr[-1, 0]:.2f} s after {len(cs)} cycles, drove {path_length(dr[:, 1:3]):.2f} m, "
              f"closest to a shelf {clear(dr[:, 1], dr[:, 2]).min():.3f} m, top speed {dr[:, 4].max():.3f} m/s, "
              f"band {min(len(c['P']) for c in cs)} to {max(len(c['P']) for c in cs)} poses")
    near = [(t, math.hypot(x - person.at(t)[0], y - person.at(t)[1]) - person.radius - space.radius)
            for t, x, y, *_ in drive if person.at(t)]
    t_close, g_close = min(near, key=lambda q: q[1])
    seen = next(c for c in cyc if c["persons"])
    t_stand = person.t0 + np.hypot(*(person.p1 - person.p0)) / person.speed
    at = drive[np.searchsorted(drive[:, 0], t_stand), 1:3]
    passing = drive[(drive[:, 0] > person.t0) & (drive[:, 0] < t_close), 4]
    print(f"person: steps out at {person.t0} s at {tuple(map(float, person.p0))}, first seen in the cycle at "
          f"{seen['t']:.1f} s, stands at {tuple(map(float, person.p1))} from {t_stand:.2f} s, when the robot's edge is "
          f"{math.hypot(*(at - person.p1)) - person.radius - space.radius:.2f} m from them; closest {g_close:.3f} m at "
          f"{t_close:.2f} s; slowest {passing.min():.2f} m/s while passing; {per_cycle * 1000:.0f} ms of computing "
          f"per cycle")
    if gifs:
        import render_local
        render_local.animate_loop(space, route.pts, cyc, drive, person, free_drive, folder(space) / "local_planner",
                                  DRIVE_CROP)
    return free, free_drive, cyc, drive


def sides(space, gifs=True):
    """One cycle with the person moved into the band's way: solved from last cycle's band and from A*'s route."""
    route, start, goal, _ = plan(space)
    clear = Clearance(space)
    cycles, _ = run_loop(space, route, start, goal)
    c = next(c for c in cycles if abs(c["t"] - SIDES_T) < 1e-6)
    persons = [SIDES_PERSON]
    (Pw, Dw), hw, ha = c["warm"], [], []
    Pw1, Dw1, cw = solve_band(Pw.copy(), Dw.copy(), c["v"], c["final"], clear, persons, hw)
    x, y = c["x"][:2]
    window = (x - 2.5, y - 2.5, x + 2.5, y + 2.5)  # the local costmap: 5 m square round the robot
    rt, length, expanded = grid_route(space, c["x"], c["goal"], cell=0.1, persons=persons, window=window)
    Pa, Da = init_band(Route(rt), c["x"], c["goal"])
    Pa1, Da1, ca = solve_band(Pa, Da, c["v"], c["final"], clear, persons, ha)

    def gap(P):  # closest the robot's disk comes to anything, at the poses and halfway between them
        mid = (P[1:, :2] + P[:-1, :2]) / 2
        return float(clear(np.r_[P[:, 0], mid[:, 0]], np.r_[P[:, 1], mid[:, 1]], persons).min())

    px, py, pr = SIDES_PERSON
    side = lambda P: "above" if np.interp(px, *P[np.argsort(P[:, 0]), :2].T) > py else "below"
    print(f"cycle at {c['t']:.1f} s: robot at ({x:.2f}, {y:.2f}), {math.hypot(x - px, y - py) - pr - space.radius:.2f}"
          f" m from the person at ({px}, {py}); the shelf above them leaves a {9.5 - (py + pr):.2f} m gap, the one "
          f"below {(py - pr) - 7.5:.2f} m; local goal ({c['goal'][0]:.2f}, {c['goal'][1]:.2f})")
    print(f"warm start: runs {side(Pw)} the person, overlap {-gap(Pw):.3f} m; solved: {side(Pw1)}, {len(Pw1)} poses, "
          f"{Dw1.sum():.2f} s, gap {gap(Pw1):.3f} m, cost {cw:.2f}")
    print(f"A* on 0.1 m cells: {expanded} cells expanded, {length:.2f} m, {side(rt)} the person; solved: "
          f"{side(Pa1)}, {len(Pa1)} poses, {Da1.sum():.2f} s, gap {gap(Pa1):.3f} m, cost {ca:.2f}")
    case = dict(hist_warm=hw, hist_search=ha, person=SIDES_PERSON, route=rt, warm=(Pw, Dw), gap=gap)
    if gifs:
        import render_local
        render_local.animate_sides(space, case, folder(space) / "warm_start_sides", (x - 2.0, y - 1.15, x + 1.0,
                                                                                    y + 1.05))
    return case, (Pw1, Dw1, cw), (Pa1, Da1, ca)


def refine(space, gifs=True):
    """One collocation solve for the whole drive, from A*'s route, against stop-and-turn along the same route."""
    route, start, goal, _ = plan(space)
    clear = Clearance(space)
    T_stop, pieces, stop_states = stop_and_turn(route.pts, start[2], goal[2])
    import time
    t0 = time.perf_counter()
    r = collocation(space, route, start, goal)
    took = time.perf_counter() - t0
    ts, xs = replay(start, r["U"], r["T"])
    best = run.shortest_possible(space)
    wr, wl = wheels(r["X"][:, 3], r["U"][:, 1])
    gaps = clear(r["X"][:, 0], r["X"][:, 1])
    print(f"stop-and-turn along A*'s route ({route.length:.2f} m, {len(route.pts) - 2} corners): {T_stop:.2f} s "
          f"({sum(t for k, t in pieces if k == 'drive'):.2f} s driving, {sum(t for k, t in pieces if k == 'turn'):.2f}"
          f" s turning)")
    print(f"collocation, {len(r['U']) - 1} intervals: {r['T']:.2f} s, {r['nit']} SLSQP iterations, {took:.1f} s, "
          f"{r['msg']}; largest defect {np.abs(r['defects']).max():.1e}; at the knots: top wheel "
          f"{max(wr.max(), wl.max()):.3f} m/s, acceleration {r['U'][:, 0].min():.2f} to {r['U'][:, 0].max():.2f}, "
          f"{np.sum(gaps < 0.0101)} knots {gaps.min():.4f} m from a shelf")
    print(f"replayed in small steps: ends {math.hypot(*(xs[-1, :2] - goal[:2])):.4f} m from the goal, top speed "
          f"{xs[:, 3].max():.4f} m/s, closest to a shelf {clear(xs[:, 0], xs[:, 1]).min():.4f} m, drove "
          f"{path_length(xs[:, :2]):.2f} m")
    print(f"no drive can beat {rest_to_rest(best):.2f} s: the shortest path, {best:.2f} m, driven straight from rest "
          f"to rest")
    if gifs:
        import render_local
        render_local.animate_refine(space, route.pts, r, np.column_stack([ts, xs]), stop_states,
                                    folder(space) / "refine_once", DRIVE_CROP)
    return r, T_stop


SECTIONS = {"fields": fields, "walks": walks, "bugs": bugs, "narrow": narrow, "lazy": lazy, "kinodynamic": kinodynamic,
            "band": band, "local": local, "sides": sides, "refine": refine}
WORLDS = {"bugs": "office"}  # every other section: the small warehouse

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*", default=list(SECTIONS), help=", ".join(SECTIONS))
    ap.add_argument("--world", help="run every chosen section on this world instead")
    ap.add_argument("--no-gifs", action="store_true")
    a = ap.parse_args()
    for name in a.sections:
        print(f"\n== {name}")
        SECTIONS[name](load_world(a.world or WORLDS.get(name, "small-warehouse")), not a.no_gifs)
