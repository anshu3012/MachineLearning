"""Run every search on one grid map, print the numbers and draw the animations.

    python run.py                          # the warehouse (maps/warehouse.png)
    python run.py --map maze               # any other map in maps/
    python run.py --map path/to/floor.png  # a PNG you drew (see grid.py for the four colours)
    python run.py --only a_star race       # just some of the pictures

Writes maps/<name>_preview.png and images/<name>/<search>.gif (+ _frames.png)."""
import argparse
import copy
from pathlib import Path

import algorithms as A
import render
from grid import load_grid

HERE = Path(__file__).resolve().parent

# The searches in the order the Notes teach them: key, function, how to call it.
SEARCHES = [
    ("bfs", lambda m: A.bfs(m, m.start, m.goal)),
    ("dfs", lambda m: A.dfs(m, m.start, m.goal)),
    ("dijkstra", lambda m: A.dijkstra(m, m.start, m.goal)),
    ("a_star", lambda m: A.a_star(m, m.start, m.goal)),
    ("greedy", lambda m: A.greedy(m, m.start, m.goal)),
    ("ida_star", lambda m: A.ida_star_in_reach(m, m.start, m.goal)),
    ("bidirectional", lambda m: A.bidirectional(m, m.start, m.goal)),
    ("weighted_a_star", lambda m: A.weighted_a_star(m, m.start, m.goal, 2.0)),
    ("anytime_a_star", lambda m: A.anytime_a_star(m, m.start, m.goal, (2.5, 1.5, 1.0))),
    ("theta_star", lambda m: A.theta_star(m, m.start, m.goal)),
    ("multi_goal", lambda m: A.multi_goal_a_star(m, m.start, m.goals)),
    ("jps", lambda m: A.jump_point_search(m, m.start, m.goal)),
]
RACE = ["bfs", "dfs", "dijkstra", "greedy", "a_star", "bidirectional"]

# A* with four heuristics, from no guess to the tightest one for an 8-way grid.
HEURISTICS = [("zero", "h = 0 (Dijkstra)"), ("manhattan", "Manhattan"), ("straight_line", "Straight line"),
              ("octile", "Octile")]


def heuristic_runs(m):
    return {key: A.a_star(m, m.start, m.goal, getattr(A, key)(m), name) for key, name in HEURISTICS}


def run(map_name="warehouse", only=None, draw=True):
    """Run the searches on the map; draw them unless draw=False. Returns the map and {key: Result}."""
    m = load_grid(map_name)
    out = HERE / "images" / m.name
    out.mkdir(parents=True, exist_ok=True)
    if draw and (not only or "preview" in only):
        render.preview(m, HERE / "maps" / f"{m.name}_preview.png")
    results = {key: f(m) for key, f in SEARCHES}
    for key, r in results.items():
        if not draw or (only and key not in only):
            continue
        shown = m
        if key == "ida_star" and r.notes["goal"] != m.goal:     # IDA* only reached a nearer goal: draw that one
            shown = copy.copy(m)
            shown.goal = r.notes["goal"]
        render.animate(shown, r, out / key, goals=key == "multi_goal", path=key in ("ida_star", "dfs"))
    if draw and (not only or "race" in only):
        render.race(m, [results[k] for k in RACE], out / "race")
    heur = heuristic_runs(m)
    if draw and (not only or "heuristics" in only):
        render.race(m, list(heur.values()), out / "heuristics", cols=2)
    results.update({f"h_{k}": r for k, r in heur.items()})
    return m, results


def table(m, results):
    """The numbers for the page, one line per search."""
    best = results["dijkstra"].length
    lines = [f"Map: {m.label} ({m.name}), {len(m.nodes())} free cells, start {m.start}, goal {m.goal}",
             f"{'search':30s} {'visited':>8s} {'edges':>7s} {'route m':>8s} {'moves':>6s} {'of Dijkstra':>11s}"]
    for key, r in results.items():
        share = f"{100 * r.length / best:.0f} %" if key not in ("ida_star", "multi_goal") else "-"
        if key == "h_zero":
            lines.append("A* with four heuristics:")
        lines.append(f"{r.name:30s} {r.visited:8d} {r.explored:7d} {r.length:8.1f} {len(r.route) - 1:6d} {share:>11s}")
    for key in ("ida_star", "multi_goal", "anytime_a_star", "jps"):
        lines.append(f"{key}: " + ", ".join(f"{k} {v}" for k, v in results[key].notes.items() if k != "jump points"))
    lines.append(f"Manhattan guess at the start: {A.manhattan(m)(m.start, m.goal):.1f} m (shortest route {best:.1f} m)")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", default="warehouse", help="a name in maps/ or a path to a PNG")
    ap.add_argument("--only", nargs="*", help="draw only these: preview, race, heuristics, or keys such as a_star")
    args = ap.parse_args()
    print(table(*run(args.map, args.only)))
