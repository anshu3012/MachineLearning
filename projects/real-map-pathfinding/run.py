"""Run the searches on a street map and draw them in the look of the video.

    python run.py                           # Chicago (data/chicago.*), the default map
    python run.py --map chicago-west-loop   # any map made by get_map.py
    python run.py --only a_star race        # just some of the pictures

Writes data/<map>.png, images/<map>/<search>.gif (+ _frames.png) and images/<map>/explore.html, and prints the
numbers. Every search is a function from projects/grid-pathfinding/algorithms.py, run unchanged on the street map
(or on a grid made from it) through the same map interface."""
import argparse
import copy
from pathlib import Path

import render
from streets import load_map, to_grid
import algorithms as A                     # noqa: E402  (found through the path streets.py adds)

HERE = Path(__file__).resolve().parent

# The searches in the order the Notes teach them: key, function of (street map m, grid g made from it).
SEARCHES = [
    ("bfs", lambda m, g: A.bfs(m, m.start, m.goal)),
    ("dfs", lambda m, g: A.dfs(m, m.start, m.goal)),
    ("dijkstra", lambda m, g: A.dijkstra(m, m.start, m.goal)),
    ("a_star", lambda m, g: A.a_star(m, m.start, m.goal)),
    ("greedy", lambda m, g: A.greedy(m, m.start, m.goal)),
    ("ida_star", lambda m, g: A.ida_star_in_reach(m, m.start, m.goal)),
    ("bidirectional", lambda m, g: A.bidirectional(m, m.start, m.goal)),
    ("weighted_a_star", lambda m, g: A.weighted_a_star(m, m.start, m.goal, 2.0)),
    ("anytime_a_star", lambda m, g: A.anytime_a_star(m, m.start, m.goal, (2.5, 1.5, 1.0))),
    ("multi_goal", lambda m, g: A.multi_goal_a_star(m, m.start, m.goals) if m.goals else None),
    ("grid_a_star", lambda m, g: A.a_star(g, g.start, g.goal, name="Grid A*")),
    ("theta_star", lambda m, g: A.theta_star(g, g.start, g.goal)),
    ("jps", lambda m, g: A.jump_point_search(g, g.start, g.goal)),
]
ON_GRID = {"grid_a_star", "theta_star", "jps"}
RACE = ["bfs", "dfs", "dijkstra", "greedy", "a_star", "bidirectional"]
EXPLORE = ["bfs", "dfs", "dijkstra", "a_star", "greedy", "bidirectional", "weighted_a_star"]

# Travel time: A* with four heuristics, from no guess to the exact time still to go.
TIME = [("zero", "h = 0 (Dijkstra)"), ("top_speed", "Straight line ÷ top speed"), ("landmarks", "Landmarks (ALT)"),
        ("exact", "Exact time to go")]
LANDMARKS = 8


def time_runs(mt):
    """A* on the travel-time map with each heuristic. Returns {key: Result} and the landmarks used."""
    marks = A.far_apart(mt, LANDMARKS, mt.start)
    h = {"zero": A.zero(mt), "top_speed": mt.heuristic, "landmarks": A.landmarks(mt, marks),
         "exact": A.exact(mt, mt.goal)}
    return {key: A.a_star(mt, mt.start, mt.goal, h[key], name) for key, name in TIME}, marks


def minutes(seconds):
    return f"{seconds / 60:.1f} min"


