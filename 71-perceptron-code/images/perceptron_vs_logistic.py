"""Perceptron trick (seed 0, left) and logistic regression trained by gradient descent (right) on the Note's 100 points,
both starting from the weights (1, 1, 1). The perceptron's decision boundary stops after its 6th update, as soon as no
point is misclassified. Gradient descent on the log loss (with scikit-learn's C = 100 penalty) keeps moving the
boundary towards the middle of the gap and ends on scikit-learn's LogisticRegression(C=100) boundary.
Run: python perceptron_vs_logistic.py  -> perceptron_vs_logistic.gif, _frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
BLUE, GREEN, RED = "#4C78A8", "#54A24B", "#E45756"
X, y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=10)
Xb = np.insert(X, 0, 1, axis=1)
C = 100

rng = np.random.default_rng(0)                      # the perceptron run of section 3
w, P = np.ones(3), [np.ones(3)]
for _ in range(1000):
    j = rng.integers(0, len(y))
    y_hat = 1 if Xb[j] @ w > 0 else 0
    if y[j] != y_hat:
        w = w + 0.1 * (y[j] - y_hat) * Xb[j]
        P.append(w.copy())
assert len(P) == 7

w, G = np.ones(3), {0: np.ones(3)}                  # gradient descent on scikit-learn's objective, divided by n
STEPS = 200000
for s in range(1, STEPS + 1):
    p = 1 / (1 + np.exp(-Xb @ w))
    w = w - 0.5 * ((Xb.T @ (p - y)) + np.r_[0, w[1:]] / C) / len(y)
    G[s] = w.copy() if s in (1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 300, 500, 800, 1200, 2000, 3000, 5000, 8000,
                             12000, 20000, 30000, 50000, 80000, 120000, STEPS) else None
G = {k: v for k, v in G.items() if v is not None}
sk = LogisticRegression(C=C, max_iter=10000).fit(X, y)
w_sk = np.r_[sk.intercept_, sk.coef_[0]]
line = lambda w, x2: -(w[0] + w[2] * x2) / w[1]
x2s = np.array([-3.2, 2.4])
assert np.abs(line(w, x2s) - line(w_sk, x2s)).max() < 0.01, (w, w_sk)     # same boundary as scikit-learn


def gaps(w):
    d = (Xb @ w) / np.linalg.norm(w[1:])
    return d[y == 1].min(), -d[y == 0].max()


print("perceptron gaps", np.round(gaps(P[-1]), 3), "gradient descent gaps", np.round(gaps(w), 3))
gsteps = list(G)
N = len(gsteps)


def frame(k):
    kp = min(k, 6)
    wp, wg = P[kp], G[gsteps[k]]
    gp, gg = gaps(wp), gaps(wg)
    lab = lambda g: (f"gap to green {g[0]:.2f}, to blue {g[1]:.2f}" if min(g) > 0 else "some points misclassified")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.07, shared_yaxes=True, subplot_titles=(
        f"Perceptron: update {kp} of 6" + (", stopped" if k >= 6 else "") + f"<br>{lab(gp)}",
        f"Logistic regression: step {gsteps[k]:,}<br>{lab(gg)}"))
    for c, wv, col in ((1, wp, RED), (2, wg, "black")):
        for cls, cc in ((1, GREEN), (0, BLUE)):
            fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", marker=dict(color=cc, size=11)), 1, c)
        fig.add_trace(go.Scatter(x=line(wv, x2s), y=x2s, mode="lines", line=dict(color=col, width=5)), 1, c)
        fig.update_xaxes(range=[-2.2, 0.6], title="x₁ (zoomed on the gap)", row=1, col=c)
    fig.update_yaxes(range=[-3.2, 2.4])
    fig.update_yaxes(title_text="x₂", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=80, r=20, t=110, b=70))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pvl_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "perceptron_vs_logistic.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 6, 16, N - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "perceptron_vs_logistic_frames.png")
    shutil.rmtree(tmp)
