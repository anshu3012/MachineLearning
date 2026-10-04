"""The perceptron trick pick by pick on Iris setosa vs versicolor (petal length, petal width, learning rate 0.1):
the same run as stopping_rules.py. The picked point is ringed; the line moves only when that point is misclassified.
Run: python trick_iris.py -> trick_iris.gif, trick_iris_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
iris = load_iris()
keep = iris.target < 2
P = iris.data[keep, 2:4]
X = np.c_[np.ones(keep.sum()), P]                               # column of 1s carries the bias
y = iris.target[keep].astype(float)
w, rng, steps = np.ones(3), np.random.default_rng(0), []
while True:                                                     # identical to run(0, 1) in stopping_rules.py
    i = rng.integers(len(y))
    wrong = float(X[i] @ w >= 0) != y[i]
    w = w + 0.1 * (y[i] - float(X[i] @ w >= 0)) * X[i]
    steps.append((i, wrong, w.copy(), int(((X @ w >= 0) != y).sum())))
    if steps[-1][3] == 0:
        break
assert len(steps) == 146                                        # the loop count quoted in the Note
MOVED = sum(s[1] for s in steps)
assert all((s[2] == steps[k - 1][2]).all() for k, s in enumerate(steps) if k and not s[1])   # correct pick: line stays


def frame(k):
    i, wrong, w, miss = steps[k]
    fig = go.Figure()
    for cls, col, name in ((0, BLUE, "setosa (0)"), (1, ORANGE, "versicolor (1)")):
        fig.add_trace(go.Scatter(x=P[y == cls, 0], y=P[y == cls, 1], mode="markers", name=name,
                                 marker=dict(color=col, size=11, opacity=0.8)))
    xs = np.array([-3.0, 6.0])
    fig.add_trace(go.Scatter(x=xs, y=-(w[0] + w[1] * xs) / w[2], mode="lines", line=dict(color="black", width=4),
                             name="decision boundary"))
    col = RED if wrong else GREEN
    fig.add_trace(go.Scatter(x=[P[i, 0]], y=[P[i, 1]], mode="markers", showlegend=False,
                             marker=dict(size=30, color="rgba(0,0,0,0)", line=dict(color=col, width=5))))
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"pick {k + 1}: <span style='color:{col}'><b>"
                                      f"{'misclassified, the line moves' if wrong else 'correct, the line stays'}</b></span>"
                                      f"<br>misclassified points now: <b>{miss}</b>", x=0.5),
                      xaxis=dict(title="petal length (cm)", range=[-2, 5.5]), yaxis=dict(title="petal width (cm)", range=[-1.6, 2.3]),
                      legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=20, t=120, b=70))
    return fig


if __name__ == "__main__":
    print("picks:", len(steps), " picks that moved the line:", MOVED)
    tmp = HERE / ".ti_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(len(steps)):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(len(steps), len(steps) + 16):
        shutil.copy(tmp / f"{len(steps) - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "trick_iris.gif")], check=True)
    moved = [k for k, s in enumerate(steps) if s[1]]
    stay = next(k for k, s in enumerate(steps) if not s[1] and k > moved[2])
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (moved[2], stay, moved[len(moved) // 2], len(steps) - 1)]
    wd, h = keys[0].size
    sheet = Image.new("RGB", (2 * wd + 16, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (wd + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "trick_iris_frames.png")
    shutil.rmtree(tmp)
