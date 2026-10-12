"""The control set of the lattice: every move from a state facing 0 deg (left) and from a state facing 45 deg (right),
worked out once before planning. Forward moves blue, reverse moves purple; each ends exactly on a lattice point
(grey dots, 1 m apart) with a heading that is a multiple of 45 deg. From 0 deg: 1 m straight, 45 deg turns ending at
(5, +-2), 90 deg turns ending at (5, +-5), each also in reverse: 10 moves. From 45 deg: 1.414 m straight and 45 deg
turns ending at (2, 5) and (5, 2), each also in reverse: 6 moves. Run -> control_set.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, GREY, PURPLE
from latticekit import CONTROL, move_poses
from lotdraw import FONT
from plotly.subplots import make_subplots

here = Path(__file__).parent
assert len(CONTROL[0]) == 10 and len(CONTROL[1]) == 6
assert {m["end"] for m in CONTROL[0] if m["d"] > 0} == {(1, 0), (5, 2), (5, -2), (5, 5), (5, -5)}
assert {m["end"] for m in CONTROL[1] if m["d"] > 0} == {(1, 1), (2, 5), (5, 2)}
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=["from a state facing 0 deg: 10 moves", "from a state facing 45 deg: 6 moves"])
gx, gy = np.meshgrid(np.arange(-6, 7), np.arange(-6, 7))
for col, h in ((1, 0), (2, 1)):
    fig.add_trace(go.Scatter(x=gx.ravel(), y=gy.ravel(), mode="markers", marker=dict(color="#C8C8C8", size=6),
                             hoverinfo="skip"), row=1, col=col)
    for m in CONTROL[h]:
        p = move_poses(0, 0, h, m)
        c = BLUE if m["d"] > 0 else PURPLE
        fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines", line=dict(color=c, width=3.5), hoverinfo="skip"),
                      row=1, col=col)
        x, y, th = p[-1]
        fig.add_trace(go.Scatter(x=[x, x + 0.7 * math.cos(th)], y=[y, y + 0.7 * math.sin(th)], mode="lines",
                                 line=dict(color=c, width=2), hoverinfo="skip"), row=1, col=col)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=c, size=10), hoverinfo="skip"),
                      row=1, col=col)
    th0 = h * math.pi / 4
    fig.add_trace(go.Scatter(x=[0, 0.9 * math.cos(th0)], y=[0, 0.9 * math.sin(th0)], mode="lines+markers",
                             line=dict(color="black", width=5), marker=dict(size=[11, 0], color="black"),
                             hoverinfo="skip"), row=1, col=col)
    fig.update_xaxes(range=[-6.6, 6.6], showgrid=False, zeroline=False, tickvals=[-5, 0, 5], tickfont=dict(size=15),
                     row=1, col=col)
    fig.update_yaxes(range=[-6.6, 6.6], showgrid=False, zeroline=False, tickvals=[-5, 0, 5], tickfont=dict(size=15),
                     scaleanchor="x" if col == 1 else "x2", row=1, col=col)
fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False, font=FONT,
                  title=dict(text="the control set: blue forward, purple reverse, all ending on lattice points",
                             x=0.5, xanchor="center", font_size=21), margin=dict(l=30, r=30, t=100, b=30))
for a in fig.layout.annotations:
    a.font = dict(size=18, family=FONT["family"])
fig.write_image(here / "control_set.png")
