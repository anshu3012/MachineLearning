"""Section 3: representation power. A two-arm spiral (400 points, our own toy data) fitted by an MLP with one hidden
layer of 4 nodes, one layer of 32 nodes, and two layers of 32 nodes (scikit-learn, tanh, Adam, 2,000 epochs).
Accuracy on the training points is averaged over 5 seeds; each map shows the seed whose accuracy is closest to
that mean (a typical run, not the best one).
Run: python spiral_power.py  -> spiral_power.png (Plotly: three decision maps side by side)"""
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPClassifier

from common import BLUE, RED

warnings.filterwarnings("ignore", category=ConvergenceWarning)
HERE = Path(__file__).parent
rng = np.random.default_rng(0)
n = 200
t = np.sqrt(rng.uniform(0, 1, n)) * 3 * np.pi                    # angle along the arm
arm = np.c_[t * np.cos(t), t * np.sin(t)] / (3 * np.pi)
X = np.r_[arm, -arm] + rng.normal(0, 0.03, (2 * n, 2))
y = np.r_[np.zeros(n), np.ones(n)]
SIZES = {"1 hidden layer, 4 nodes": (4,), "1 hidden layer, 32 nodes": (32,), "2 hidden layers, 32 + 32": (32, 32)}


def fit(size, seed):
    return MLPClassifier(size, activation="tanh", max_iter=2000, learning_rate_init=0.01, random_state=seed).fit(X, y)


runs = {k: [fit(s, seed) for seed in range(5)] for k, s in SIZES.items()}
scores = {k: np.array([m.score(X, y) for m in ms]) for k, ms in runs.items()}
acc = {k: v.mean() for k, v in scores.items()}
typical = {k: runs[k][int(np.argmin(abs(scores[k] - acc[k])))] for k in SIZES}
a = list(acc.values())
assert a[0] < a[1] < a[2] or (a[0] < a[1] and a[2] >= 0.99), acc     # more nodes, then more layers, fit better
print({k: round(v, 3) for k, v in acc.items()})

g = np.linspace(-1.15, 1.15, 160)
GX, GY = np.meshgrid(g, g)
fig = make_subplots(1, 3, subplot_titles=[f"{k}<br>accuracy {acc[k]:.2f}" for k in SIZES], horizontal_spacing=0.04)
for c, (k, s) in enumerate(SIZES.items(), start=1):
    P = typical[k].predict_proba(np.c_[GX.ravel(), GY.ravel()])[:, 1].reshape(GX.shape)
    fig.add_trace(go.Heatmap(x=g, y=g, z=(P > 0.5).astype(float), colorscale=[[0, "#F6C7C8"], [1, "#C9D7E8"]], zmin=0, zmax=1,
                             showscale=False), 1, c)
    for cls, col in ((0, RED), (1, BLUE)):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", showlegend=False,
                                 marker=dict(size=5, color=col)), 1, c)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False, scaleanchor="x")
fig.update_layout(template="simple_white", width=1200, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=10, r=10, t=90, b=10))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "spiral_power.png", scale=2)
