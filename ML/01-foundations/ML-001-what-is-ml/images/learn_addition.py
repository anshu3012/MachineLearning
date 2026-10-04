"""Training finds the pattern: a model  sum = w1*a + w2*b + c  starts with random numbers and, by gradient descent on
pairs of numbers and their sums, ends at w1 = 1, w2 = 1, c = 0, which is addition. Data: the two-number rows of the
Note's table (2 + 3 = 5, 10 + 4 = 14) plus 18 random pairs from 0 to 10 (seed 0). Nobody writes "add" into it.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#8A8A8A"

rng = np.random.default_rng(0)
X = np.vstack([[2, 3], [10, 4], rng.integers(0, 11, size=(18, 2))]).astype(float)
y = X.sum(axis=1)
w, c, lr = np.array([0.2, -0.3]), 3.0, 0.004            # a model that knows nothing yet
history = []
for step in range(3001):
    history.append((step, w.copy(), c))
    err = X @ w + c - y
    w, c = w - lr * 2 * X.T @ err / len(y), c - lr * 2 * err.mean()
SHOW = [0, 1, 2, 4, 8, 15, 30, 60, 120, 250, 500, 1000, 2000, 3000]
fs, fw, fc = history[-1]
assert np.allclose(fw, 1, atol=0.01) and abs(fc) < 0.05, (fw, fc)
assert abs(fw @ [7, 8] + fc - 15) < 0.05


def frame(step):
    _, w, c = history[step]
    pred = X @ w + c
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.14,
                        subplot_titles=("Model's answer vs true sum", "The numbers the model learns"))
    fig.add_scatter(x=[0, 21], y=[0, 21], mode="lines", line=dict(color=GREY, dash="dash"), showlegend=False,
                    row=1, col=1)
    fig.add_scatter(x=y, y=pred, mode="markers", marker=dict(size=13, color=BLUE, line=dict(width=1, color="white")),
                    showlegend=False, row=1, col=1)
    fig.add_annotation(x=5, y=22, text="perfect answers lie<br>on the dashed line", showarrow=False,
                       font=dict(size=16, color=GREY), row=1, col=1)
    fig.add_bar(x=["w1", "w2", "c"], y=[w[0], w[1], c], marker_color=[ORANGE, ORANGE, GREEN],
                text=[f"{v:.2f}" for v in (w[0], w[1], c)], textposition="outside", showlegend=False, row=1, col=2)
    for xv, tv in (("w1", 1), ("w2", 1), ("c", 0)):
        fig.add_scatter(x=[xv], y=[tv], mode="markers", marker=dict(symbol="line-ew", size=60, color="black",
                        line=dict(width=3)), showlegend=False, row=1, col=2)
    new = w @ [7, 8] + c
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT,
                      title=dict(text=f"Training step {step}:  sum ≈ {w[0]:.2f}·a {'+' if w[1] >= 0 else '−'} {abs(w[1]):.2f}·b"
                                      f" {'+' if c >= 0 else '−'} {abs(c):.2f}<br>new input 7, 8 → <b>{new:.2f}</b>",
                                 x=0.5, y=0.96, font=dict(size=24)),
                      margin=dict(l=70, r=30, t=140, b=80))
    fig.update_xaxes(title_text="true sum", range=[0, 21], row=1, col=1)
    fig.update_yaxes(title_text="model's answer", range=[-1, 26], row=1, col=1)
    fig.update_yaxes(range=[-0.6, 3.6], row=1, col=2)
    fig.add_annotation(x=1.0, y=-0.13, xref="paper", yref="paper", text="black marks: addition (1, 1, 0)",
                       showarrow=False, font=dict(size=16), xanchor="right")
    for a in fig.layout.annotations[:2]:
        a.font.size = 20
    return fig


if __name__ == "__main__":
    tmp = HERE / ".la_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for s in SHOW:
        keys[s] = tmp / f"s{s}.png"
        frame(s).write_image(keys[s])
    seq = [SHOW[0]] * 3 + [s for s in SHOW[1:] for _ in range(2)] + [SHOW[-1]] * 6
    for j, s in enumerate(seq):
        shutil.copy(keys[s], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "learn_addition.gif")], check=True)
    ims = [Image.open(keys[s]).convert("RGB") for s in (0, 3000)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "learn_addition_frames.png")
    shutil.rmtree(tmp)
