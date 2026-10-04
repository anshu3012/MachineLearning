"""Gradient boosting for classification on the Note's eight students, stage by stage: each student's probability
of placement (dot) moves towards its class (ring at 0 or 1); the red bar is the pseudo-residual y - p that the
next tree learns. Learning rate 1, trees with 3 leaves, random_state=0, exactly as the Notebook (stages 1-3),
then two more trees. Right: average log loss per stage.
Run: python prob_climb.py  -> prob_climb.gif, prob_climb_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
df = pd.read_csv(HERE.parent / "data" / "placement8.csv")
X, y = df[["cgpa", "iq"]].values, df["placed"].values
sig = lambda z: 1 / (1 + np.exp(-z))
TREES = 4

F = [np.full(len(y), np.log(y.sum() / (1 - y).sum()))]       # stage 1: ln(5/3) for everyone
for _ in range(TREES):
    p = sig(F[-1])
    r = y - p
    leaf = DecisionTreeRegressor(max_leaf_nodes=3, random_state=0).fit(X, r).apply(X)
    gamma = {j: r[leaf == j].sum() / (p[leaf == j] * (1 - p[leaf == j])).sum() for j in np.unique(leaf)}
    F.append(F[-1] + np.array([gamma[j] for j in leaf]))
P = [sig(f) for f in F]
loss = [-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)) for p in P]
assert np.allclose(P[2].round(2), [0.21, 0.04, 0.82, 0.40, 0.90, 0.74, 0.74, 0.95])   # the Note's stage 3 table
assert np.allclose(np.round(loss[:3], 2), [0.66, 0.31, 0.22]) and all(np.diff(loss) < 0)
print("log loss per stage:", np.round(loss, 3))

SUB = 6                                                         # in-between frames per tree (in log-odds)
students = np.arange(1, 9)


def frame(s, u):
    """Stage s (0 = F0), u in [0, 1]: part of the way to stage s + 1."""
    f = F[s] + u * (F[min(s + 1, TREES)] - F[s])
    p = sig(f)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.66, 0.34], horizontal_spacing=0.12,
                        subplot_titles=("", "average log loss"))
    for i in range(8):
        fig.add_shape(type="line", x0=students[i], x1=students[i], y0=p[i], y1=y[i], line=dict(color=RED, width=6),
                      opacity=0.55, row=1, col=1)
    fig.add_hline(y=0.5, line=dict(color="black", dash="dot", width=2), row=1, col=1)
    cols = [BLUE if c else ORANGE for c in y]          # blue = placed, as in Figure 5
    fig.add_trace(go.Scatter(x=students, y=y, mode="markers", name="true class",
                             marker=dict(symbol="circle-open", size=26, color=cols, line=dict(width=3))), 1, 1)
    fig.add_trace(go.Scatter(x=students, y=p, mode="markers", name="probability p",
                             marker=dict(size=20, color=cols, line=dict(color="black", width=1.5))), 1, 1)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="residual y - p", line=dict(color=RED, width=6)), 1, 1)
    done = s + (u >= 1)
    fig.add_trace(go.Scatter(x=list(range(1, done + 2)), y=loss[:done + 1], mode="lines+markers", showlegend=False,
                             line=dict(color="black", width=3), marker=dict(size=11)), 1, 2)
    title = ("stage 1: everyone starts at ln(5/3), p = 0.62" if done == 0 else
             f"stage {done + 1}: after {done} tree{'s' if done > 1 else ''}" if u in (0, 1) else
             f"tree {s + 1} pushes the log-odds")
    fig.update_xaxes(range=[0.4, 8.6], tickvals=students, title="student", row=1, col=1)
    fig.update_yaxes(range=[-0.08, 1.08], title="probability of placed", row=1, col=1)
    fig.update_xaxes(range=[0.6, TREES + 1.4], dtick=1, title="stage", row=1, col=2)
    fig.update_yaxes(range=[0, 0.7], row=1, col=2)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=80, r=20, t=120, b=60),
                      legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".climb_frames"
    tmp.mkdir(exist_ok=True)
    seq, keys = [], []
    for s in range(TREES + 1):
        keys.append(len(seq))
        seq += [(s, 0.0)] * 8                                    # hold each stage
        if s < TREES:
            seq += [(s, (j / SUB) ** 0.7) for j in range(1, SUB)]
    seq += [(TREES, 0.0)] * 10
    cache = {}
    for k, su in enumerate(seq):
        if su not in cache:
            frame(*su).write_image(tmp / f"{k:03d}.png")
            cache[su] = k
        else:
            shutil.copy(tmp / f"{cache[su]:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "10", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "prob_climb.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[i]:03d}.png").convert("RGB") for i in (0, 1, 2, TREES)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "prob_climb_frames.png")
    shutil.rmtree(tmp)
