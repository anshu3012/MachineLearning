"""XOR with 2 hidden nodes, and the TensorFlow Playground demos rebuilt in Python.
Run: python playground.py -> xor_lines.png/.pdf and playground.png/.pdf. The Notebook builds the same models."""
from pathlib import Path
import warnings
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")      # adam may stop at max_iter on the sigmoid spiral: that failure is the point
here = Path(__file__).parent
GREEN, RED = "#54A24B", "#E45756"
SHADE = [[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]]


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def datasets(seed=0):
    rng = np.random.default_rng(seed)
    corners = np.array([[-1.5, -1.5], [1.5, 1.5], [-1.5, 1.5], [1.5, -1.5]])   # the four XOR inputs, centred
    k = np.repeat(np.arange(4), 50)                                            # 50 noisy points around each
    Xx = corners[k] + rng.normal(0, 0.3, (200, 2))
    yx = (k >= 2).astype(int)                       # XOR: class 1 where exactly one input is positive
    Xc, yc = make_circles(200, noise=0.08, factor=0.4, random_state=seed)
    rng = np.random.default_rng(seed)                                 # the spirals get their own random numbers
    t = np.sqrt(rng.uniform(0, 1, 150)) * 3 * np.pi                  # two interleaved spirals
    arm = np.c_[t * np.cos(t), t * np.sin(t)] / 3
    Xs = np.r_[arm, -arm] + rng.normal(0, 0.15, (300, 2))
    ys = np.r_[np.zeros(150), np.ones(150)].astype(int)
    return {"xor": (Xx, yx), "circles": (Xc * 2.5, yc), "spiral": (Xs, ys)}


class TwoNodeNet:
    """2 inputs -> 2 sigmoid hidden nodes -> 1 sigmoid output.
    Plain gradient descent on the log loss, all 200 points per step, small random starting weights."""

    def __init__(self, seed=0, lr=1.0, epochs=5000, init_std=0.01):
        self.seed, self.lr, self.epochs, self.init_std = seed, lr, epochs, init_std

    def hidden(self, X):
        return sigmoid(X @ self.W1 + self.b1)        # one column per hidden node

    def predict_proba(self, X):
        p = sigmoid(self.hidden(X) @ self.w2 + self.b2)
        return np.c_[1 - p, p]

    def score(self, X, y):
        return np.mean((self.predict_proba(X)[:, 1] > 0.5) == y)

    def fit(self, X, y):
        rng = np.random.default_rng(self.seed)
        self.W1, self.b1 = rng.normal(0, self.init_std, (2, 2)), np.zeros(2)
        self.w2, self.b2 = rng.normal(0, self.init_std, 2), 0.0
        for _ in range(self.epochs):
            H = self.hidden(X)
            p = sigmoid(H @ self.w2 + self.b2)
            d = (p - y) / len(y)                       # slope of the mean log loss at the output's weighted sum
            dH = np.outer(d, self.w2) * H * (1 - H)   # passed back to each hidden node's weighted sum
            self.w2 = self.w2 - self.lr * H.T @ d
            self.b2 = self.b2 - self.lr * d.sum()
            self.W1 = self.W1 - self.lr * X.T @ dH
            self.b1 = self.b1 - self.lr * dH.sum(axis=0)
        return self


# (title, data, hidden layers, activation, solver, seed)
RUNS = [("Circles: 4 hidden nodes, sigmoid", "circles", (4,), "logistic", "lbfgs", 0),
        ("Spiral: 4 layers of 4, sigmoid", "spiral", (4, 4, 4, 4), "logistic", "adam", 0),
        ("Spiral: 4 layers of 4, ReLU", "spiral", (4, 4, 4, 4), "relu", "adam", 0)]


def fit_xor(seed=0):
    X, y = datasets()["xor"]
    return X, y, TwoNodeNet(seed=seed).fit(X, y)


def fit_all():
    data = datasets()
    out = []
    for title, d, h, act, solver, seed in RUNS:
        X, y = data[d]
        clf = MLPClassifier(h, activation=act, solver=solver, max_iter=5000, random_state=seed).fit(X, y)
        out.append((title, X, y, clf))
    return out


