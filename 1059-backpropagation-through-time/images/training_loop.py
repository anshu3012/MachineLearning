"""Section 8: the full training loop on the three toy reviews. NumPy BPTT + gradient descent (lr 0.5, the three
reviews averaged per update), from the Notebook's seeded Keras starting weights. Left: mean loss per epoch.
Right: the prediction for each review moving toward its target.
Run: python training_loop.py  -> training_loop.gif, training_loop_frames.png (Plotly frames + ffmpeg)"""
import os
import shutil
import subprocess
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import keras
import numpy as np
import plotly.graph_objects as go
import tensorflow as tf
from plotly.subplots import make_subplots

from common import BLUE, GREEN, GREY, ORANGE, RED

HERE = Path(__file__).parent
keras.utils.set_random_seed(42)                               # same start as the Notebook
tf.config.experimental.enable_op_determinism()
vocab, reviews, Y = ["cat", "mat", "rat"], ["cat mat rat", "rat rat mat", "mat mat cat"], np.array([1.0, 1.0, 0.0])
X = np.array([[np.eye(3)[vocab.index(w)] for w in r.split()] for r in reviews])
model = keras.Sequential([keras.Input(shape=(3, 3)), keras.layers.SimpleRNN(3, use_bias=False),
                          keras.layers.Dense(1, activation="sigmoid", use_bias=False)])
W = [w.astype("float64") for w in model.get_weights()]


def bptt(x, y, W_i, W_h, W_o):
    hs = [np.zeros(3)]
    for t in range(3):
        hs.append(np.tanh(x[t] @ W_i + hs[-1] @ W_h))
    p = 1 / (1 + np.exp(-(hs[3] @ W_o)))
    L = -(y * np.log(p) + (1 - y) * np.log(1 - p)).item()
    dz = p - y
    gW_i, gW_h, dh = np.zeros_like(W_i), np.zeros_like(W_h), dz @ W_o.T
    for t in range(3, 0, -1):
        da = dh * (1 - hs[t] ** 2)
        gW_i += np.outer(x[t - 1], da)
        gW_h += np.outer(hs[t - 1], da)
        dh = da @ W_h.T
    return L, p.item(), [gW_i, gW_h, np.outer(hs[3], dz)]


history, preds = [], []
for epoch in range(301):
    out = [bptt(xr, yr, *W) for xr, yr in zip(X, Y)]
    history.append(np.mean([o[0] for o in out]))
    preds.append([o[1] for o in out])
    W = [w - 0.5 * np.mean([o[2][k] for o in out], axis=0) for k, w in enumerate(W)]
history, preds = history[:300], np.array(preds)               # loss of epochs 1..300; preds after k updates
assert round(history[0], 3) == 0.809 and round(history[-1], 3) == 0.004, (history[0], history[-1])
assert list(np.round(preds[300], 3)) == [0.997, 0.997, 0.006], preds[300]
SHOW = [0, 2, 5, 10, 15, 20, 30, 40, 50, 60, 80, 100, 130, 160, 200, 250, 300]


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.14,
                        subplot_titles=["mean loss", "prediction ŷ for each review"])
    ep = np.arange(1, k + 1)
    fig.add_trace(go.Scatter(x=ep, y=history[:k], mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 1)
    if k:
        fig.add_trace(go.Scatter(x=[k], y=[history[k - 1]], mode="markers+text", text=[f"{history[k - 1]:.3f}"],
                                 textposition="top right" if k < 200 else "top left", marker=dict(size=12, color=BLUE), showlegend=False), 1, 1)
    names = [f"{r}<br>(target {int(y)})" for r, y in zip(reviews, Y)]
    colours = [GREEN, GREEN, RED]
    fig.add_trace(go.Bar(x=names, y=preds[k], marker_color=colours, text=[f"{p:.3f}" for p in preds[k]],
                         textposition="outside", showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=names, y=Y, mode="markers", marker=dict(symbol="line-ew", size=60,
                             line=dict(width=4, color="black")), name="target", showlegend=False), 1, 2)
    fig.update_xaxes(title_text="epoch", range=[0, 305], row=1, col=1)
    fig.update_yaxes(range=[0, 0.9], row=1, col=1)
    fig.update_yaxes(range=[0, 1.15], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"after {k} gradient descent updates   (black line = target)", x=0.5),
                      margin=dict(l=60, r=20, t=110, b=60))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".train_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(SHOW):
        frame(k).write_image(tmp / f"{i:03d}.png")
    n = len(SHOW)
    for i in range(n, n + 6):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "training_loop.gif")], check=True)
    shutil.copy(tmp / f"{n - 1:03d}.png", HERE / "training_loop_frames.png")   # last frame: whole loss curve, readable in the PDF
    shutil.rmtree(tmp)
