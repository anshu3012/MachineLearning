"""The second-order approximation of one leaf's log loss, animated. Leaf of section 12: classes 0, 1, 0, all at
log-odds ln 1.5 (p = 0.6). Part 1: the expansion point a slides along w; the parabola L(a) + g (w - a) + h (w - a)^2 / 2
always touches the exact loss at a, and its minimum a - g/h is the Newton step. Part 2: back at a = 0, lambda grows
and the leaf output w* = -G / (H + lambda) shrinks towards 0.
Run: python newton_leaf.py  -> newton_leaf.gif, newton_leaf_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREEN, GREY = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
yl, z0 = np.array([0, 1, 0]), np.log(1.5)
sig = lambda z: 1 / (1 + np.exp(-z))
L = lambda w: -(yl * np.log(sig(z0 + w)) + (1 - yl) * np.log(1 - sig(z0 + w))).sum()
g = lambda a: (sig(z0 + a) - yl).sum()                   # gradient of the leaf loss at w = a
h = lambda a: 3 * sig(z0 + a) * (1 - sig(z0 + a))        # Hessian
W = np.linspace(-3, 1.5, 300)
EXACT = np.array([L(w) for w in W])
w_exact = np.log(0.5) - z0
assert np.isclose(-g(0) / h(0), -0.8 / 0.72) and np.isclose(round(-g(0) / h(0), 2), -1.11)
assert abs(-g(0) / h(0) - w_exact) < abs(1.2 - g(1.2) / h(1.2) - w_exact)   # far from the minimum, the guess is worse


def frame(a, lam, title):
    G, H = g(a), h(a)
    para = L(a) + G * (W - a) + 0.5 * (H + lam) * (W - a) ** 2 + (0.5 * lam * a * a if lam else 0)
    step = a - G / (H + lam)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=W, y=EXACT, mode="lines", name="exact log loss", line=dict(color=BLUE, width=5)))
    fig.add_trace(go.Scatter(x=W, y=para, mode="lines", line=dict(color=RED, width=4, dash="dash"),
                             name="parabola" + (" + lambda w²/2" if lam else " touching at a")))
    fig.add_trace(go.Scatter(x=[w_exact], y=[L(w_exact)], mode="markers", name=f"exact minimum {w_exact:.2f}",
                             marker=dict(color=BLUE, size=16, symbol="diamond")))
    fig.add_trace(go.Scatter(x=[a], y=[L(a)], mode="markers+text", text=["a"], textposition="top right", showlegend=False,
                             marker=dict(color="black", size=16), textfont=dict(size=26)))
    ys = L(a) + G * (step - a) + 0.5 * (H + lam) * (step - a) ** 2
    fig.add_trace(go.Scatter(x=[step], y=[ys], mode="markers+text", text=[f"w* = {step:.2f}"],
                             textposition="bottom center", showlegend=False, textfont=dict(size=26, color=RED),
                             marker=dict(color=RED, size=18, symbol="star")))
    fig.update_xaxes(range=[-3, 1.5], title="leaf output w (log-odds)")
    fig.update_yaxes(range=[0.4, 6.2], title="log loss of the leaf")
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=90, r=20, t=90, b=75),
                      legend=dict(x=0.3, y=0.98, bgcolor="rgba(255,255,255,0.85)"))
    return fig


if __name__ == "__main__":
    seq = [(0.0, 0.0, "touch the loss at a = 0: w* = -G/H = -1.11")] * 10
    path = np.r_[np.linspace(0, 1.2, 9)[1:], np.linspace(1.2, -2.4, 19)[1:], np.linspace(-2.4, 0, 13)[1:]]
    seq += [(a, 0.0, "move a: the parabola always touches at a") for a in path]
    seq += [(0.0, 0.0, "close to a, parabola and loss agree")] * 8
    lams = np.r_[np.linspace(0, 3, 13)[1:]]
    seq += [(0.0, l, f"lambda = {l:.2f}: w* = -0.8 / (0.72 + {l:.2f})") for l in lams]
    seq += [seq[-1]] * 10
    tmp = HERE / ".newton_frames"
    tmp.mkdir(exist_ok=True)
    done = {}
    for k, s in enumerate(seq):
        if s in done:
            shutil.copy(tmp / f"{done[s]:03d}.png", tmp / f"{k:03d}.png")
        else:
            frame(*s).write_image(tmp / f"{k:03d}.png")
            done[s] = k
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "newton_leaf.gif")], check=True)
    pick = [0, 10 + 7, 10 + 25, len(seq) - 1]               # a = 0, a = 1.2, a = -2.4, lambda = 3
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in pick]
    w_, h_ = ims[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "newton_leaf_frames.png")
    shutil.rmtree(tmp)
