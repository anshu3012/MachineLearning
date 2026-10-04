"""Batch, mini-batch (10) and stochastic gradient descent race on the 100-point example (m and b), same start,
same learning rate 0.05 as the Note's Figure 1. Fair race: every frame, each method reads the same 10 observations' worth
of data, so SGD makes 10 updates, mini-batch 1, and batch 1 only every 10 frames (after reading all 100).
Left: paths on the loss contours. Right: loss (mean squared error) against observations read.
One script, three Notes (58, 59, 60): the GIF and the frame grid are copied into each Note's images/.
Run: python gd_race.py  -> gd_race.gif, gd_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_regression

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1, noise=20, random_state=13)
x = X.ravel(); n = len(x)
best_m, best_b = np.polyfit(x, y, 1)
mse = lambda p: np.mean((y - p[0] * x - p[1]) ** 2)
EPOCHS, PER_FRAME = 3, 10                                  # 10 observations read per frame -> 30 frames


def run(batch_size, lr=0.05, seed=2, m=-127.82, b=150.0):
    rng = np.random.default_rng(seed); path = [(m, b)]
    for _ in range(EPOCHS):
        idx = rng.permutation(n)
        for s in range(0, n, batch_size):
            j = idx[s:s + batch_size]; err = y[j] - m * x[j] - b
            m, b = m + lr * 2 * np.mean(err * x[j]), b + lr * 2 * np.mean(err)
            path.append((m, b))
    return np.array(path)


RUNNERS = [("batch (all 100)", n, RED), ("mini-batch of 10", 10, GREEN), ("stochastic (1)", 1, ORANGE)]
PATHS = {name: run(bs) for name, bs, _ in RUNNERS}
LOSS = {name: np.array([mse(p) for p in P]) for name, P in PATHS.items()}
FRAMES = EPOCHS * n // PER_FRAME
mg, bg = np.linspace(-150, 150, 120), np.linspace(-150, 170, 120)
Z = np.array([[np.mean((y - mm * x - bb) ** 2) for mm in mg] for bb in bg])


def upto(bs, k):
    """Updates made after reading k * PER_FRAME observations."""
    return k * PER_FRAME // bs


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.11,
                        subplot_titles=["paths on the loss contours", "loss against data read"])
    fig.add_trace(go.Contour(x=mg, y=bg, z=Z, colorscale="Blues", reversescale=True, showscale=False, ncontours=20,
                             line=dict(width=0.4), opacity=0.5), 1, 1)
    obs = np.arange(FRAMES + 1) * PER_FRAME
    for name, bs, c in RUNNERS:
        u = upto(bs, k)
        P = PATHS[name][:u + 1]
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=c, width=3 if bs > 1 else 2),
                                 marker=dict(size=10 if bs == n else (6 if bs == 10 else 3), color=c),
                                 name=f"{name}: {u} update{'' if u == 1 else 's'}"), 1, 1)
        L = LOSS[name][[upto(bs, j) for j in range(k + 1)]]
        fig.add_trace(go.Scatter(x=obs[:k + 1], y=L, mode="lines", line=dict(color=c, width=4), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[best_m], y=[best_b], mode="markers", marker=dict(size=16, color="black", symbol="x"),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[0, EPOCHS * n], y=[mse((best_m, best_b))] * 2, mode="lines", showlegend=False,
                             line=dict(color="black", dash="dot", width=2)), 1, 2)
    fig.add_annotation(x=5, y=np.log10(mse((best_m, best_b))), xref="x2", yref="y2", text="best possible loss",
                       showarrow=False, yshift=-15, xanchor="left", font=dict(size=18))
    fig.update_xaxes(title="m", range=[-150, 150], row=1, col=1)
    fig.update_yaxes(title="b", range=[-150, 170], row=1, col=1)
    fig.update_xaxes(title="observations read", range=[0, EPOCHS * n], row=1, col=2)
    fig.update_yaxes(title="loss (log scale)", type="log", range=[2.28, 4.7], tickvals=[300, 1000, 3000, 10000, 30000],
                     ticktext=["300", "1k", "3k", "10k", "30k"], row=1, col=2)
    seen = k * PER_FRAME
    fig.update_layout(template="simple_white", width=1200, height=680, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"observations read: {seen}  (epoch {seen / n:.1f})", x=0.5, y=0.98, font=dict(size=26)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14, font=dict(size=21)),
                      margin=dict(l=70, r=30, t=100, b=140))
    fig.update_annotations(selector=dict(text="paths on the loss contours"), font_size=22)
    fig.update_annotations(selector=dict(text="loss against data read"), font_size=22)
    return fig


# Checks that the race shows what the three Notes teach.
end = {name: P[-1] for name, P in PATHS.items()}
dist = lambda p: float(np.hypot(p[0] - best_m, p[1] - best_b))
assert len(PATHS["batch (all 100)"]) - 1 == EPOCHS and len(PATHS["stochastic (1)"]) - 1 == EPOCHS * n
assert dist(end["batch (all 100)"]) > 5 * dist(end["mini-batch of 10"])          # batch has barely started
sgd_tail = PATHS["stochastic (1)"][-100:]; mb_tail = PATHS["mini-batch of 10"][-10:]
jit = lambda P: float(np.hypot(*(np.diff(P, axis=0).T)).sum() / np.hypot(*(P[-1] - P[0])))   # path length / net move
assert jit(sgd_tail) > 3 * jit(mb_tail), (jit(sgd_tail), jit(mb_tail))           # last epoch: SGD zigzags, mini-batch smooth
print("end distance to minimum:", {k: round(dist(v), 1) for k, v in end.items()},
      "| last epoch path length / net move: SGD", round(jit(sgd_tail), 2), "mini-batch", round(jit(mb_tail), 2))

if __name__ == "__main__":
    tmp = HERE / ".race_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(FRAMES + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(FRAMES + 1, FRAMES + 9):                  # hold the last frame
        shutil.copy(tmp / f"{FRAMES:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gd_race.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (1, 5, 10, FRAMES)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "gd_race_frames.png")
    shutil.rmtree(tmp)
    for note in ("58-batch-gradient-descent", "59-stochastic-gradient-descent"):
        for f in ("gd_race.gif", "gd_race_frames.png"):
            shutil.copy(HERE / f, ROOT / note / "images" / f)
