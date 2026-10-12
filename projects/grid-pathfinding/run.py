"""Run every search on one grid map, print the numbers and draw the animations.

    python run.py                          # the warehouse (maps/warehouse.png)
    python run.py --map maze               # any other map in maps/
    python run.py --map path/to/floor.png  # a PNG you drew (see grid.py for the four colours)
    python run.py --only a_star race       # just some of the pictures

Writes maps/<name>_preview.png and images/<name>/<search>.gif (+ _frames.png)."""
import argparse
import copy
import math
from pathlib import Path

import algorithms as A
import render
from grid import finer, load_grid

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


# ---------------------------------------------------------------- cost-to-go maps (chapter RO-06)
SENSE = 3.0        # the replanning robot sees every cell within 3 m of its own
FINE = 5           # fast marching runs on cells 5 times smaller


def walks(m):
    """The starts of the downhill walks: S and each blue cell."""
    return [("S", m.start)] + [(f"pad {i}", g) for i, g in enumerate(m.goals, 1)]


def replanning_drive(m):
    """The robot drives on its map, a copy of m, while the real floor also has m.hidden blocked; it sees a hidden
    cell when within SENSE metres, marks it blocked on its map and lets D* Lite repair. Returns the drive Result
    and {move: the hidden cells first seen at that move}."""
    belief = copy.copy(m)
    belief.free = m.free.copy()
    unseen, found = set(m.hidden), []      # found[k]: the hidden cells first seen before move k + 1

    def discover(pos):
        new = [c for c in sorted(unseen) if math.dist(m.xy(c), m.xy(pos)) <= SENSE]
        unseen.difference_update(new)
        found.append(new)
        for c, r in new:
            belief.free[r, c] = False
        return sorted({(c + dc, r + dr) for c, r in new for dc in (-1, 0, 1) for dr in (-1, 0, 1)})

    run = A.drive(belief, discover)
    return run, {k: new for k, new in enumerate(found) if new}


def lrta_trials(m, max_trials=1000):
    """LRTA* from S with the octile guess, trial after trial keeping what it learned, until a trial raises no
    guess. Returns the first and the last trial; the last one's notes["trial"] says how many ran."""
    h, learned = A.octile(m), {}
    first = last = A.lrta_star(m, m.start, m.goal, h, learned)
    for trial in range(2, max_trials + 1):
        last = A.lrta_star(m, m.start, m.goal, h, learned)
        if last.notes["raised"] == 0:
            break
    last.notes["trial"] = trial
    return first, last


def cost_to_go(m, out, want):
    """Chapter RO-06 on map m: the wavefront and navigation function, value iteration, D* Lite replanning (if the
    map has hidden cells), LRTA* and fast marching. Draws what want(key) asks for; returns the numbers."""
    V = A.costs_from(m, m.goal)
    arrow = {n: A.downhill(m, V, n) for n in V if n != m.goal}
    walked = [(name, A.walk_downhill(m, V, s)) for name, s in walks(m)]
    if want("wavefront"):
        render.wavefront(m, V, out / "wavefront")
    if want("downhill"):
        render.downhill(m, V, arrow, walked, out / "downhill")
    VI, record = A.value_iteration(m, m.goal)
    if want("value_iteration"):
        render.sweeps(m, record, out / "value_iteration")
    n = dict(V=V, VI=VI, record=record, walked=walked, arrow=arrow)
    if m.hidden:
        n["drive"], n["seen_at"] = replanning_drive(m)
        if want("d_star_lite"):
            render.replanning(m, n["drive"], n["seen_at"], out / "d_star_lite")
    n["lrta"] = lrta_trials(m)
    if want("lrta_star"):
        h0 = A.octile(m)
        render.lrta(m, *n["lrta"], {c: h0(c, m.goal) for c in m.nodes()}, out / "lrta_star")
    fine = finer(m, FINE)
    n["fine"], n["fmm"] = fine, A.fast_marching(fine, fine.goal)[0]
    n["fine_dijkstra"] = A.costs_from(fine, fine.goal)
    n["fine_theta"] = A.theta_star(fine, fine.start, fine.goal)
    if want("fast_marching"):
        render.fronts(fine, [("8-connected Dijkstra", n["fine_dijkstra"]), ("Fast marching", n["fmm"])], fine.start,
                      out / "fast_marching")
    return n


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
    if m.goals:                            # the nearest goal: one A* run per goal against one multi-goal run
        results["multi_goal_each"] = A.a_star_each(m, m.start, m.goals)
        if draw and (not only or "multi_goal_race" in only):
            render.race(m, [results["multi_goal_each"], results["multi_goal"]], out / "multi_goal_race", cols=2,
                        goals=True)
    heur = heuristic_runs(m)
    if draw and (not only or "heuristics" in only):
        render.race(m, list(heur.values()), out / "heuristics", cols=2)
    results.update({f"h_{k}": r for k, r in heur.items()})
    results["cost_to_go"] = cost_to_go(m, out, lambda key: draw and (not only or key in only))
    return m, results


