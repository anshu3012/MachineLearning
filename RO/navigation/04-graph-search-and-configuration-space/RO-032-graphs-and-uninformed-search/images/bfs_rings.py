"""Figure 6: breadth-first search on the room grid (4-connected, 0.5 m moves), ring by ring. A blue cell is visited
and shows how many moves it is from S; an orange cell waits in the queue and shows its place in the queue. Each frame
is the moment the last cell of one ring has been expanded: then the queue holds exactly the next ring. The door's
cell G comes off the queue at the 57th expansion; the route read back along the parents has 8 moves, 4.0 m.
Run: python bfs_rings.py -> bfs_rings.gif, bfs_rings_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, make_gif
from griddraw import axes, cell_box, grid_lines, grid_trace, layout, lines_below, room_lines, route_cells, start_goal
from roomsearch import GOAL, START, bfs, length

here = Path(__file__).parent
R = bfs()
FULL = bfs(goal=None)
RING = {START: 0}
for c in FULL["visited"]:
    p = FULL["parent"][c]
    if p is not None:
        RING[c] = RING[p] + 1
SIZES = [sum(v == k for v in RING.values()) for k in range(max(RING.values()) + 1)]
assert len(R["path"]) - 1 == 8 and length(R["path"]) == 4.0 and len(R["visited"]) == 57
assert len(FULL["visited"]) == 76 and SIZES[:9] == [1, 4, 7, 9, 10, 9, 7, 6, 5] and len(SIZES) == 19


def frame(snap, title, lines, path=None):
    text = {c: str(RING[c]) for c in snap["visited"]}
    text |= {c: f"<b>{i + 1}</b>" for i, c in enumerate(snap["frontier"])}
    fig = go.Figure()
    fig.add_trace(grid_trace(snap["visited"], snap["frontier"], text, size=16))
    fig.add_trace(grid_lines())
    for t in room_lines():
        fig.add_trace(t)
    start_goal(fig)
    for t in route_cells(path or []):
        fig.add_trace(t)
    axes(fig)
    layout(fig, height=760, title=title, b=170)
    lines_below(fig, [("blue: visited; its number = moves from S", BLUE),
                      ("orange: waiting in the queue; its number = its place in the queue", ORANGE)] + lines, y0=-0.14)
    return fig


figs, holds, keys = [], [], []
figs.append(frame(dict(visited=[], frontier=[START]), "start: the queue holds only S",
                  [("each expansion takes the front cell off and adds its new neighbours at the back", "black")]))
holds.append(10)
done = 0
for k in range(8):
    done += SIZES[k]
    snap = R["snaps"][done - 1]
    assert sorted(snap["frontier"]) == sorted(c for c, v in RING.items() if v == k + 1)
    figs.append(frame(snap, f"ring {k} done: the queue holds ring {k + 1}",
                      [(f"{done} cells visited; the queue holds all {SIZES[k + 1]} cells {k + 1} moves from S", GREY)]))
    holds.append(6)
    if k in (1, 4):
        keys.append(len(figs) - 1)
last = R["snaps"][-1]
figs.append(frame(last, "G comes off the queue: 57 expansions",
                  [("green outlines: the route read back along the parents, 8 moves of 0.5 m = 4.0 m", GREEN)], path=R["path"]))
holds.append(30)
keys = [0] + keys + [len(figs) - 1]
make_gif(figs, here / "bfs_rings.gif", fps=2, holds=holds, keys=keys, cols=2, width=900)
print("ring sizes", SIZES, "route", R["path"])
