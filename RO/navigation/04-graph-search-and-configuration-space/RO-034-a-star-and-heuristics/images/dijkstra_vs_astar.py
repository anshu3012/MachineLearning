"""The same search loop with three guesses h, on the room grid from the start cell S to the goal cell G under the
door, one expansion per frame in all three panels. Top: h = 0, which is Dijkstra's algorithm. Middle: A* with the
straight-line distance to G. Bottom: A* with the octile distance to G. Closed cells (taken off the open list) are
light red, open cells light green, the cell just expanded is outlined in orange. Dijkstra is done after 54 cells,
A* with the straight line after 11, A* with the octile distance after 9; all three routes are 3.414 m long.
Run -> dijkstra_vs_astar.gif, dijkstra_vs_astar_frames.png"""
from pathlib import Path

from drawkit import axes, layout, outline, room, route, sg, title_at
from gifkit import make_gif
from plotly.subplots import make_subplots
from searchkit import astar, dijkstra, straight

here = Path(__file__).parent
RUNS = [("h = 0 (Dijkstra)", dijkstra(trace=True)), ("A*, h = straight-line distance", astar(h=straight, trace=True)),
        ("A*, h = octile distance", astar(trace=True))]
assert [len(r["order"]) for _, r in RUNS] == [54, 11, 9]
assert all(round(r["cost"], 3) == 3.414 for _, r in RUNS)


def panel(fig, rc, run, k, name):
    snaps = run["snaps"]
    s = snaps[min(k, len(snaps)) - 1] if k else None
    status = {}
    if s:
        status.update({c: "open" for c in s["open"]})
        status.update({c: "closed" for c in s["closed"]})
    room(fig, rc, status, labels=False)
    if s:
        outline(fig, s["cur"], rc=rc)
    done = k >= len(snaps)
    if done:
        route(fig, run["path"], rc=rc)
    sg(fig, rc)
    n = min(k, len(snaps))
    return f"{name}: {n} cells taken off" + (f", route {run['cost']:.3f} m" if done else "")


def frame(k):
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.065)
    for i, (name, run) in enumerate(RUNS):
        t = panel(fig, (i + 1, 1), run, k, name)
        axes(fig, (i + 1, 1))
        title_at(fig, t, fig.get_subplot(i + 1, 1).yaxis.domain[1] + 0.004, size=20)
    title = "one search loop, three guesses h (S: the robot, G: under the door)" if k == 0 else \
        f"expansion {k}" + (": all three are done" if k >= len(RUNS[0][1]["snaps"]) else "")
    return layout(fig, title, width=900, height=1500, margin=dict(l=30, r=30, t=110, b=25))


# one expansion per frame while the A* runs work, then two per frame (only Dijkstra still changes)
n = len(RUNS[0][1]["snaps"])
ks = list(range(0, 12)) + list(range(13, n, 2)) + [n]
figs = [frame(k) for k in ks]
holds = [6] + [2] * (len(ks) - 2) + [24]
holds[9], holds[11] = 8, 8                         # the octile and the straight-line runs finish
make_gif(figs, here / "dijkstra_vs_astar", fps=5, holds=holds, keys=[11, len(ks) - 1], cols=2,
         width=600)
