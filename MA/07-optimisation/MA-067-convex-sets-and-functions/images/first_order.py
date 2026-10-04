"""First-order test of convexity (Plotly). Left: softplus f(z) = ln(1 + e^z) with tangent lines at z = -2, 0, 2;
every tangent stays below the curve (convex). The tangent at 0 is ln 2 + z/2; at z = 2 it gives 1.69 < f(2) = 2.13.
Right: q(w) = w^2 (w - 1)^2 with its tangent at w = 0.5 (flat, height 0.0625); the curve drops below it near 0 and 1,
so q is not convex."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
sp = lambda z: np.log1p(np.exp(z))
sig = lambda z: 1 / (1 + np.exp(-z))
q = lambda w: w ** 2 * (w - 1) ** 2
assert abs(sp(2) - 2.1269) < 1e-3 and abs(sp(0) + 0.5 * 2 - 1.6931) < 1e-3

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("softplus ln(1 + e<sup>z</sup>): tangents below, convex",
                                    "w²(w − 1)²: tangent above the curve, not convex"))
z = np.linspace(-4, 4, 300)
fig.add_trace(go.Scatter(x=z, y=sp(z), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
for z0 in (-2, 0, 2):
    zz = np.linspace(z0 - 1.8, z0 + 1.8, 50)
    fig.add_trace(go.Scatter(x=zz, y=sp(z0) + sig(z0) * (zz - z0), mode="lines", line=dict(color=ORANGE, width=2.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[z0], y=[sp(z0)], mode="markers", marker=dict(size=10, color="black")), 1, 1)
w = np.linspace(-0.4, 1.4, 300)
fig.add_trace(go.Scatter(x=w, y=q(w), mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
fig.add_trace(go.Scatter(x=[-0.4, 1.4], y=[0.0625, 0.0625], mode="lines", line=dict(color=RED, width=2.5)), 1, 2)
fig.add_trace(go.Scatter(x=[0.5], y=[0.0625], mode="markers", marker=dict(size=10, color="black")), 1, 2)
fig.add_annotation(x=0.5, y=0.0625, text="tangent at w = 0.5", showarrow=False, yshift=16, font=dict(color=RED, size=17),
                   bgcolor="white", xref="x2", yref="y2")
fig.add_annotation(x=0, y=0, text="curve below: q(0) = 0", showarrow=False, yshift=-18, font=dict(color=BLUE, size=17),
                   bgcolor="white", xref="x2", yref="y2")
fig.update_xaxes(title_text="z", range=[-4, 4], row=1, col=1)
fig.update_yaxes(range=[-0.5, 4.2], row=1, col=1)
fig.update_xaxes(title_text="w", range=[-0.4, 1.4], row=1, col=2)
fig.update_yaxes(range=[-0.06, 0.25], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=50, b=55))
fig.write_image(here / "first_order.png", scale=2)
fig.write_image(here / "first_order.pdf")
