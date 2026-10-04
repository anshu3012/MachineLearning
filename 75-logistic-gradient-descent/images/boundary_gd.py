"""Two Plotly-frame animations for logistic regression trained by batch gradient descent (lr 0.5, start w = 1).
boundary_gd: 100 overlapping points (make_classification, class_sep 1.5, random state 4). The line turns into
  place while the log loss falls to scikit-learn's minimum (penalty=None).
separable_growth: perfectly separated points (class_sep 20, random state 41). The line barely moves, but the
  weights keep growing, so the band where the model is unsure (0.1 < p < 0.9) keeps narrowing.
Run: python boundary_gd.py -> boundary_gd.gif/_frames.png, separable_growth.gif/_frames.png (Plotly + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
BLUE, GREEN, ORANGE, RED = "#4C78A8", "#54A24B", "#F58518", "#E45756"
FONT = dict(family="Latin Modern Roman", size=22)
sig = lambda z: 1 / (1 + np.exp(-z))


def train(X, y, epochs, keep):
    Xb, w, out = np.insert(X, 0, 1, axis=1), np.ones(3), {0: np.ones(3)}
    for e in range(1, epochs + 1):
        w = w + 0.5 * (Xb.T @ (y - sig(Xb @ w))) / len(y)
        if e in keep:
            out[e] = w.copy()
    return out


def loss(X, y, w):
    return log_loss(y, sig(w[0] + X @ w[1:]))


def render(figs, name, fps, keys, hold=12):
    tmp = HERE / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    for k, fig in enumerate(figs):
        fig.write_image(tmp / f"{k:03d}.png")
    for k in range(len(figs), len(figs) + hold):            # hold the last frame
        shutil.copy(tmp / f"{len(figs) - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


def panel(X, y, w, xr, yr, band):
    """Left panel traces: shaded p-regions, points, the line p = 0.5."""
    gx, gy = np.linspace(*xr, 160), np.linspace(*yr, 160)
    GX, GY = np.meshgrid(gx, gy)
    P = sig(w[0] + w[1] * GX + w[2] * GY)
    tr = [go.Contour(x=gx, y=gy, z=P, zmin=0, zmax=1, showscale=False, line=dict(width=0),
                     contours=dict(start=band[0], end=band[-1], size=band[1] - band[0]) if len(band) > 1
                     else dict(start=0.5, end=0.5, size=1),
                     colorscale=[[0, "#C9DAEC"], [0.5, "#FFFFFF"], [1, "#CDE6C6"]], opacity=0.9)]
    for k, c, nm in ((1, GREEN, "class 1"), (0, BLUE, "class 0")):
        tr.append(go.Scatter(x=X[y == k, 0], y=X[y == k, 1], mode="markers", name=nm,
                             marker=dict(color=c, size=10, line=dict(color="white", width=1))))
    xs = np.array(xr)
    tr.append(go.Scatter(x=xs, y=-(w[0] + w[1] * xs) / w[2], mode="lines", name="p = 0.5",
                         line=dict(color=ORANGE, width=5)))
    return tr


def layout(fig, title, xr, yr):
    fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=70, r=30, t=110, b=70))
    fig.update_annotations(font_size=24)
    fig.update_xaxes(title="x₁", range=xr, row=1, col=1)
    fig.update_yaxes(title="x₂", range=yr, row=1, col=1)
    return fig


# ---- 1. overlapping data: the line turns into place -------------------------------------------------------
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=4, class_sep=1.5)
sk = LogisticRegression(penalty=None, max_iter=100000, tol=1e-10).fit(X, y)
w_sk = np.r_[sk.intercept_, sk.coef_[0]]
EP = [0] + sorted({int(round(v)) for v in np.geomspace(1, 5000, 34)})
snaps = train(X, y, 5000, set(EP))
L = {e: loss(X, y, w) for e, w in snaps.items()}
assert np.allclose(snaps[5000], w_sk, atol=2e-3)              # matches the Note's table
assert abs(L[5000] - loss(X, y, w_sk)) < 1e-4
XR, YR = [-4.5, 1.2], [-4.3, 3.8]
figs = []
for e in EP:
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                        subplot_titles=("the line moves", "the loss falls"))
    for t in panel(X, y, snaps[e], XR, YR, [0.5]):
        fig.add_trace(t, 1, 1)
    fig.add_trace(go.Scatter(x=XR, y=-(w_sk[0] + w_sk[1] * np.array(XR)) / w_sk[2], mode="lines",
                             line=dict(color="black", width=2, dash="dash")), 1, 1)
    seen = [k for k in EP if 1 <= k <= e]
    fig.add_trace(go.Scatter(x=seen, y=[L[k] for k in seen], mode="lines+markers",
                             line=dict(color=ORANGE, width=4), marker=dict(size=8)), 1, 2)
    fig.add_trace(go.Scatter(x=[1, 5000], y=[L[5000]] * 2, mode="lines", line=dict(color="black", width=2, dash="dash")), 1, 2)
    fig.add_annotation(x=np.log10(5000), y=L[5000], text="scikit-learn", showarrow=False, xanchor="right",
                       yanchor="bottom", row=1, col=2, font=dict(size=20))
    fig.update_xaxes(type="log", title="epoch", range=[0, np.log10(5000) + 0.05], dtick=1, row=1, col=2)
    fig.update_yaxes(title="log loss", range=[0.12, 0.42], row=1, col=2)
    figs.append(layout(fig, f"epoch {e}   ·   log loss {L[e]:.4f}", XR, YR))
idx = {e: i for i, e in enumerate(EP)}
render(figs, "boundary_gd", 6, [0, idx[min(EP, key=lambda v: abs(v - 10))], idx[min(EP, key=lambda v: abs(v - 100))], len(EP) - 1])

# ---- 2. separable data: the weights never settle ------------------------------------------------------------
Xs, ys = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                             n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=20)
EP2 = sorted({int(round(v)) for v in np.geomspace(10, 50000, 30)})
s2 = train(Xs, ys, 50000, set(EP2))
norms = {e: np.linalg.norm(s2[e]) for e in EP2}
assert all(norms[a] < norms[b] for a, b in zip(EP2, EP2[1:]))  # weights grow without settling
assert np.allclose(s2[50000], [8.20, 6.52, 0.37], atol=0.01)   # the Note's table
XR2, YR2 = [-4.6, 3.0], [-3.4, 2.6]
figs = []
for e in EP2:
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=("unsure band 0.1 < p < 0.9", "size of the weights"))
    for t in panel(Xs, ys, s2[e], XR2, YR2, [0.1, 0.5, 0.9]):
        fig.add_trace(t, 1, 1)
    seen = [k for k in EP2 if k <= e]
    fig.add_trace(go.Scatter(x=seen, y=[norms[k] for k in seen], mode="lines+markers",
                             line=dict(color=RED, width=4), marker=dict(size=8)), 1, 2)
    fig.update_xaxes(type="log", title="epoch", range=[1, np.log10(50000) + 0.05], dtick=1, row=1, col=2)
    fig.update_yaxes(title="length of w", range=[0, 11], row=1, col=2)
    figs.append(layout(fig, f"epoch {e}   ·   log loss {loss(Xs, ys, s2[e]):.5f}", XR2, YR2))
render(figs, "separable_growth", 6, [0, 10, 20, len(EP2) - 1])
print(snaps[5000].round(3), w_sk.round(3))
