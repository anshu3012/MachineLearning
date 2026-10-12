"""Jump point search on the room grid from S to G. From each cell it takes off the open list, it scans in straight
lines and diagonals without putting the cells it passes on the open list; a scan stops at a wall or obstacle (no
jump point) or at a jump point: G, or a cell next to an obstacle corner, where a route may have to turn (a forced
neighbour). One scan per frame: light orange, the cells this scan passes; grey, earlier scans; green, jump points on
the open list; red, taken off it; purple outline, a forced neighbour. JPS takes 5 cells off the open list (A*: 9) and only 7 cells ever enter it (A*: 23);
the route through the jump points is 3.414 m. Run -> jps_anim.gif, jps_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, sg, title_at
from gifkit import GREY, ORANGE, PURPLE, make_gif
from searchkit import START, astar, free, jps

here = Path(__file__).parent
J = jps()
A = astar(trace=True)
assert J["order"] == [START, (5, 3), (5, 6), (6, 7), (7, 7)] and round(J["cost"], 3) == 3.414
entered = {START} | {j["jp"] for j in J["jumps"] if j["jp"]}
assert len(entered) == 7 and len(A["snaps"][-1]["closed"]) + len(A["snaps"][-1]["open"]) == 23
NAMES = {(-1, -1): "down-left", (-1, 0): "left", (-1, 1): "up-left", (0, -1): "down", (0, 1): "up",
         (1, -1): "down-right", (1, 0): "right", (1, 1): "up-right"}


def forced(j):
    """The forced neighbours that make the end of a straight scan a jump point."""
    (x, y), (dx, dy) = j["jp"], j["d"]
    if dx and not dy:
        return [(x, y + s) for s in (1, -1) if free((x, y + s)) and not free((x - dx, y + s))]
    if dy and not dx:
        return [(x + s, y) for s in (1, -1) if free((x + s, y)) and not free((x + s, y - dy))]
    return []


def frame(upto, title, sub, final=False):
    """upto: number of scans done; the last one is the current scan."""
    fig = go.Figure()
    st = {}
    for j in J["jumps"][:upto - 1]:
        st.update({c: "pale" for c in j["steps"]})
    if upto:
        st.update({c: "seen" for c in J["jumps"][upto - 1]["steps"]})
    found = [j["jp"] for j in J["jumps"][:upto] if j["jp"]]
    cur = J["jumps"][upto - 1]["frm"] if upto else START
    closed = J["order"][:J["order"].index(cur) + 1] if not final else J["order"]
    st.update({c: "open" for c in found})
    st.update({c: "closed" for c in closed})
    room(fig, None, st, labels=False)
    if upto and not final:
        j = J["jumps"][upto - 1]
        if j["steps"]:
            (x0, y0), (x1, y1) = centre(j["frm"]), centre(j["steps"][-1])
            fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", text="",
                               showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3.5, arrowcolor=ORANGE)
        outline(fig, cur)
        if j["jp"] and j["jp"] != (7, 7):
            for c in forced(j):
                outline(fig, c, colour=PURPLE, width=5)
    if final:
        route(fig, J["path"])
    sg(fig)
    axes(fig)
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, title, width=900, height=600, margin=dict(l=30, r=30, t=110, b=30))


figs, holds = [frame(0, "jump point search: scan, do not queue", "only jump points go on the open list")], [6]
for k, j in enumerate(J["jumps"], start=1):
    name = NAMES[j["d"]]
    if j["jp"] == (7, 7):
        what = "jump point: G itself"
    elif j["jp"] and forced(j):
        what = "jump point: the purple cell past the obstacle's corner is a forced neighbour"
    elif j["jp"]:
        what = "jump point: a straight scan from it reaches a jump point"
    elif j["steps"]:
        what = f"{len(j['steps'])} step" + ("s" if len(j["steps"]) > 1 else "") + ", then blocked: nothing"
    else:
        what = "blocked at once: nothing"
    n = J["order"].index(j["frm"]) + 1
    figs.append(frame(k, f"cell {n} off the open list: scan {name}", what))
    holds.append(5 if j["jp"] else 3)
figs.append(frame(len(J["jumps"]), "G comes off the open list: route 3.414 m through the jump points",
                  "5 cells taken off the open list (A*: 9); 7 ever on it (A*: 23)", final=True))
holds.append(24)
make_gif(figs, here / "jps_anim", fps=3, holds=holds, keys=[3, 8, 10, len(figs) - 1], cols=2, width=760)
