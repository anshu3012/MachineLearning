"""The batch update as an average of per-point pulls, on the 100 points of section 8 (make_classification, class_sep 1.5,
random state 4), learning rate 0.5, start w = (1, 1, 1). Each point's marker area shows the size of its error y - y_hat:
the pull that point puts on the weights. Well-classified points shrink to dots; the update is the average of all pulls,
so the decision boundary moves a lot while many pulls are large and little once only the overlap points still pull.
Run: python pulls.py  -> pulls.gif, pulls_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import make_classification

HERE = Path(__file__).parent
BLUE, GREEN, ORANGE = "#4C78A8", "#54A24B", "#F58518"
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=4, class_sep=1.5)
Xb = np.insert(X, 0, 1, axis=1)
sig = lambda z: 1 / (1 + np.exp(-z))
EP = [0, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50, 80, 120, 200, 400, 1000, 5000]
w, W = np.ones(3), {}
for e in range(5001):
    if e in EP:
        W[e] = w.copy()
    w = w + 0.5 * Xb.T @ (y - sig(Xb @ w)) / len(y)
err = {e: np.abs(y - sig(Xb @ W[e])) for e in EP}
print({e: (round(err[e].mean(), 3), int((err[e] > 0.5).sum())) for e in EP})
assert err[0].mean() > err[20].mean() > err[5000].mean()          # the pulls shrink as training goes on
XR, YR = [-4.5, 1.2], [-4.3, 3.8]


def frame(e):
    wv, r = W[e], err[e]
    fig = go.Figure()
    for k, c in ((1, GREEN), (0, BLUE)):
        m = y == k
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers",
                                 marker=dict(color=c, size=5 + 34 * np.sqrt(r[m]), opacity=0.75,
                                             line=dict(color="white", width=1))))
    xs = np.array(XR)
    fig.add_trace(go.Scatter(x=xs, y=-(wv[0] + wv[1] * xs) / wv[2], mode="lines", line=dict(color=ORANGE, width=5)))
    fig.update_layout(template="simple_white", width=850, height=680, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=70, r=20, t=130, b=70),
                      title=dict(text=f"epoch {e}: average error size {r.mean():.2f}<br><span style='font-size:21px'>"
                                      "bigger circle = bigger error y − ŷ = stronger pull</span>", x=0.5, y=0.95),
                      xaxis=dict(title="x₁", range=XR), yaxis=dict(title="x₂", range=YR))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pull_frames"
    tmp.mkdir(exist_ok=True)
    for k, e in enumerate(EP):
        frame(e).write_image(tmp / f"{k:03d}.png")
    N = len(EP)
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=700:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pulls.gif")], check=True)
    keys = [Image.open(tmp / f"{EP.index(e):03d}.png").convert("RGB") for e in (0, 3, 20, 5000)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "pulls_frames.png")
    shutil.rmtree(tmp)
