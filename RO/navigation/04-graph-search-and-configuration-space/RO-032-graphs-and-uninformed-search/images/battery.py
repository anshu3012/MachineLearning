"""Figure 11: a search state that breaks the Markov property. The robot's battery holds 12 moves (each 0.5 m move uses
one unit). Depth-first search with the cell alone as its state: each visited cell shows the charge left when the
search reached it; a cell reached once is never tried again. The cell x 2.0-2.5 m, y 2.0-2.5 m, two moves from S,
is first reached after a detour with only 2 units left, so the route through it is lost; after 42 expansions the
stack is empty: no route. The last frame: with (cell, charge left) as the state the same search finds a 12-move
route after 182 expansions. Run: python battery.py -> battery.gif, battery_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from griddraw import axes, cell_box, grid_lines, grid_trace, layout, lines_below, room_lines, route_cells, start_goal
from roomsearch import FREE, dfs_battery

here = Path(__file__).parent
CH = 12
A = dfs_battery(CH, full_state=False)
B = dfs_battery(CH, full_state=True)
KEY = (4, 4)                                                   # x 2.0-2.5, y 2.0-2.5: two moves from S
first = dict(A["visited"])
assert A["path"] is None and len(A["visited"]) == 42 and first[KEY] == 2
assert len(B["path"]) - 1 == 12 and len(B["visited"]) == 182 and len(FREE) * (CH + 1) == 988


def frame(visited, stack, cur, title, lines, path=None, mark=False):
    text = {c: str(b) for c, b in visited}
    fig = go.Figure()
    fig.add_trace(grid_trace([c for c, _ in visited] if not path else [], [c for c, _ in stack], text, size=16))
    fig.add_trace(grid_lines())
    for t in room_lines():
        fig.add_trace(t)
    start_goal(fig)
    if mark:
        fig.add_trace(cell_box(KEY, PURPLE, 6))
    if cur:
        fig.add_trace(cell_box(cur, RED, 4))
    for t in route_cells(path or []):
        fig.add_trace(t)
    axes(fig)
    layout(fig, height=760, title=title, b=170)
    first_line = [] if path else [("blue: visited, with the charge left on arrival (12 at S); orange: on the stack",
                                   BLUE)]
    lines_below(fig, first_line + lines, y0=-0.14)
    return fig


figs, holds, keys = [frame([], [], None, "state = cell; the battery holds 12 moves", [
    ("each 0.5 m move uses 1 unit; a cell reached with 0 units left cannot be left", GREY)])], [10], [0]
for k, s in enumerate(A["snaps"]):
    cur, b = s["cur"]
    figs.append(frame(s["visited"], s["stack"], cur, f"expansion {k + 1}: reach this cell with {b} units left",
                      [("a cell already visited is never tried again, whatever the charge", "black")],
                      mark=first.get(KEY) is not None and KEY in [c for c, _ in s["visited"]]))
    holds.append(2)
    if k == 30:
        keys.append(len(figs) - 1)
figs.append(frame(A["visited"], [], None, "stack empty after 42 expansions: no route",
                  [("purple: this cell was first reached on a detour with 2 units left", PURPLE),
                   ("from it the door is 6 moves away, so the charge runs out; the cell is never tried again with more", RED)],
                  mark=True))
holds.append(16)
keys.append(len(figs) - 1)
text_b = {}
for c, b in zip(B["path"], range(CH, -1, -1)):
    text_b[c] = str(b)
figs.append(frame([(c, int(t)) for c, t in text_b.items()], [], None,
                  "state = (cell, charge left): a 12-move route",
                  [("green outlines: the route; the number in each cell is the charge left there", GREEN),
                   ("the same cell with more charge is a new state, so it is tried again: route after 182 expansions", GREEN)], path=B["path"]))
holds.append(30)
keys.append(len(figs) - 1)
make_gif(figs, here / "battery.gif", fps=5, holds=holds, keys=keys, cols=2, width=900)
print("cell-only: expansions", len(A["visited"]), "; full state: route", len(B["path"]) - 1, "moves,",
      len(B["visited"]), "expansions")
