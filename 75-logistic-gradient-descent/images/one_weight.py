"""Gradient descent on one weight. Data: the first 30 students of the placement data (Note 13), feature x = CGPA - 6,
target placed (1) or not (0). Model: P(placed) = sigmoid(w * x), one weight and no intercept.
Left: the log loss against w, with a ball that steps downhill; each step is the learning rate times the slope there.
Right: the S-curve that the current w gives, over the data.
Run: python one_weight.py  -> one_weight.gif, one_weight_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, GREEN, RED = "#4C78A8", "#54A24B", "#E45756"
d = pd.read_csv(HERE.parent / "data" / "placement_30.csv")
x, y = d.cgpa.to_numpy() - 6, d.placed.to_numpy()
sig = lambda z: 1 / (1 + np.exp(-z))
loss = lambda w: -np.mean(y * np.log(sig(w * x)) + (1 - y) * np.log(1 - sig(w * x)))
slope = lambda w: -np.mean((y - sig(w * x)) * x)
LR, N = 4.0, 60
ws = [0.0]
for _ in range(N):
    ws.append(ws[-1] - LR * slope(ws[-1]))
for k in range(4):
    print(f"step {k + 1}: w {ws[k]:.3f}  loss {loss(ws[k]):.3f}  slope {slope(ws[k]):.3f}  step {-LR * slope(ws[k]):.3f}  new w {ws[k + 1]:.3f}")
print("after", N, "steps: w", round(ws[-1], 3), "loss", round(loss(ws[-1]), 4), "slope", round(slope(ws[-1]), 4))
i = int(np.argmin(abs(d.cgpa - 6.8)))
print("one student: cgpa", d.cgpa[i], "placed", y[i], "x", x[i])
steps = np.abs(np.diff(ws))
assert all(a > b for a, b in zip(steps, steps[1:])) and all(loss(a) > loss(b) for a, b in zip(ws, ws[1:]))   # steps shrink, loss falls
grid = np.linspace(-0.5, 7, 300)
Lg = np.array([loss(w) for w in grid])
xs = np.linspace(-3, 3, 200)


def frame(k):
    w = ws[k]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=(
        f"log loss {loss(w):.3f}, slope {slope(w):.3f}".replace("-", "−"), f"the curve for w = {w:.2f}"))
    fig.add_trace(go.Scatter(x=grid, y=Lg, mode="lines", line=dict(color=BLUE, width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=ws[:k + 1], y=[loss(v) for v in ws[:k + 1]], mode="lines+markers",
                             line=dict(color=RED, width=2), marker=dict(size=9, color=RED)), 1, 1)
    fig.add_trace(go.Scatter(x=[w], y=[loss(w)], mode="markers", marker=dict(size=20, color=RED,
                             line=dict(color="black", width=2))), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=sig(w * xs), mode="lines", line=dict(color="black", width=5)), 1, 2)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=13, color=[GREEN if v else BLUE for v in y])), 1, 2)
    fig.update_xaxes(title="weight w", range=[-0.5, 7], row=1, col=1)
    fig.update_yaxes(title="log loss", range=[0, 0.75], row=1, col=1)
    fig.update_xaxes(title="x = CGPA − 6", range=[-3, 3], row=1, col=2)
    fig.update_yaxes(title="P(placed)", range=[-0.08, 1.08], tickvals=[0, 0.5, 1], row=1, col=2)
    nxt = f"next step = {LR:g} × {-slope(w):.3f} = {-LR * slope(w):.3f}" if k < N else f"the steps have shrunk to {-LR * slope(w):.3f}"
    fig.update_layout(template="simple_white", width=1150, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=80, r=20, t=140, b=70),
                      title=dict(text=f"step {k}: w = {w:.3f}<br><span style='font-size:22px'>{nxt}</span>", x=0.5, y=0.96))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ow_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N + 1, N + 9):
        shutil.copy(tmp / f"{N:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "one_weight.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, 3, N)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i_, im in enumerate(keys):
        sheet.paste(im, ((i_ % 2) * (w_ + 16), (i_ // 2) * (h_ + 16)))
    sheet.save(HERE / "one_weight_frames.png")
    shutil.rmtree(tmp)