def add_points(fig, X, y, r, c, size=6):
    for lab, col in [(1, GREEN), (0, RED)]:
        m = y == lab
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=col, size=size, line=dict(color="white", width=0.6))), r, c)


def boundary(fig, g, Z, r, c, dash="solid", color="black", width=4):
    fig.add_trace(go.Contour(x=g, y=g, z=Z, showscale=False, hoverinfo="skip", contours_coloring="none",
                             contours=dict(start=0.5, end=0.5, size=1), showlegend=False,
                             line=dict(width=width, color=color, dash=dash)), r, c)


def xor_figure(X, y, net):
    g = np.linspace(-3, 3, 241)
    G1, G2 = np.meshgrid(g, g)
    grid = np.c_[G1.ravel(), G2.ravel()]
    H = [net.hidden(grid)[:, j].reshape(G1.shape) for j in range(2)]
    OUT = net.predict_proba(grid)[:, 1].reshape(G1.shape)
    titles = ["Hidden node 1: one line", "Hidden node 2: another line",
              f"Output node: combines them<br>accuracy {net.score(X, y):.0%}"]
    fig = make_subplots(1, 3, subplot_titles=titles, horizontal_spacing=0.06)
    colours = ["#4C78A8", "#B279A2"]
    for k, Z in enumerate([H[0], H[1], OUT], start=1):
        fig.add_trace(go.Contour(x=g, y=g, z=Z, colorscale=SHADE, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                                 contours=dict(start=0.1, end=0.9, size=0.1), line=dict(width=0.5, color="#BBBBBB")), 1, k)
        if k < 3:
            boundary(fig, g, Z, 1, k, color=colours[k - 1])          # the hidden node's line
        else:
            boundary(fig, g, OUT, 1, 3, width=9)                    # the network's boundary (black) ...
            for j in range(2):                                      # ... lies on the two hidden lines (dashed)
                boundary(fig, g, H[j], 1, 3, dash="dash", color=colours[j])
        add_points(fig, X, y, 1, k)
        fig.update_xaxes(title_text="x<sub>1</sub>", range=[-3, 3], row=1, col=k)
        fig.update_yaxes(range=[-3, 3], scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
    fig.update_yaxes(title_text="x<sub>2</sub>", row=1, col=1)
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=1350, height=520, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=60, r=20, t=80, b=60))
    fig.write_image(here / "xor_lines.png", scale=2)
    fig.write_image(here / "xor_lines.pdf")


def playground_figure(runs):
    fig = make_subplots(1, 3, horizontal_spacing=0.04,
                        subplot_titles=[f"{t}<br>accuracy {c.score(X, y):.0%}" for t, X, y, c in runs])
    g = np.linspace(-4, 4, 250)
    G1, G2 = np.meshgrid(g, g)
    for k, (title, X, y, clf) in enumerate(runs, start=1):
        Z = clf.predict_proba(np.c_[G1.ravel(), G2.ravel()])[:, 1].reshape(G1.shape)
        fig.add_trace(go.Contour(x=g, y=g, z=Z, zmin=0, zmax=1, showscale=False, hoverinfo="skip", colorscale=SHADE,
                                 contours=dict(start=0.5, end=0.5, size=1), line=dict(width=2.5, color="black")), 1, k)
        add_points(fig, X, y, 1, k, size=5)
        fig.update_xaxes(range=[-4, 4], showticklabels=False, row=1, col=k)
        fig.update_yaxes(range=[-4, 4], showticklabels=False, row=1, col=k)
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=1350, height=500, font=dict(family="Latin Modern Roman", size=16),
                      margin=dict(l=20, r=20, t=80, b=20))
    fig.write_image(here / "playground.png", scale=2)
    fig.write_image(here / "playground.pdf")


if __name__ == "__main__":
    X, y, net = fit_xor()
    print("XOR, 2 hidden nodes:", net.score(X, y))
    print("hidden weights (columns = nodes):\n", net.W1.round(2), "\nhidden biases:", net.b1.round(2),
          "\noutput weights:", net.w2.round(2), "output bias:", round(net.b2, 2))
    xor_figure(X, y, net)
    runs = fit_all()
    for title, Xr, yr, clf in runs:
        print(title, round(clf.score(Xr, yr), 3))
    playground_figure(runs)