def table(m, results):
    """The numbers for the page, one line per search."""
    best = results["dijkstra"].length
    lines = [f"Map: {m.label} ({m.name}), {len(m.nodes())} free cells, start {m.start}, goal {m.goal}",
             f"{'search':30s} {'visited':>8s} {'edges':>7s} {'route m':>8s} {'moves':>6s} {'of Dijkstra':>11s}"]
    for key, r in results.items():
        if key == "cost_to_go":
            continue
        share = f"{100 * r.length / best:.0f} %" if not key.startswith(("ida_star", "multi_goal")) else "-"
        if key == "h_zero":
            lines.append("A* with four heuristics:")
        lines.append(f"{r.name:30s} {r.visited:8d} {r.explored:7d} {r.length:8.1f} {len(r.route) - 1:6d} {share:>11s}")
    for key in ("ida_star", "multi_goal", "multi_goal_each", "anytime_a_star", "jps"):
        lines.append(f"{key}: " + ", ".join(f"{k} {v}" for k, v in results[key].notes.items() if k != "jump points"))
    lines.append(f"Manhattan guess at the start: {A.manhattan(m)(m.start, m.goal):.1f} m (shortest route {best:.1f} m)")
    return "\n".join(lines + cost_to_go_table(m, results["cost_to_go"]))


def cost_to_go_table(m, n):
    """The chapter RO-06 numbers for the page."""
    V, record = n["V"], n["record"]
    far = max(V, key=V.get)
    lines = [f"Wavefront (Dijkstra from G): {len(V)} cells numbered; S {V[m.start]:.2f} m; farthest {far} {V[far]:.2f} m",
             "Downhill walks: " + ", ".join(f"{name} {m.route_length(r):.2f} m (its number {V[r[0]]:.2f})"
                                             for name, r in n["walked"]),
             f"Value iteration: {len(record)} sweeps ({len(record) - 1} change something), "
             f"{len(record) * (len(V) - 1):,} updates against {len(V)} cells settled by Dijkstra; "
             "first values per sweep " + str([len(f) for _, f, _ in record]) +
             ", values fallen per sweep " + str([len(f) for _, _, f in record])]
    if "drive" in n:
        run = n["drive"]
        d, a = run.notes["first"]
        lines.append(f"Replanning: hidden cells {list(m.hidden)}, seen within {SENSE:g} m; drove {run.length:.2f} m in "
                     f"{len(run.route) - 1} moves; first plan: D* Lite {d.visited} cells, A* {a.visited} "
                     f"(A* from G to S: {A.a_star(m, m.goal, m.start).visited})")
        for e in run.notes["replans"]:
            lines.append(f"  move {e['move']} at {e['pos']}: saw {n['seen_at'][e['move']]}; D* Lite {e['dstar'].visited}"
                         f" cells, A* {e['astar'].visited}; number left {e['dstar'].length:.2f} m")
        real = copy.copy(m)                # the floor as it really is: the hidden cells blocked
        real.free = m.free.copy()
        for c, r in m.hidden:
            real.free[r, c] = False
        lines.append(f"  replans in all: D* Lite {sum(e['dstar'].visited for e in run.notes['replans'])}, "
                     f"A* {sum(e['astar'].visited for e in run.notes['replans'])}; shortest route with the hidden "
                     f"cells known: {A.a_star(real, m.start, m.goal).length:.2f} m")
    first, last = n["lrta"]
    cells = len({e[1] for e in first.log if e[0] == "raise"})
    lines.append(f"LRTA*: trial 1 {len(first.route) - 1} moves, {first.length:.2f} m, {first.notes['raised']} raises "
                 f"in {cells} cells; "
                 f"trial {last.notes['trial']} raises nothing: {len(last.route) - 1} moves, {last.length:.2f} m")
    fine = n["fine"]
    lines.append(f"Fast marching on {fine.cell:g} m cells ({len(n['fmm'])} free): S at {n['fmm'][fine.start]:.2f} s; "
                 f"8-connected Dijkstra {n['fine_dijkstra'][fine.start]:.2f} m; Theta* route {n['fine_theta'].length:.2f} m")
    return lines


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", default="warehouse", help="a name in maps/ or a path to a PNG")
    ap.add_argument("--only", nargs="*", help="draw only these: preview, race, heuristics, multi_goal_race, "
                                              "wavefront, downhill, value_iteration, d_star_lite, lrta_star, "
                                              "fast_marching, or keys such as a_star")
    args = ap.parse_args()
    print(table(*run(args.map, args.only)))
