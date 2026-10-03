"""Gradient boosting on the noisy quadratic data (Plotly):
stages.png         - the ensemble after 0, 1, 2, 3, 10 and 50 trees (learning rate 1, 8 leaves per tree);
learning_rate.png  - training and test MSE after each added tree, for three learning rates."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import GRID, X, X_test, boost, mse, predict, y, y_test  # noqa: E402

FONT = dict(family="Latin Modern Roman", size=19)
BLUE, RED, GREEN = "#4C78A8", "#E45756", "#54A24B"

f0, trees = boost(50, 1.0, 8)
counts = [0, 1, 2, 3, 10, 50]
titles = [f"{m} tree{'s' * (m != 1)}: train MSE {mse(y, predict(f0, trees[:m], 1.0, X)):.4f}, "
          f"test {mse(y_test, predict(f0, trees[:m], 1.0, X_test)):.4f}" for m in counts]
fig = make_subplots(2, 3, subplot_titles=titles, horizontal_spacing=0.05, vertical_spacing=0.13)
for i, m in enumerate(counts):
    r, c = i // 3 + 1, i % 3 + 1
    fig.add_trace(go.Scatter(x=X[:, 0], y=y, mode="markers", marker=dict(color=BLUE, size=6), name="training data",
                             showlegend=i == 0), r, c)
    fig.add_trace(go.Scatter(x=GRID[:, 0], y=predict(f0, trees[:m], 1.0, GRID), mode="lines", name="ensemble",
                             line=dict(color=RED, width=3), showlegend=i == 0), r, c)
    print(titles[i])
fig.update_yaxes(range=[-0.2, 0.9])
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1500, height=850, font=FONT, margin=dict(l=40, r=20, t=50, b=40),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.07, font_size=20))
fig.write_image(HERE / "stages.png", scale=2)
fig.write_image(HERE / "stages.pdf")

fig = go.Figure()
n = np.arange(1, 201)
for lr, col in [(1.0, RED), (0.5, GREEN), (0.1, BLUE)]:
    f0, trees = boost(200, lr, 8)
    tr = [mse(y, predict(f0, trees[:m], lr, X)) for m in n]
    te = [mse(y_test, predict(f0, trees[:m], lr, X_test)) for m in n]
    fig.add_trace(go.Scatter(x=n, y=te, name=f"learning rate {lr}: test", line=dict(color=col, width=3)))
    fig.add_trace(go.Scatter(x=n, y=tr, name=f"learning rate {lr}: train", line=dict(color=col, width=2, dash="dot")))
    print(lr, "best test", round(min(te), 5), "after", int(np.argmin(te)) + 1, "trees; test after 200:", round(te[-1], 5),
          "train after 200:", round(tr[-1], 6))
fig.update_xaxes(title="number of trees (log scale)", type="log")
fig.update_yaxes(title="mean squared error", range=[0, 0.012])
fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, margin=dict(l=80, r=20, t=20, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.17, yanchor="top", font_size=17))
fig.write_image(HERE / "learning_rate.png", scale=2)
fig.write_image(HERE / "learning_rate.pdf")
