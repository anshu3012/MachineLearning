"""Run the four planners on one world, check them, print their numbers and draw the animations.

  python run.py --world small-warehouse            a world in worlds/
  python run.py --world worlds/office.json         a world file anywhere
  python run.py --world ../grid-pathfinding/maps/maze.png   a grid map image (becomes worlds/maze.json)
Add --sweep for the 10-seed tables, --no-gifs to skip the animations. Pictures go to images/<world>/."""
import argparse
import math
import statistics
from pathlib import Path

import networkx as nx
import shapely
from shapely.geometry import LineString

from check_planners import check
from planners import prm, rrt, rrt_connect, rrt_star
from world import load_world

SEED = 2  # the seed for the single runs shown in the animations


def run_all(space, seed=SEED):
    """One seeded run of each planner on this space."""
    s, g, step = space.start, space.goal, space.step
    gamma = math.sqrt(3 * space.free_area / math.pi)  # RRT* radius constant for 2-D (Karaman and Frazzoli 2011)
    first = rrt(space, s, g, step, seed, max_samples=20000)
    return {"RRT": first,
            # RRT* draws the same samples as RRT (same seed), so it reaches the goal at the same sample; it then
            # goes on for as many samples again (at least 1,500 in all) to shorten the path
            "RRT*": rrt_star(space, s, g, step, gamma, seed, samples=max(1500, 2 * first["samples"])),
            "RRT-Connect": rrt_connect(space, s, g, step, seed, max_samples=20000),
            "PRM": prm(space, s, g, n=prm_size(space), seed=seed)}


def prm_size(space):
    """PRM samples: 3 per square metre of free space, at least 500."""
    return max(500, int(round(3 * space.free_area, -1)))


def shortest_possible(space):
    """Length of the shortest collision-free path, for reference: the shortest route in the visibility graph of the
    free space's corners (corners rounded with 2 segments per quarter circle, so it is a few mm short)."""
    zone = space.free_region.buffer(-space.radius, quad_segs=2)
    rings = [r for poly in getattr(zone, "geoms", [zone]) for r in [poly.exterior, *poly.interiors]]
    points = [space.start, space.goal] + [p for r in rings for p in r.coords[:-1]]
    if len(points) > 500:
        return None  # ponytail: O(n^2) visibility test, skipped on big maps
    inside = zone.buffer(1e-6)
    shapely.prepare(inside)
    graph = nx.Graph()
    for i, a in enumerate(points):
        for b in points[i + 1:]:
            if inside.covers(LineString([a, b])):
                graph.add_edge(a, b, weight=math.dist(a, b))
    return nx.shortest_path_length(graph, space.start, space.goal, weight="weight")


def table(results):
    rows = [f"{'planner':12} {'samples':>8} {'checks':>8} {'path (m)':>9} {'time (s)':>9}"]
    for name, r in results.items():
        length = f"{r['length']:>9.1f}" if r["path"] else "  no path"
        rows.append(f"{name:12} {r['samples']:>8,} {r['checks']:>8,} {length} {r['time']:>9.3f}")
    return "\n".join(rows)


def seed_sweep(space, seeds=range(1, 11)):
    """Median samples, checks, path and time of each planner over several seeds, and how many runs found a path
    shorter than twice the shortest possible."""
    runs = [run_all(space, seed) for seed in seeds]
    best = shortest_possible(space)
    rows = [f"{'planner':12} {'samples':>8} {'checks':>8} {'path (m)':>9} {'time (s)':>9} {'under 2x best':>14}"]
    for name in runs[0]:
        rs = [r[name] for r in runs]
        med = {k: statistics.median(r[k] for r in rs) for k in ("samples", "checks", "length", "time")}
        short = sum(r["length"] < 2 * best for r in rs)
        rows.append(f"{name:12} {med['samples']:>8,.0f} {med['checks']:>8,.0f} {med['length']:>9.1f} "
                    f"{med['time']:>9.3f} {short:>8} of {len(rs)}")
    return "\n".join(rows)


def prm_sweep(space, sizes=(250, 500, 1000, 2000), seeds=range(1, 11)):
    """PRM with more and more samples: how many seeds give a route shorter than twice the shortest possible."""
    best = shortest_possible(space)
    rows = [f"{'samples':>8} {'under 2x best':>14} {'median route (m)':>17} {'median checks':>14}"]
    for n in sizes:
        rs = [prm(space, space.start, space.goal, n=n, seed=s) for s in seeds]
        lengths = [r["length"] or math.inf for r in rs]
        rows.append(f"{n:>8} {sum(x < 2 * best for x in lengths):>8} of {len(rs)} "
                    f"{statistics.median(lengths):>17.1f} {statistics.median(r['checks'] for r in rs):>14,.0f}")
    return "\n".join(rows)


def main(world="small-warehouse", sweep=False, gifs=True):
    space = load_world(world)
    x0, y0, x1, y1 = space.bounds
    best = shortest_possible(space)
    print(f"{space.name}: {x1 - x0:g} m x {y1 - y0:g} m, robot radius {space.radius} m, free area for the robot's "
          f"centre {space.free_area:.1f} m2, step {space.step} m, edge resolution {space.eps} m")
    print(f"start {space.start}, goal {space.goal}, straight line {math.dist(space.start, space.goal):.1f} m, "
          f"shortest possible path {best:.1f} m" if best else "")
    results = run_all(space)
    results["RRT*"]["shortest"] = best
    print(f"\nseed {SEED}\n" + table(results))
    missing = check(space, results)
    print("checks passed: every path found is collision-free, starts at the start and ends at the goal; RRT* cost "
          "never rises; PRM's route is the shortest in its roadmap")
    if missing:
        print("no path within the sample budget:", ", ".join(missing))
        gifs = False  # ponytail: the animations assume a path; add a "no path" ending if you need them here
    if sweep:
        print("\nmedians over seeds 1-10\n" + seed_sweep(space))
        print("\nPRM over seeds 1-10\n" + prm_sweep(space))
    if gifs:
        import render
        render.animate_all(space, results, Path(__file__).parent / "images" / space.key)
    return space, results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--world", default="small-warehouse", help="a name in worlds/, a world .json, or a grid map .png")
    ap.add_argument("--sweep", action="store_true", help="also print the 10-seed tables")
    ap.add_argument("--no-gifs", action="store_true", help="skip the animations")
    a = ap.parse_args()
    main(a.world, a.sweep, not a.no_gifs)
