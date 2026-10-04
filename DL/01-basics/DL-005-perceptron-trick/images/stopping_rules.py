"""When to stop: run the perceptron trick (random single picks, w <- w + lr (y - y_hat) x) on two Iris problems
and count the misclassified training points after every loop.
Setosa vs versicolor (petal length, petal width) is linearly separable: the count reaches 0 and convergence stops it.
Versicolor vs virginica (same features) is not: the count never reaches 0, so only the loop cap stops it.
Run: python stopping_rules.py -> stopping_rules.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
CAP, LR = 1000, 0.1
iris = load_iris()
X_all, t = iris.data[:, 2:4], iris.target


def run(a, b, seed=0):
    keep = (t == a) | (t == b)
    X = np.c_[np.ones(keep.sum()), X_all[keep]]                # column of 1s carries the bias
    y = (t[keep] == b).astype(float)
    w, rng, counts = np.ones(3), np.random.default_rng(seed), []
    for _ in range(CAP):
        i = rng.integers(len(y))
        w += LR * (y[i] - float(X[i] @ w >= 0)) * X[i]
        counts.append(int(((X @ w >= 0) != y).sum()))
        if counts[-1] == 0:                                     # convergence: no point can move the line
            break
    return np.array(counts), len(y)


sep, n_sep = run(0, 1)
non, n_non = run(1, 2)
assert sep[-1] == 0 and len(sep) < CAP                        # separable: stops early by convergence
assert len(non) == CAP and non.min() > 0                      # not separable: never 0, the cap stops it
for s in range(1, 6):                                         # not a lucky seed
    assert run(0, 1, s)[0][-1] == 0 and run(1, 2, s)[0].min() > 0
print("separable stop at loop", len(sep), "; non-separable best count", non.min(), "of", n_non)
fig = go.Figure()
fig.add_trace(go.Scatter(x=np.arange(1, len(non) + 1), y=non, mode="lines", line=dict(color=RED, width=2),
                         name=f"versicolor vs virginica: never 0, stopped by the cap of {CAP}"))
fig.add_trace(go.Scatter(x=np.arange(1, len(sep) + 1), y=sep, mode="lines", line=dict(color=BLUE, width=3),
                         name=f"setosa vs versicolor: 0 at loop {len(sep)}, converged"))
fig.add_trace(go.Scatter(x=[len(sep)], y=[0], mode="markers", marker=dict(size=16, color=BLUE, symbol="star"),
                         showlegend=False))
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=24),
                  xaxis=dict(title="loop (one random pick and update)", range=[0, CAP + 10]),
                  yaxis=dict(title="misclassified training points", range=[-3, 64]),
                  legend=dict(x=0, y=1.02, yanchor="bottom"), margin=dict(l=80, r=30, t=110, b=70))
fig.write_image(HERE / "stopping_rules.png", scale=2)
