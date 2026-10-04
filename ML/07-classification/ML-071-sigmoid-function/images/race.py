"""The step perceptron and the sigmoid perceptron trained side by side (Plotly frames -> GIF), on the Note's data
(make_classification, class_sep 30, random_state 41), learning rate 0.1, the same random points (seed 0). The step
line stops moving at the last mistake; the sigmoid line keeps moving away from the near green points. Titles give
each line's gap to the nearest green point. After 1,000 loops the gaps are those of the Note's table."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
X, y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=30)
Xb = np.insert(X, 0, 1, axis=1)
sig = lambda z: 1 / (1 + np.exp(-z))
step = lambda z: 1.0 if z > 0 else 0.0


def history(f, loops=1000):
    rng = np.random.default_rng(0); w = np.ones(3); out = [w.copy()]
    for _ in range(loops):
        j = rng.integers(0, len(y)); w = w + 0.1 * (y[j] - f(Xb[j] @ w)) * Xb[j]; out.append(w.copy())
    return out


def gaps(w):
    d = (Xb @ w) / np.linalg.norm(w[1:]); return d[y == 1].min(), -d[y == 0].max()


HS, HG = history(step), history(sig)
g_s, g_g = gaps(HS[-1]), gaps(HG[-1])
assert (round(g_s[1], 2), round(g_s[0], 2)) == (2.41, 0.25) and (round(g_g[1], 2), round(g_g[0], 2)) == (3.07, 1.21)
last_change = max(i for i in range(1, 1001) if not np.array_equal(HS[i], HS[i - 1]))
assert last_change == 44
ys = np.linspace(-3.2, 2.4, 20)
label = lambda w: (f"gap to green {gaps(w)[0]:.2f}" if min(gaps(w)) > 0 else "some points on the wrong side")
KS = [0, 5, 10, 20, 40, 80, 150, 250, 400, 600, 800, 1000]


def frame(k):
    fig = make_subplots(1, 2, horizontal_spacing=0.08,
                        subplot_titles=[f"step: {label(HS[k])}", f"sigmoid: {label(HG[k])}"])
    fig.update_annotations(font_size=21)
    for col, H, c in ((1, HS, RED), (2, HG, ORANGE)):
        for cls, cc in ((1, GREEN), (0, BLUE)):
            fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", marker=dict(color=cc, size=7)), 1, col)
        w = H[k]
        fig.add_trace(go.Scatter(x=-(w[0] + w[2] * ys) / w[1], y=ys, mode="lines", line=dict(color=c, width=4)), 1, col)
        fig.update_xaxes(title="x₁", range=[-6.2, 3.2], row=1, col=col)
        fig.update_yaxes(range=[-3.2, 2.4], row=1, col=col)
    fig.update_layout(template="simple_white", width=1200, height=540, font=FONT, showlegend=False,
                      title=dict(text=f"after {k} random points", x=0.5), margin=dict(l=60, r=30, t=100, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in KS], here / "race", fps=2, holds=[2] + [1] * (len(KS) - 2) + [6], keys=[3, len(KS) - 1], cols=1)

