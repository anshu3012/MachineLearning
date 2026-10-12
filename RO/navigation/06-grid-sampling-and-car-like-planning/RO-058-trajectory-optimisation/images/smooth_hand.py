"""Smoothing one corner of the A* route by hand. Left: three route points p0 = (2.25, 1.25), p1 = (2.75, 1.75),
p2 = (2.75, 2.25) (grey); the middle one may move only sideways, along n = (-0.894, 0.447), at right angles to the
line through its neighbours, by at most 0.1 m each way (green); the moved point at d = 0.1 m (blue); the arrow is the
second difference p0 - 2 p1 + p2 = (-0.5, 0), which smoothing makes short. Right: the smoothing cost
|p0 - 2 p1 + p2|^2 as the move d changes: 0.25 - 1.789 d + 4 d^2, lowest at d = 0.224 m (0.05) but the bound stops
it at d = 0.1 m (0.111). Run -> smooth_hand.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, RED
from plotly.subplots import make_subplots

here = Path(__file__).parent
p0, p1, p2 = np.array([2.25, 1.25]), np.array([2.75, 1.75]), np.array([2.75, 2.25])
c = (p2 - p0) / np.hypot(*(p2 - p0))
n = np.array([-c[1], c[0]])
D2 = p0 - 2 * p1 + p2
cost = lambda d: float(np.sum((D2 - 2 * d * n) ** 2))
assert np.allclose(np.round(n, 3), [-0.894, 0.447]) and np.allclose(D2, [-0.5, 0])
assert round(cost(0.1), 3) == 0.111 and round(float(n @ D2) / 2, 3) == 0.224 and round(cost(float(n @ D2) / 2), 3) == 0.05
fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.12,
                    subplot_titles=["one corner: the middle point moves sideways", "the cost as the move d changes"])
fig.add_trace(go.Scatter(x=[p0[0], p1[0], p2[0]], y=[p0[1], p1[1], p2[1]], mode="lines+markers",
                         line=dict(color=GREY, width=3, dash="dash"), marker=dict(size=12, color=GREY)), row=1, col=1)
a, b = p1 - 0.1 * n, p1 + 0.1 * n
fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color=GREEN, width=9)), row=1, col=1)
q = p1 + 0.1 * n
fig.add_trace(go.Scatter(x=[p0[0], q[0], p2[0]], y=[p0[1], q[1], p2[1]], mode="lines+markers",
                         line=dict(color=BLUE, width=3), marker=dict(size=13, color=BLUE)), row=1, col=1)
fig.add_annotation(x=p1[0] + D2[0], y=p1[1] + D2[1], ax=p1[0], ay=p1[1], xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowwidth=3, arrowcolor=RED, text="", row=1, col=1)
for p, t, dx, dy in ((p0, "p0", 0.04, 0), (p1, "p1", 0.05, 0.07), (p2, "p2", 0.04, 0)):
    fig.add_annotation(x=p[0] + dx, y=p[1] + dy, text=t, showarrow=False, xanchor="left", font=dict(size=20),
                       row=1, col=1)
fig.add_annotation(x=q[0], y=q[1], text="moved 0.1 m", showarrow=True, ax=-70, ay=-70, arrowcolor=BLUE,
                   font=dict(size=18, color=BLUE), row=1, col=1)
fig.add_annotation(x=p1[0] - 0.42, y=p1[1] + 0.03, text="p0 − 2 p1 + p2", showarrow=False, xanchor="left",
                   yanchor="bottom", font=dict(size=18, color=RED), row=1, col=1)
fig.add_annotation(x=a[0] - 0.02, y=a[1] - 0.05, text="allowed: ±0.1 m", showarrow=False, xanchor="left",
                   yanchor="top", font=dict(size=18, color=GREEN), row=1, col=1)
fig.update_xaxes(range=[2.15, 3.05], visible=False, row=1, col=1)
fig.update_yaxes(range=[1.15, 2.35], visible=False, scaleanchor="x", row=1, col=1)
d = np.linspace(-0.15, 0.35, 200)
fig.add_shape(type="rect", x0=-0.1, x1=0.1, y0=0, y1=1, xref="x2", yref="y2 domain", fillcolor="#DDEEDD",
              line_width=0, layer="below")
fig.add_trace(go.Scatter(x=d, y=[cost(x) for x in d], mode="lines", line=dict(color=BLUE, width=4)), row=1, col=2)
for x, txt, col, ay in ((0.1, "bounded: d = 0.1 m,<br>cost 0.111", GREEN, -70), (0.224, "lowest: d = 0.224 m,<br>cost 0.05", GREY, -80)):
    fig.add_trace(go.Scatter(x=[x], y=[cost(x)], mode="markers", marker=dict(size=13, color=col)), row=1, col=2)
    fig.add_annotation(x=x, y=cost(x), text=txt, showarrow=True, ax=40, ay=ay, font=dict(size=18, color=col),
                       row=1, col=2)
fig.add_annotation(x=0, y=0.43, text="allowed moves", showarrow=False, font=dict(size=18, color=GREEN), row=1, col=2)
fig.update_xaxes(title="sideways move d (m)", range=[-0.15, 0.35], row=1, col=2)
fig.update_yaxes(title="cost (m²)", range=[0, 0.47], row=1, col=2)
fig.update_annotations(font_size=21, selector=dict(text="one corner: the middle point moves sideways"))
fig.update_annotations(font_size=21, selector=dict(text="the cost as the move d changes"))
fig.update_layout(template="simple_white", font=FONT, width=1300, height=700, showlegend=False,
                  margin=dict(l=10, r=20, t=50, b=60))
fig.write_image(here / "smooth_hand.png", scale=2)