def run(map_name="chicago", only=None, draw=True):
    """Run every search on the map (and the travel-time searches); draw them unless draw=False."""
    sm = load_map(map_name)
    grid = to_grid(sm)
    mt = copy.copy(sm)
    mt.weight = "travel_time"              # the same streets, costed in seconds
    want = lambda key: draw and (not only or key in only)
    out = HERE / "images" / sm.name
    out.mkdir(parents=True, exist_ok=True)
    if want("preview"):
        render.preview(sm, HERE / "data" / f"{sm.name}.png")
    results = {key: f(sm, grid) for key, f in SEARCHES}
    results = {k: r for k, r in results.items() if r is not None}
    timed, marks = time_runs(mt)
    for key, r in results.items():
        if not want(key):
            continue
        shown = sm
        if key == "ida_star" and r.notes["goal"] != sm.goal:   # IDA* only reached a nearer goal: draw that one
            shown = copy.copy(sm)
            shown.goal = r.notes["goal"]
        space = grid if key in ON_GRID else sm
        numbers = (f"{r.visited:,} cells visited  ·  route {r.length:,.0f} m" if key in ON_GRID else
                   f"{r.visited:,} visits in {r.notes['rounds']} rounds  ·  route {r.length:,.0f} m" if key == "ida_star"
                   else "")
        render.animate(shown, space, r, out / key, goals=key == "multi_goal", tree_only=key in ON_GRID,
                       numbers=numbers, what="moves" if key in ON_GRID else "explored")
    for key, r in timed.items():
        if want("time"):
            render.animate(mt, mt, r, out / f"time_{key}", numbers=f"{r.explored:,} explored  ·  route {minutes(r.length)}")
    if want("time"):
        render.race(mt, list(timed.values()), out / "time_race", cols=2, width=900, fmt=lambda r: minutes(r.length))
    if sm.goals:                           # the nearest goal: one A* run per goal against one multi-goal run
        results["multi_goal_each"] = A.a_star_each(sm, sm.start, sm.goals)
        if want("multi_goal_race"):
            render.race(sm, [results["multi_goal_each"], results["multi_goal"]], out / "multi_goal_race", cols=2,
                        width=1000, goals=True)
    if want("race"):
        render.race(sm, [results[k] for k in RACE], out / "race")
    if want("explore"):
        render.interactive(sm, [results[k] for k in EXPLORE], out / "explore.html")
    results.update({f"time_{k}": r for k, r in timed.items()})
    return sm, grid, results, marks


def table(sm, grid, results, marks):
    """The numbers for the page."""
    best, grid_best = results["dijkstra"].length, results["grid_a_star"].length
    lines = [f"Map: {sm.label} ({sm.name}): {len(sm.nodes())} intersections, {sm.G.number_of_edges()} streets; "
             f"start {sm.start} {sm.xy(sm.start)}, goal {sm.goal} {sm.xy(sm.goal)}, "
             f"straight line {sm.heuristic(sm.start, sm.goal):,.0f} m",
             f"Grid: {grid.free.shape[1]} x {grid.free.shape[0]} cells of {grid.cell:g} m, {int(grid.free.sum())} free",
             f"{'search':30s} {'explored':>9s} {'visited':>8s} {'route m':>9s} {'streets':>8s} {'share':>7s}"]
    for key, r in results.items():
        if key.startswith("time_"):
            continue
        ref = grid_best if key in ON_GRID else best
        share = "-" if key.startswith(("ida_star", "multi_goal")) else f"{100 * r.length / ref:.0f} %"
        lines.append(f"{r.name:30s} {r.explored:9,d} {r.visited:8,d} {r.length:9,.0f} {len(r.route) - 1:8d} {share:>7s}")
    lines.append(f"Travel time (top speed {sm.top_speed * 3.6:.1f} km/h, {LANDMARKS} landmarks {marks}):")
    for key, r in results.items():
        if key.startswith("time_"):
            lines.append(f"{r.name:30s} {r.explored:9,d} {r.visited:8,d} {r.length:8.1f} s = {minutes(r.length)}, "
                         f"{sm.route_length(r.route):,.0f} m")
    for key in ("ida_star", "multi_goal", "multi_goal_each", "anytime_a_star", "jps"):
        if key in results:
            notes = {k: v for k, v in results[key].notes.items() if k != "jump points"}
            lines.append(f"{key}: {notes}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", default="chicago", help="a map in data/ made by get_map.py")
    ap.add_argument("--only", nargs="*", help="draw only these: preview, race, time, explore, multi_goal_race, "
                                              "or keys such as a_star")
    args = ap.parse_args()
    print(table(*run(args.map, args.only)))
