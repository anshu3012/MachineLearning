"""Theta* on the room grid from S to G, on the part of the room it touches (x 1.0-4.5 m, y 0-4 m). It is A* with one
change: when a cell is taken off the open list, each neighbour first tries the cell's own parent as its parent, and
keeps it if the straight line between their centres crosses no blocked cell (line of sight). Grey lines join each
cell to its parent; most cells see S directly. One expansion per frame. When the cell left of G is expanded, S cannot
see G (the line crosses a table cell, red dashed), so G's parent is that cell. Last frame: the Theta* route,
2.693 + 0.500 = 3.193 m, against the grid route of A*, 3.414 m (dashed). Run -> theta_anim.gif, theta_anim_frames.png"""
import math
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, sg, title_at
from gifkit import GREY, RED, make_gif
from searchkit import GOAL, START, astar, line_of_sight, theta_star

here = Path(__file__).parent
XR, YR = (2, 9), (0, 8)
T, A = theta_star(trace=True), astar()
assert T["path"] == [START, (6, 7), GOAL] and round(T["cost"], 3) == 3.193 and len(T["order"]) == 10
assert len(T["snaps"]) == 9 and T["snaps"][-1]["cur"] == (6, 7)
assert round(math.hypot(1.0, 2.5), 3) == 2.693 and round(2.693 + 0.5, 3) == 3.193
assert not line_of_sight(START, GOAL) and line_of_sight(START, (6, 7))
assert round(T["snaps"][-1]["g"][(6, 7)], 3) == 2.693


def frame(k, final=False):
    s = T["snaps"][min(k, len(T["snaps"])) - 1] if k else dict(cur=START, closed=[], g={START: 0.0},
                                                               parent={START: START})
    fig = go.Figure()
    st = {c: "open" for c in s["g"] if c not in s["closed"]}
    st.update({c: "closed" for c in s["closed"]})
    if final:
        st[GOAL] = "closed"
    room(fig, None, st, xr=XR, yr=YR, labels=False)
    if not final:
        for c, p in s["parent"].items():
            if c != p:
                (x, y), (px, py) = centre(c), centre(p)
                fig.add_trace(go.Scatter(x=[x, px], y=[y, py], mode="lines", line=dict(color=GREY, width=2)))
        if k:
            outline(fig, s["cur"])
        if s["cur"] == (6, 7) and k:
            (x0, y0), (x1, y1) = centre(START), centre(GOAL)
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=RED, width=4, dash="dash")))
    else:
        route(fig, A["path"], colour=GREY, width=4, dash="dash")
        route(fig, T["path"])
    sg(fig, None, XR, YR)
    axes(fig, None, XR, YR)
    if final:
        t, sub = "Theta*: route 3.193 m, against A*'s 3.414 m", "blue: S to the cell left of G in one straight line, then 0.5 m"
    elif k == 0:
        t, sub = "Theta*: A* that lets a cell take its parent's parent", "grey line: each cell to its parent"
    else:
        c = s["cur"]
        t = f"cell {k} off the open list, g = {s['g'][c]:.3f} m"
        sub = ("S cannot see G: the red line crosses a table cell" if c == (6, 7) else
               "each neighbour keeps the parent's parent if it can see it")
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, t, width=900, height=1080, margin=dict(l=30, r=30, t=115, b=30))


figs = [frame(k) for k in range(len(T["snaps"]) + 1)] + [frame(len(T["snaps"]), final=True)]
holds = [5] + [4] * len(T["snaps"]) + [16]
holds[9] = 8
make_gif(figs, here / "theta_anim", fps=2, holds=holds, keys=[2, 6, 9, len(figs) - 1], cols=2, width=720)
