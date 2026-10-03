"""Plotly figures for the XGBoost maths Note:
steps.png  - a straight-line fit versus a boosted-tree fit (piecewise constant) on the same data;
taylor.png - e^x and its Taylor approximations around 0;
leaf.png   - exact log loss of one leaf versus its second-order approximation, as a function of the leaf output w."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, RED, GREEN, GREY, PURPLE, ORANGE = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B", "#B279A2", "#F58518"


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# 1. line versus trees: the same noisy parabola as in the gradient boosting Notes
rng = np.random.RandomState(42)
X = rng.rand(100, 1) - 0.5
y = 3 * X[:, 0] ** 2 + 0.05 * rng.randn(100)
grid = np.linspace(-0.5, 0.5, 1000).reshape(-1, 1)
line = LinearRegression().fit(X, y).predict(grid)
trees = GradientBoostingRegressor(n_estimators=5, learning_rate=1.0, max_depth=2, random_state=42).fit(X, y).predict(grid)
fig = make_subplots(1, 2, subplot_titles=["linear regression: a smooth line", "boosted trees: flat steps and jumps"],
                    horizontal_spacing=0.07)
for col, pred in [(1, line), (2, trees)]:
    fig.add_trace(go.Scatter(x=X[:, 0], y=y, mode="markers", marker=dict(color=BLUE, size=8), name="data",
                             showlegend=(col == 1)), 1, col)
    fig.add_trace(go.Scatter(x=grid[:, 0], y=pred, mode="lines", line=dict(color=RED, width=3), name="prediction",
                             showlegend=(col == 1)), 1, col)
for a in fig.layout.annotations:
    a.font.size = 24
fig.update_xaxes(title="x")
fig.update_yaxes(title="y", col=1)
fig.update_layout(template="simple_white", width=1300, height=520, font=FONT, margin=dict(l=70, r=20, t=50, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
save(fig, "steps")

# 2. Taylor series of e^x around 0
x = np.linspace(-3, 3, 400)
fig = go.Figure(go.Scatter(x=x, y=np.exp(x), mode="lines", name="exp(x)", line=dict(color=BLUE, width=5)))
terms = [(1 + x, "1 + x", RED), (1 + x + x**2 / 2, "1 + x + x²/2", GREEN),
         (1 + x + x**2 / 2 + x**3 / 6, "1 + x + x²/2 + x³/6", PURPLE)]
for yy, name, c in terms:
    fig.add_trace(go.Scatter(x=x, y=yy, mode="lines", name=name, line=dict(color=c, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=[0], y=[1], mode="markers", marker=dict(color="black", size=11), name="a = 0"))
fig.update_xaxes(title="x", range=[-3, 3])
fig.update_yaxes(title="value", range=[-2, 12])
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=70, r=20, t=20, b=70),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"))
save(fig, "taylor")

# 3. one leaf of the classification tree: rows with y = 0, 1, 0, all at log-odds z0 = ln 1.5
yl = np.array([0, 1, 0])
z0 = np.log(1.5)
sig = lambda z: 1 / (1 + np.exp(-z))
w = np.linspace(-3, 1.5, 400)
logloss = lambda z: -(yl * np.log(sig(z)) + (1 - yl) * np.log(1 - sig(z))).sum()
exact = np.array([logloss(z0 + wi) for wi in w])
p = sig(z0)
G, H = (p - yl).sum(), 3 * p * (1 - p)
approx = logloss(z0) + G * w + 0.5 * H * w**2
w_star, w_exact = -G / H, np.log(0.5) - z0
print("G", G, "H", H, "w* (Taylor)", w_star, "w exact minimum", w_exact)
fig = go.Figure()
fig.add_trace(go.Scatter(x=w, y=exact, mode="lines", name="exact log loss", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=w, y=approx, mode="lines", name="second-order approximation",
                         line=dict(color=RED, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=[w_star], y=[logloss(z0) + G * w_star + 0.5 * H * w_star**2], mode="markers+text",
                         marker=dict(color=RED, size=12), text=[f"w* = {w_star:.2f}"], textposition="bottom center",
                         showlegend=False, textfont=dict(color=RED)))
fig.add_trace(go.Scatter(x=[w_exact], y=[logloss(z0 + w_exact)], mode="markers+text", marker=dict(color=BLUE, size=12),
                         text=[f"exact minimum {w_exact:.2f}"], textposition="top center", showlegend=False,
                         textfont=dict(color=BLUE)))
fig.update_xaxes(title="leaf output w (log-odds)")
fig.update_yaxes(title="log loss of the leaf's 3 rows", range=[1.5, 6])
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=80, r=20, t=20, b=70),
                  legend=dict(x=0.35, y=0.98, bgcolor="rgba(255,255,255,0.8)"))
save(fig, "leaf")
