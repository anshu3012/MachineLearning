"""Training the 2-2-1 network of section 5.1 on the XOR clouds, step by step: the same data, starting weights
(seed 0, std 0.01), learning rate 1 and 5,000 steps of plain gradient descent as playground.TwoNodeNet.
Each frame: the output node's probability (shading), its 0.5 decision boundary (black) and the two hidden nodes'
lines (dashed). Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from playground import datasets, fit_xor, sigmoid

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED = "#54A24B", "#E45756"
X, y = datasets()["xor"]
rng = np.random.default_rng(0)                          # exactly TwoNodeNet(seed=0).fit
W1, b1 = rng.normal(0, 0.01, (2, 2)), np.zeros(2)
w2, b2 = rng.normal(0, 0.01, 2), 0.0
SHOW = [0, 500, 1000, 1500, 1600, 1650, 1700, 1750, 2000, 5000]
snaps = {}
for step in range(5001):
    if step in SHOW:
        snaps[step] = (W1.copy(), b1.copy(), w2.copy(), b2)
    H = sigmoid(X @ W1 + b1)
    p = sigmoid(H @ w2 + b2)
    d = (p - y) / len(y)
    dH = np.outer(d, w2) * H * (1 - H)
    w2, b2 = w2 - H.T @ d, b2 - d.sum()
    W1, b1 = W1 - X.T @ dH, b1 - dH.sum(axis=0)
_, _, ref = fit_xor(seed=0)
assert np.allclose(snaps[5000][0], ref.W1) and np.allclose(snaps[5000][2], ref.w2)
g = np.linspace(-3, 3, 181)
G1, G2 = np.meshgrid(g, g)
GRID = np.c_[G1.ravel(), G2.ravel()]


def stats(s):
    W1, b1, w2, b2 = snaps[s]
    p = sigmoid(sigmoid(X @ W1 + b1) @ w2 + b2)
    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    return loss, 100 * ((p > 0.5) == y).mean()


assert stats(5000)[1] == 100 and stats(1000) [1] == 50 and round(stats(1000)[0], 3) == 0.693 and round(stats(1700)[1]) == 92


def frame(s):
    W1, b1, w2, b2 = snaps[s]
    P = sigmoid(sigmoid(GRID @ W1 + b1) @ w2 + b2).reshape(G1.shape)
    loss, acc = stats(s)
    fig = go.Figure()
    fig.add_trace(go.Heatmap(x=g, y=g, z=P, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                             colorscale=[[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]]))
    if P.min() < 0.5 < P.max():
        fig.add_trace(go.Contour(x=g, y=g, z=P, showscale=False, contours_coloring="none", hoverinfo="skip",
                                 contours=dict(start=0.5, end=0.5, size=1), line=dict(width=5, color="black"), showlegend=False))
    for j, dash in ((0, "dash"), (1, "dot")):
        a, c, bb = W1[0, j], W1[1, j], b1[j]
        if abs(c) > 1e-9:
            fig.add_scatter(x=g, y=-(a * g + bb) / c, mode="lines", line=dict(color="#4C78A8", width=3, dash=dash),
                            showlegend=False)
    for lab, col in ((1, GREEN), (0, RED)):
        m = y == lab
        fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                        marker=dict(size=8, color=col, line=dict(width=0.6, color="white")))
    fig.update_layout(template="simple_white", width=860, height=860, font=FONT, showlegend=False,
                      title=dict(text=f"Gradient descent step {s:,}: log loss {loss:.3f}, accuracy {acc:.0f}%",
                                 x=0.5, y=0.97, font=dict(size=22)),
                      xaxis=dict(title="x₁", range=[-3, 3]), yaxis=dict(title="x₂", range=[-3, 3], scaleanchor="x"),
                      margin=dict(l=70, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    print({s: tuple(round(v, 3) for v in stats(s)) for s in SHOW})
    tmp = HERE / ".xt_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for s in SHOW:
        keys[s] = tmp / f"s{s}.png"
        frame(s).write_image(keys[s])
    seq = [s for s in SHOW for _ in range(2)] + [SHOW[-1]] * 5
    for j, s in enumerate(seq):
        shutil.copy(keys[s], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=680:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "xor_training.gif")], check=True)
    ims = [Image.open(keys[s]).convert("RGB") for s in (1000, 1650, 5000)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "xor_training_frames.png")
    shutil.rmtree(tmp)
