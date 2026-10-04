"""Convex and non-convex loss functions (made-up curves): one minimum vs a local minimum and a flat stretch (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
w = np.linspace(-3, 3, 400)
convex = w ** 2
nonconvex = 0.15 * w ** 4 - 0.9 * w ** 2 + 0.35 * w + 2.2
plateau_x = np.linspace(0, 10, 400)
plateau = 3 / (1 + np.exp(-2 * (plateau_x - 7))) + 0.03 * plateau_x
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=(
    "Convex: one minimum (linear regression's MSE)", "Non-convex: local and global minimum", "A flat stretch (plateau)"))
fig.add_trace(go.Scatter(x=w, y=convex, mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
fig.add_trace(go.Scatter(x=[-2, 2.5], y=[4, 6.25], mode="lines", line=dict(color=GREY, dash="dash")), 1, 1)
fig.add_trace(go.Scatter(x=w, y=nonconvex, mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
i_loc = np.argmin(np.where(w > 0, nonconvex, 99)); i_glob = np.argmin(nonconvex)
fig.add_trace(go.Scatter(x=[w[i_loc], w[i_glob]], y=[nonconvex[i_loc], nonconvex[i_glob]], mode="markers+text",
                         text=["local minimum", "global minimum"], textposition=["top center", "bottom center"],
                         marker=dict(size=12, color=[ORANGE, GREEN]), textfont=dict(size=14)), 1, 2)
fig.add_trace(go.Scatter(x=[-1.0, 1.4], y=[np.interp(-1.0, w, nonconvex), np.interp(1.4, w, nonconvex)], mode="lines",
                         line=dict(color=RED, dash="dash")), 1, 2)
fig.add_trace(go.Scatter(x=plateau_x, y=plateau[::-1], mode="lines", line=dict(color=BLUE, width=4)), 1, 3)
fig.add_annotation(x=7.5, y=1.2, xref="x3", yref="y3", text="almost flat: tiny slope, tiny steps",
                   showarrow=False, font=dict(color=RED, size=14))
for c in (1, 2, 3):
    fig.update_xaxes(showticklabels=False, ticks="", title="parameter", row=1, col=c)
    fig.update_yaxes(showticklabels=False, ticks="", row=1, col=c)
fig.update_yaxes(title="loss", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=380, showlegend=False, font=FONT,
                  margin=dict(l=50, r=20, t=50, b=50))
fig.update_annotations(font_size=15, selector=dict(xref="paper"))
fig.write_image(here / "loss_shapes.png", scale=2)
fig.write_image(here / "loss_shapes.pdf")
