"""Why the meeting cell is not enough: bidirectional Dijkstra from R (x 2.0-2.5 m, y 2.0-2.5 m, two cells above
the start cell) to the goal cell G, at the moment it stops. Red: taken off the forward open list; blue: taken off
the backward one. The first cell off both lists, w (purple outline), gives 1.000 + 1.707 = 2.707 m. The cell u
just above R (orange outline), reached by both searches but taken off only the forward list, gives
0.500 + 1.914 = 2.414 m, the shortest route (blue line). Run -> bidir_trap.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, sg, title_at
from gifkit import ORANGE, PURPLE
from searchkit import GOAL, bidirectional, dist_from

here = Path(__file__).parent
R = (4, 4)
B = bidirectional(R, GOAL)
w, x = B["w"], (4, 5)
assert w == (4, 6) and round(B["gf"][w], 3) == 1.0 and round(B["gb"][w], 3) == 1.707
assert round(B["gf"][x], 3) == 0.5 and round(B["gb"][x], 3) == 1.914 and round(B["cost"], 3) == 2.414
assert round(dist_from(R)[GOAL], 3) == 2.414 and B["expanded"] == 26
assert round(1.0 + 1.707, 3) == 2.707 and round(0.5 + 1.914, 3) == 2.414
fr = B["frames"][-1]
XR, YR = (1, 11), (2, 8)
st = {c: "closed" for c in fr["closed"][0]}
st.update({c: "back" for c in fr["closed"][1] if c != w})
fig = go.Figure()
room(fig, None, st, xr=XR, yr=YR, labels=False)
best = [R, x, (5, 6), (6, 7), GOAL]
route(fig, best)
outline(fig, w, colour=PURPLE, width=6)
outline(fig, x, colour=ORANGE, width=6)
for c, txt, col, dx in ((w, "w: 1.000 + 1.707 = 2.707 m", PURPLE, -0.27), (x, "u: 0.500 + 1.914 = 2.414 m", ORANGE,
                                                                           -0.27)):
    cx, cy = centre(c)
    fig.add_annotation(x=cx + dx, y=cy, text=txt, showarrow=False, xanchor="right", font=dict(size=19, color=col),
                       bgcolor="white")
sg(fig, None, XR, YR, start=None)
cx, cy = centre(R)
fig.add_trace(go.Scatter(x=[cx], y=[cy], mode="markers+text", text=["<b>R</b>"], textfont=dict(size=17),
                         marker=dict(size=26, color="white", line=dict(color="black", width=1.5))))
axes(fig, None, XR, YR)
title_at(fig, "red: off the forward list; blue: off the backward list; w is off both", 1.0, size=19)
layout(fig, "bidirectional Dijkstra from R to G, when it stops", width=1000, height=720,
       margin=dict(l=30, r=30, t=110, b=30))
fig.write_image(here / "bidir_trap.png")
