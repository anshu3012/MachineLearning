"""Try a curve, score it, change it, score again: the first 30 students of the placement data (Note 13) (CGPA -> placed).
A candidate S-curve P(placed) = sigmoid(w0 + w1 * cgpa) is changed step by step by gradient descent on the log loss.
Each student's red bar is the gap between the point and the curve, 1 - (probability given to the true class).
The log loss is written on every frame and falls until the curve stops changing.
Run: python curve_search.py  -> curve_search.gif, curve_search_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
BLUE, GREEN, RED, GREY = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
d = pd.read_csv(HERE.parent / "data" / "placement_30.csv")
x, y = d.cgpa.to_numpy(), d.placed.to_numpy()
mu, sd = x.mean(), x.std()
Z = np.c_[np.ones(len(x)), (x - mu) / sd]               # standardised CGPA, so plain gradient descent behaves
sig = lambda z: 1 / (1 + np.exp(-z))
loss = lambda w: -np.mean(y * np.log(sig(Z @ w)) + (1 - y) * np.log(1 - sig(Z @ w)))
w, W = np.array([0.0, -1.0]), {}                        # start from a curve that slopes the wrong way
KEEP = (0, 1, 2, 3, 4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 50, 65, 80, 100, 130, 170, 220, 300, 400, 600, 1000, 2000, 5000, 20000)
for s in range(max(KEEP) + 1):
    if s in KEEP:
        W[s] = w.copy()
    w = w + 1.0 * Z.T @ (y - sig(Z @ w)) / len(y)
sk = LogisticRegression(C=np.inf).fit(Z[:, 1:], y)
assert abs(loss(w) - loss(np.r_[sk.intercept_, sk.coef_[0]])) < 1e-3      # gradient descent reached the minimum
L = {s: loss(v) for s, v in W.items()}
print({s: round(v, 3) for s, v in L.items()})
steps = list(W)
assert all(L[a] > L[b] - 1e-12 for a, b in zip(steps, steps[1:]))
xs = np.linspace(4.5, 9.5, 200)


def frame(k):
    s = steps[k]
    wv = W[s]
    curve = sig(wv[0] + wv[1] * (xs - mu) / sd)
    p = sig(Z @ wv)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.1,
                        subplot_titles=(f"curve {k + 1}: log loss {L[s]:.3f}", "log loss of each curve tried"))
    for xi, yi, pi in zip(x, y, p):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, pi], mode="lines", line=dict(color=RED, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=curve, mode="lines", line=dict(color="black", width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers",
                             marker=dict(size=13, color=[GREEN if v else BLUE for v in y])), 1, 1)
    fig.add_trace(go.Scatter(x=list(range(1, k + 2)), y=[L[t] for t in steps[:k + 1]], mode="lines+markers",
                             line=dict(color=RED, width=4), marker=dict(size=9)), 1, 2)
    fig.update_xaxes(title="CGPA", range=[4.5, 9.5], row=1, col=1)
    fig.update_yaxes(title="P(placed)", range=[-0.08, 1.08], tickvals=[0, 0.5, 1],
                     ticktext=["0 (not placed)", "0.5", "1 (placed)"], row=1, col=1)
    fig.update_xaxes(title="curve number", range=[0, len(steps) + 1], row=1, col=2)
    fig.update_yaxes(range=[0, 1.05], row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=150, r=20, t=80, b=70))
    fig.update_annotations(font_size=26)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cs_frames"
    tmp.mkdir(exist_ok=True)
    N = len(steps)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "curve_search.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 4, 10, N - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "curve_search_frames.png")
    shutil.rmtree(tmp)
