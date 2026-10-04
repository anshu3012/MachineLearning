"""Five perceptron runs (seeds 0-4) vs logistic regression (C=100) on the same data, with a zoom on the gap (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

here = Path(__file__).parent
X, y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=10)
Xb = np.insert(X, 0, 1, axis=1)


def perceptron(seed, lr=0.1, loops=1000):
    rng = np.random.default_rng(seed)
    w = np.ones(3)
    for _ in range(loops):
        j = rng.integers(0, len(y))
        w = w + lr * (y[j] - (1 if Xb[j] @ w > 0 else 0)) * Xb[j]
    return w


def gaps(w):
    d = (Xb @ w) / np.linalg.norm(w[1:])
    return d[y == 1].min(), -d[y == 0].max()


lr = LogisticRegression(C=100, max_iter=10000).fit(X, y)
w_lr = np.r_[lr.intercept_, lr.coef_[0]]
ys = np.linspace(-3.2, 2.4, 50)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, column_widths=[0.55, 0.45],
                    subplot_titles=("All the data", "Zoom on the gap between the classes"))
for col in (1, 2):
    for k, c in ((1, "#54A24B"), (0, "#4C78A8")):
        fig.add_trace(go.Scatter(x=X[y == k, 0], y=X[y == k, 1], mode="markers", marker=dict(color=c, size=8),
                                 showlegend=False), 1, col)
for s in range(5):
    w = perceptron(s)
    g = gaps(w)
    print("seed", s, w.round(3), "gap to class 1", round(g[0], 3), "gap to class 0", round(g[1], 3))
    for col in (1, 2):
        fig.add_trace(go.Scatter(x=-(w[0] + w[2] * ys) / w[1], y=ys, mode="lines", line=dict(color="#E45756", width=2),
                                 opacity=0.7, name="perceptron (5 random orders)" if s == 0 else None,
                                 showlegend=(s == 0 and col == 1)), 1, col)
g = gaps(w_lr)
print("logistic", w_lr.round(3), "gaps", round(g[0], 3), round(g[1], 3))
for col in (1, 2):
    fig.add_trace(go.Scatter(x=-(w_lr[0] + w_lr[2] * ys) / w_lr[1], y=ys, mode="lines", line=dict(color="black", width=4),
                             name="logistic regression", showlegend=(col == 1)), 1, col)
fig.update_xaxes(range=[-2.6, 2.4], title="x₁", row=1, col=1)
fig.update_xaxes(range=[-1.15, -0.35], title="x₁", row=1, col=2)
fig.update_yaxes(range=[-3.2, 2.4], title="x₂", row=1, col=1)
fig.update_yaxes(range=[-3.2, 2.4], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=540, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.5, y=-0.2, xanchor="center", orientation="h"), margin=dict(l=60, r=20, t=50, b=90))
fig.write_image(here / "compare.png", scale=2); fig.write_image(here / "compare.pdf")
