"""Figure 4: Dijkstra's algorithm on the room grid with diagonal moves (8-connected: 0.5 m straight, 0.707 m diagonal,
no cutting corners). Blue cells are settled and show their shortest distance from S in m; orange cells wait in the
priority queue and show their tentative distance. One frame each time the settled distances pass another 0.5 m, so
the blue region grows in rings of equal distance, rounder than breadth-first search's rings of equal moves. The
door's cell G is settled at 3.414 m as the 54th cell; the route, outlined in green, is 6 moves: 2 diagonals and
4 straight. Run: python dijkstra_grid.py -> dijkstra_grid.gif, dijkstra_grid_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, make_gif
from griddraw import axes, grid_lines, grid_trace, layout, lines_below, room_lines, route_cells, start_goal
from roomsearch import GOAL, START, STEPS8, dijkstra, neighbours

here = Path(__file__).parent
R = dijkstra(lambda c: neighbours(c, STEPS8), START, GOAL)
SN = R["snaps"]
assert len(R["settled"]) == 54 and round(R["cost"], 3) == 3.414 and len(R["path"]) - 1 == 6
assert max(len(s["queue"]) for s in SN) == 16


def frame(snap, title, lines, path=None):
    text = {c: f"{snap['g'][c]:.2f}" for c in snap["settled"]}
    text |= {c: f"<b>{v:.2f}</b>" for v, c in snap["queue"]}
    fig = go.Figure()
    fig.add_trace(grid_trace(snap["settled"], [c for _, c in snap["queue"]], text, size=14))
    fig.add_trace(grid_lines())
    for t in room_lines():
        fig.add_trace(t)
    start_goal(fig)
    for t in route_cells(path or []):
        fig.add_trace(t)
    axes(fig)
    layout(fig, height=760, title=title, b=170)
    lines_below(fig, [("blue: settled, with its shortest distance from S in m", BLUE),
                      ("orange: in the priority queue, with its tentative distance (bold)", ORANGE)] + lines, y0=-0.14)
    return fig


figs, holds, keys = [], [], []
for th in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    k = max(i for i, s in enumerate(SN) if s["cost"] <= th + 1e-9)
    s = SN[k]
    figs.append(frame(s, f"settled up to {th:.1f} m: {len(s['settled'])} cell" + ("s" if len(s["settled"]) > 1 else ""),
                      [(f"the queue holds {len(s['queue'])} cells; the next to settle has the smallest number", GREY)]))
    holds.append(8 if th else 10)
    if th in (1.0, 2.0):
        keys.append(len(figs) - 1)
last = SN[-1]
figs.append(frame(last, "G settled at 3.414 m: 54 cells settled",
                  [("green outlines: the route, 6 moves = 2 diagonals + 4 straight = 3.414 m", GREEN)], path=R["path"]))
holds.append(30)
keys = [0] + keys + [len(figs) - 1]
make_gif(figs, here / "dijkstra_grid.gif", fps=2, holds=holds, keys=keys, cols=2, width=900)
print("settled per frame", [len(f.data) for f in figs][:1], "route", R["path"])
