"""Why a hidden layer solves XOR. Two hidden perceptrons, h1 = step(x1 + x2 - 0.5) (the OR line of section 4) and
h2 = step(x1 + x2 - 1.5) (the AND line), move the four XOR observations to new positions (h1, h2). There the two
classes are linearly separable: the output perceptron step(h1 - h2 - 0.5) gets all four right. Frames slide the
points from the input square to the hidden square. Plotly frames -> ffmpeg GIF, plus a grid for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED, BLUE, PURPLE = "#54A24B", "#E45756", "#4C78A8", "#B279A2"
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
y = np.array([0, 1, 1, 0])
step = lambda z: (z >= 0).astype(float)
H = np.c_[step(X.sum(1) - 0.5), step(X.sum(1) - 1.5)]
out = step(H[:, 0] - H[:, 1] - 0.5)
assert (out == y).all() and H.tolist() == [[0, 0], [1, 0], [1, 0], [1, 1]]
JIT = np.array([[0, 0], [-0.04, 0.04], [0.04, -0.04], [0, 0]])     # keep the two (1, 0) points visible
T = np.linspace(0, 1, 9)


def frame(t, stage):
    P = (1 - t) * X + t * (H + JIT)
    fig = go.Figure()
    if stage == 0:
        xs = np.array([-0.3, 1.3])
        fig.add_scatter(x=xs, y=0.5 - xs, mode="lines", line=dict(color=BLUE, width=4, dash="dash"), name="h₁ line: x₁ + x₂ = 0.5")
        fig.add_scatter(x=xs, y=1.5 - xs, mode="lines", line=dict(color=PURPLE, width=4, dash="dash"), name="h₂ line: x₁ + x₂ = 1.5")
    if stage == 2:
        hs = np.array([-0.3, 1.3])
        fig.add_scatter(x=hs, y=hs - 0.5, mode="lines", line=dict(color="black", width=5), name="output line: h₁ − h₂ = 0.5")
    for lab, c, name in ((1, GREEN, "XOR = 1"), (0, RED, "XOR = 0")):
        m = y == lab
        fig.add_scatter(x=P[m, 0], y=P[m, 1], mode="markers+text", name=name, marker=dict(size=30, color=c),
                        text=[f"({int(a)},{int(b)})" for a, b in X[m]], textposition="top center", textfont=dict(size=18))
    axis = ("x₁", "x₂") if t == 0 else ("h₁", "h₂") if t == 1 else ("", "")
    title = ["Input space: no single line separates the green and red corners",
             "The hidden perceptrons move each corner to (h₁, h₂)",
             "Hidden space: (0,1) and (1,0) land on the same spot; one line now separates the classes"][stage]
    fig.update_layout(template="simple_white", width=900, height=820, font=FONT,
                      title=dict(text=title, x=0.5, y=0.96, font=dict(size=20)),
                      xaxis=dict(title=axis[0], range=[-0.3, 1.3], tickvals=[0, 1]),
                      yaxis=dict(title=axis[1], range=[-0.3, 1.3], tickvals=[0, 1], scaleanchor="x"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12, font=dict(size=17)),
                      margin=dict(l=80, r=30, t=80, b=150))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".xr_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(0, 0)] * 5 + [(t, 1) for t in T[1:-1]] + [(1, 2)] * 7
    cache = {}
    for j, (t, st) in enumerate(seq):
        key = (round(t, 3), st)
        if key not in cache:
            cache[key] = tmp / f"c{len(cache)}.png"
            frame(t, st).write_image(cache[key])
        shutil.copy(cache[key], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "xor_remap.gif")], check=True)
    ims = [Image.open(cache[k]).convert("RGB") for k in ((0, 0), (1, 2))]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "xor_remap_frames.png")
    shutil.rmtree(tmp)
