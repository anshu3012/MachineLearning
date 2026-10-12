"""Figure 7: depth-first search on the room grid (4-connected, neighbours tried left, down, up, right). The frontier is
a stack: the newest cells sit on top and come off first. One frame per expansion. Blue: visited; orange: on the
stack, numbered from the top (1 comes off next); red outline: the cell being expanded; purple line: the path from S
to it. At a dead end (no new neighbour) the search backs up: the next cell off the stack hangs off an earlier cell.
The door's cell comes off at the 55th expansion; the route has 22 moves, 11.0 m. Run: python dfs_dive.py ->
dfs_dive.gif, dfs_dive_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from griddraw import axes, cell_box, grid_lines, grid_trace, layout, lines_below, room_lines, route, start_goal
from roomsearch import dfs, length, path_to

here = Path(__file__).parent
R = dfs()
DEAD = [k for k, s in enumerate(R["snaps"]) if s["dead"]]
assert len(R["path"]) - 1 == 22 and length(R["path"]) == 11.0 and len(R["visited"]) == 55 and len(DEAD) == 8


def frame(snap, title, lines, final=False):
    text = {c: f"<b>{i + 1}</b>" for i, c in enumerate(snap["frontier"])}
    fig = go.Figure()
    fig.add_trace(grid_trace(snap["visited"], snap["frontier"], text, size=16))
    fig.add_trace(grid_lines())
    for t in room_lines():
        fig.add_trace(t)
    start_goal(fig)
    if final:
        fig.add_trace(route(R["path"]))
    elif snap.get("cur"):
        fig.add_trace(route(path_to(snap["parent"], snap["cur"]), color=PURPLE, width=4))
        fig.add_trace(cell_box(snap["cur"], RED, 4))
    axes(fig)
    layout(fig, height=760, title=title, b=170)
    lines_below(fig, [("orange: on the stack, numbered from the top; blue: visited", ORANGE)] + lines, y0=-0.14)
    return fig


figs, holds, keys = [frame(dict(visited=[], frontier=[R["snaps"][0]["cur"]]), "start: the stack holds only S",
                           [("neighbours are tried left, down, up, right; the first one ends up on top", "black")])], [10], [0]
for k, snap in enumerate(R["snaps"][:-1]):
    nxt = R["snaps"][k + 1]["cur"]
    if snap["dead"]:
        title = f"expansion {k + 1}: dead end, back up"
        lines = [("no new neighbour here; the next cell comes off the top of the stack", RED),
                 ("it hangs off an earlier cell, so the purple path jumps back", PURPLE)]
    else:
        title = f"expansion {k + 1}: dive deeper"
        lines = [(f"purple: the path from S to the red cell, {len(path_to(snap['parent'], snap['cur'])) - 1} moves",
                  PURPLE), (f"{len(snap['frontier'])} cells on the stack", GREY)]
    figs.append(frame(snap, title, lines))
    holds.append(6 if snap["dead"] else 2)
    if k in (11, DEAD[2]):
        keys.append(len(figs) - 1)
last = R["snaps"][-1]
figs.append(frame(last, "G comes off the stack: 55 expansions",
                  [("green line: the route found, 22 moves = 11.0 m", GREEN),
                   ("breadth-first search found 8 moves = 4.0 m on the same grid", BLUE)], final=True))
holds.append(30)
keys.append(len(figs) - 1)
make_gif(figs, here / "dfs_dive.gif", fps=5, holds=holds, keys=keys, cols=2, width=900)
print("dead ends at expansions", [d + 1 for d in DEAD])
