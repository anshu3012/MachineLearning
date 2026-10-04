"""Two stills for the gradient boosting classification Note (Plotly), on the eight students at stage 1 (p = 0.625):
residual_gaps.png - each student's class (0 or 1) as a dot, the predicted probability as a dashed line, and the
                    pseudo-residual y - p as the red gap between them;
leaf_newton.png   - the true log loss of a leaf against its value gamma, with the second-order Taylor parabola.
                    Leaf 2 (students 3, 4, 5): the parabola's lowest point is the leaf value 0.18.
Run: python leaf_newton.py"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
d = pd.read_csv(HERE.parent / "data" / "placement8.csv")
y = d.placed.to_numpy()
F0 = np.log(y.sum() / (1 - y).sum())
p0 = 1 / (1 + np.exp(-F0))
assert np.isclose(p0, 0.625)

# ---- residual_gaps.png ----
fig = go.Figure()
xs = np.arange(1, 9)
for x, yi in zip(xs, y):
    fig.add_trace(go.Scatter(x=[x, x], y=[p0, yi], mode="lines", line=dict(color=RED, width=5), showlegend=False))
    fig.add_annotation(x=x, y=(p0 + yi) / 2, text=f"{yi - p0:+.3f}", showarrow=False, xshift=38,
                       font=dict(size=18, color=RED))
for c, col, name in [(1, BLUE, "placed (class 1)"), (0, ORANGE, "not placed (class 0)")]:
    fig.add_trace(go.Scatter(x=xs[y == c], y=y[y == c], mode="markers", marker=dict(color=col, size=22), name=name))
fig.add_hline(y=p0, line=dict(color="black", dash="dash", width=3))
fig.add_annotation(x=8.75, y=p0, text="predicted<br>p = 0.625", showarrow=False, font_size=19, yshift=30)
fig.update_xaxes(title_text="student", tickvals=xs, range=[0.4, 9.3])
fig.update_yaxes(title_text="probability of placement", range=[-0.08, 1.08])
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, margin=dict(l=80, r=20, t=30, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(HERE / "residual_gaps.png", scale=2)
fig.write_image(HERE / "residual_gaps.pdf")


# ---- leaf_newton.png ----
def true_loss(ys, g):                                     # log loss of the leaf's students at log-odds F0 + g
    z = F0 + g[:, None]
    return (np.log1p(np.exp(-z)) + (1 - ys) * z).sum(axis=1)


def taylor(ys, g):                                        # L(0) + sum(p - y) g + 1/2 sum p(1-p) g^2
    return true_loss(ys, np.array([0.0]))[0] + (p0 - ys).sum() * g + 0.5 * len(ys) * p0 * (1 - p0) * g ** 2


ys, g = np.array([1, 0, 1]), np.linspace(-2, 2.5, 901)    # leaf 2: students 3, 4, 5
newton = (ys - p0).sum() / (len(ys) * p0 * (1 - p0))
exact = np.log(2) - F0                                    # sigma(F0 + g) = 2/3, the leaf's share of 1s
assert abs(g[true_loss(ys, g).argmin()] - exact) < 0.01 and np.isclose(newton, 0.178, atol=0.001)
fig = go.Figure()
fig.add_trace(go.Scatter(x=g, y=true_loss(ys, g), mode="lines", line=dict(color=GREY, width=4),
                         name="log loss of the leaf's students"))
fig.add_trace(go.Scatter(x=g, y=taylor(ys, g), mode="lines", line=dict(color=RED, width=3, dash="dash"),
                         name="its parabola (second-order Taylor)"))
fig.add_trace(go.Scatter(x=[newton], y=[taylor(ys, np.array([newton]))[0]], mode="markers",
                         marker=dict(color=RED, size=18), name="lowest point of the parabola"))
fig.add_annotation(x=newton, y=1.93, ax=0, ay=-90, arrowhead=2, font_size=21,
                   text="γ = Σr / Σp(1 − p) = 0.18")
fig.update_xaxes(title_text="leaf value γ (log-odds), leaf 2: students 3, 4, 5")
fig.update_yaxes(title_text="log loss", range=[1.5, 4.2])
fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, margin=dict(l=80, r=20, t=30, b=130),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.24))
fig.write_image(HERE / "leaf_newton.png", scale=2)
fig.write_image(HERE / "leaf_newton.pdf")
