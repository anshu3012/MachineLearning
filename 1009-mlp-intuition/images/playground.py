"""MLPs on non-linear data (the TensorFlow Playground demos, rebuilt with scikit-learn's MLPClassifier).
Run: python playground.py -> playground.png/.pdf. The Notebook builds the same models."""
from pathlib import Path
import warnings
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")      # adam may stop at max_iter on the sigmoid spiral: that failure is the point
here = Path(__file__).parent


def datasets(seed=0):
    rng = np.random.default_rng(seed)
    Xx = rng.uniform(-3, 3, (200, 2))
    yx = (Xx[:, 0] * Xx[:, 1] > 0).astype(int)                      # XOR: same sign -> class 1
    Xc, yc = make_circles(200, noise=0.08, factor=0.4, random_state=seed)
    t = np.sqrt(rng.uniform(0, 1, 150)) * 3 * np.pi                  # two interleaved spirals
    arm = np.c_[t * np.cos(t), t * np.sin(t)] / 3
    Xs = np.r_[arm, -arm] + rng.normal(0, 0.15, (300, 2))
    ys = np.r_[np.zeros(150), np.ones(150)].astype(int)
    return {"xor": (Xx, yx), "circles": (Xc * 2.5, yc), "spiral": (Xs, ys)}


# (title, data, hidden layers, activation, solver, seed)
RUNS = [("XOR: 2 hidden nodes, sigmoid", "xor", (2,), "logistic", "lbfgs", 0),
        ("XOR: 4 hidden nodes, sigmoid", "xor", (4,), "logistic", "lbfgs", 1),
        ("Circles: 4 hidden nodes, sigmoid", "circles", (4,), "logistic", "lbfgs", 0),
        ("Spiral: 4 layers of 4, sigmoid", "spiral", (4, 4, 4, 4), "logistic", "adam", 0),
        ("Spiral: 4 layers of 4, ReLU", "spiral", (4, 4, 4, 4), "relu", "adam", 0)]


def fit_all():
    data = datasets()
    out = []
    for title, d, h, act, solver, seed in RUNS:
        X, y = data[d]
        clf = MLPClassifier(h, activation=act, solver=solver, max_iter=5000, random_state=seed).fit(X, y)
        out.append((title, X, y, clf))
    return out


if __name__ == "__main__":
    runs = fit_all()
    fig = make_subplots(2, 3, horizontal_spacing=0.05, vertical_spacing=0.12,
                        subplot_titles=[f"{t}<br>accuracy {c.score(X, y):.0%}" for t, X, y, c in runs])
    g = np.linspace(-4, 4, 250)
    G1, G2 = np.meshgrid(g, g)
    for k, (title, X, y, clf) in enumerate(runs):
        r, c = k // 3 + 1, k % 3 + 1
        Z = clf.predict_proba(np.c_[G1.ravel(), G2.ravel()])[:, 1].reshape(G1.shape)
        fig.add_trace(go.Contour(x=g, y=g, z=Z, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                                 colorscale=[[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]],
                                 contours=dict(start=0.5, end=0.5, size=1), line=dict(width=2.5, color="black")), r, c)
        for lab, col in [(1, "#54A24B"), (0, "#E45756")]:
            m = y == lab
            fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                                     marker=dict(color=col, size=5, line=dict(color="white", width=0.5))), r, c)
        fig.update_xaxes(range=[-4, 4], showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-4, 4], showticklabels=False, row=r, col=c)
        print(title, round(clf.score(X, y), 3))
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=1200, height=820, font=dict(family="Latin Modern Roman", size=16),
                      margin=dict(l=20, r=20, t=70, b=20))
    fig.write_image(here / "playground.png", scale=2)
    fig.write_image(here / "playground.pdf")
