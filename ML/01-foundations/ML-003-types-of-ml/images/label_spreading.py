"""Semi-supervised learning as a process: one hand-written label per group spreads to the unlabelled students through
their nearest neighbours (label propagation on a 5-nearest-neighbour graph, Zhu and Ghahramani 2002). Data: the
Note's example students (IQ and CGPA, the same 90 points as the clustering figure). At each step, every student adds up
its neighbours' labels and takes the strongest; the three hand labels never change.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.neighbors import NearestNeighbors

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
COL = ["#4C78A8", "#F58518", "#54A24B"]
NAMES = ["high IQ, high CGPA", "high IQ, low CGPA", "low IQ, high CGPA"]

rng = np.random.default_rng(11)                        # same example data as clustering.py
centres = [(120, 8.8), (118, 6.2), (85, 8.5)]
X = np.vstack([np.column_stack([rng.normal(i, 5, 30), rng.normal(c, 0.35, 30)]) for i, c in centres])
truth = np.repeat([0, 1, 2], 30)
Z = (X - X.mean(0)) / X.std(0)
seeds = [int(np.argmin(((Z - Z[truth == g].mean(0)) ** 2).sum(1))) for g in range(3)]   # one student per group

nn = NearestNeighbors(n_neighbors=6).fit(Z)
_, idx = nn.kneighbors(Z)
A = np.zeros((90, 90))
for i, row in enumerate(idx):
    A[i, row[1:]] = A[row[1:], i] = 1                  # symmetric 5-nearest-neighbour graph
F = np.zeros((90, 3))
F[seeds, [truth[s] for s in seeds]] = 1
states = [F.copy()]
while (F.sum(1) == 0).any():
    F = A @ F
    F = np.where(F.sum(1, keepdims=True) > 0, F / np.maximum(F.sum(1, keepdims=True), 1e-12), 0)
    F[seeds] = np.eye(3)[[truth[s] for s in seeds]]     # the hand labels stay fixed
    states.append(F.copy())
    assert len(states) < 40
final = states[-1].argmax(1)
assert (final == truth).mean() == 1.0                   # every student ends in its own group's label
STEPS = len(states) - 1


def frame(k):
    F = states[k]
    reached = F.sum(1) > 0
    fig = go.Figure()
    xs, ys = [], []
    for i in range(90):
        for j in np.nonzero(A[i])[0]:
            if j > i:
                xs += [X[i, 0], X[j, 0], None]; ys += [X[i, 1], X[j, 1], None]
    fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color="#DDDDDD", width=1), showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=X[~reached, 0], y=X[~reached, 1], mode="markers", name="no label yet",
                    marker=dict(size=13, color="white", line=dict(color="#9A9A9A", width=2)))
    for g in range(3):
        m = reached & (F.argmax(1) == g)
        fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=NAMES[g],
                        marker=dict(size=13, color=COL[g], line=dict(color="white", width=1)))
    fig.add_scatter(x=X[seeds, 0], y=X[seeds, 1], mode="markers", name="labelled by hand",
                    marker=dict(symbol="star", size=30, color=[COL[truth[s]] for s in seeds],
                                line=dict(color="black", width=2)))
    n = int(reached.sum())
    head = "Start: 3 students labelled by hand, 87 unlabelled" if k == 0 else \
        f"Step {k}: {n} of 90 students have a label"
    fig.update_layout(template="simple_white", width=1000, height=760, font=FONT,
                      title=dict(text=head, x=0.5, y=0.96),
                      xaxis=dict(title="IQ", range=[70, 135]), yaxis=dict(title="CGPA", range=[5.2, 9.9]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14, font=dict(size=18)),
                      margin=dict(l=80, r=30, t=80, b=150))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ls_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(STEPS + 1):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [0] * 4 + [k for k in range(1, STEPS + 1) for _ in range(2)] + [STEPS] * 6
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "label_spreading.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (0, 2)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "label_spreading_frames.png")
    shutil.rmtree(tmp)
    print("steps:", STEPS, "reached per step:", [int((s.sum(1) > 0).sum()) for s in states])
