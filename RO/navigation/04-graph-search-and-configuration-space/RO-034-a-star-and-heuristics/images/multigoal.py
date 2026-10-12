"""Two goals, one search: the doorway covers two whole cells, x 3.0-3.5 m (G1) and x 3.5-4.0 m (G2, the goal cell
of the other figures). Each gets an edge of 0 m to one extra vertex V, the virtual goal, drawn outside the door; A*
searches for V with h = the smaller octile distance to G1 or G2. It takes 6 cells, then V, off the open list and returns the
route through G1, 2.914 m, 0.5 m shorter than the route to G2. Run -> multigoal.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, title_at
from gifkit import GREEN, GREY, PURPLE
from searchkit import GOAL, START, dist_from, multi_goal

here = Path(__file__).parent
G1, G2 = (6, 7), GOAL
M = multi_goal({G1, G2})
assert round(M["cost"], 3) == 2.914 and M["path"][-2] == G1 and len(M["order"]) == 7
d = dist_from(START)
assert round(d[G1], 3) == 2.914 and round(d[G2], 3) == 3.414
XR, YR = (2, 10), (0, 8)
st = {c: "closed" for c in M["order"] if c != "V"}
fig = go.Figure()
room(fig, None, st, xr=XR, yr=YR, labels=False)
route(fig, M["path"][:-1])
V = (3.5, 4.55)
for c in (G1, G2):
    outline(fig, c, colour=PURPLE, width=5)
    x, y = centre(c)
    fig.add_trace(go.Scatter(x=[x, V[0]], y=[y, V[1]], mode="lines", line=dict(color=PURPLE, width=3, dash="dash")))
    fig.add_annotation(x=(x + V[0]) / 2 + (0.13 if c == G2 else -0.13), y=(y + V[1]) / 2, text="0 m",
                       showarrow=False, font=dict(size=18, color=PURPLE), bgcolor="white")
fig.add_trace(go.Scatter(x=[V[0]], y=[V[1]], mode="markers+text", text=["<b>V</b>"], textfont=dict(size=18),
                         marker=dict(size=34, color="white", line=dict(color=PURPLE, width=3))))
for c, t in ((G1, "G1"), (G2, "G2")):
    x, y = centre(c)
    fig.add_trace(go.Scatter(x=[x], y=[y - 0.12], mode="markers+text", text=[f"<b>{t}</b>"], textfont=dict(size=15),
                             marker=dict(size=34, color="white", line=dict(color="black", width=1.5))))
x, y = centre(START)
fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=["<b>S</b>"], textfont=dict(size=17),
                         marker=dict(size=26, color="white", line=dict(color="black", width=1.5))))
fig.add_annotation(x=V[0] + 0.25, y=V[1], text="V: the virtual goal", showarrow=False, xanchor="left",
                   font=dict(size=19, color=PURPLE))
axes(fig, None, XR, YR)
fig.update_yaxes(range=[-0.06, 4.8])
title_at(fig, "route to G1: 2.914 m (to G2 it would be 3.414 m); red: the 6 cells taken off the open list before V",
         1.0, size=18)
layout(fig, "two doorway cells joined to one virtual goal V", width=900, height=980,
       margin=dict(l=30, r=30, t=110, b=30))
fig.write_image(here / "multigoal.png")
