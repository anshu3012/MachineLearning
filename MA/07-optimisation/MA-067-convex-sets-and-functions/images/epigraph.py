"""The epigraph: the region on and above a graph (Plotly). Left: w^2; its epigraph is a convex set: the segment
between (-1, 1) and (2, 4) stays in the shaded region. Right: q(w) = w^2 (w - 1)^2; the segment between (0, 0) and
(1, 0) leaves the shaded region under the hump (q(0.5) = 0.0625 > 0), so the epigraph is not convex.
Run: python epigraph.py -> epigraph.png, epigraph.pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, GREEN, RED = "#4C78A8", "#54A24B", "#E45756"
q = lambda w: w ** 2 * (w - 1) ** 2
assert abs(q(0.5) - 0.0625) < 1e-12

fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=(
    "w²: region above is convex", "w²(w − 1)²: region above is not convex"))
for c, (f, lo, hi, top, a, b) in enumerate([(lambda w: w ** 2, -2.2, 2.6, 7, (-1, 1), (2, 4)),
                                            (q, -0.35, 1.35, 0.2, (0, 0), (1, 0))], start=1):
    w = np.linspace(lo, hi, 300)
    y = np.minimum(f(w), top)
    fig.add_trace(go.Scatter(x=np.r_[w, w[::-1]], y=np.r_[y, np.full_like(w, top)], fill="toself", mode="none",
                             fillcolor="rgba(76,120,168,0.30)"), 1, c)
    fig.add_trace(go.Scatter(x=w, y=y, mode="lines", line=dict(color=BLUE, width=4)), 1, c)
    if c == 1:
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color=GREEN, width=5)), 1, c)
    else:
        for x0, x1, col, dash in [(0, 0.0, GREEN, "solid"), (0.0, 1.0, RED, "dash")]:
            fig.add_trace(go.Scatter(x=[x0, x1], y=[0, 0], mode="lines", line=dict(color=col, width=5, dash=dash)), 1, c)
        fig.add_annotation(x=0.5, y=0.0625, ax=0.5, ay=0.0, axref="x2", ayref="y2", xref="x2", yref="y2",
                           showarrow=True, arrowhead=0, arrowcolor=RED, arrowwidth=2)
        fig.add_annotation(x=0.5, y=-0.018, text="segment under the hump: outside", showarrow=False,
                           font=dict(color=RED, size=20), xref="x2", yref="y2")
    fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="markers", marker=dict(color="black", size=13)), 1, c)
fig.update_xaxes(title_text="w", range=[-2.2, 2.6], row=1, col=1)
fig.update_yaxes(range=[-0.3, 7], row=1, col=1)
fig.update_xaxes(title_text="w", range=[-0.35, 1.35], row=1, col=2)
fig.update_yaxes(range=[-0.035, 0.2], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=55, b=55))
fig.update_annotations(font_size=22)
fig.write_image(HERE / "epigraph.png", scale=2)
fig.write_image(HERE / "epigraph.pdf")
