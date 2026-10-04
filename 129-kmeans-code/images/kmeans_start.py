"""What fit_predict does on the 200 students, k = 4, without scaling (as in the Note): a k-means++ start (plain
version of Arthur and Vassilvitskii 2007; scikit-learn runs a greedy variant of it), then assign / update rounds
until no student changes cluster. Each new start centroid is a student drawn with probability proportional to
its squared distance from the nearest centroid chosen so far (shown as marker size).
Also checks the first rows and labels drawn in boolean_index.tex.
Run: python kmeans_start.py  -> kmeans_start.gif, kmeans_start_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.cluster import KMeans

HERE = Path(__file__).parent
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
GREY = "#9A9A9A"
df = pd.read_csv(HERE.parent / "data" / "student_clustering.csv")
X = df.values
K = 4

# the numbers boolean_index.tex draws: first five students and their labels from the Note's code
y_means = KMeans(n_clusters=4, random_state=0).fit_predict(X)
assert list(y_means[:5]) == [3, 2, 1, 1, 2]
assert np.allclose(X[:5], [[5.13, 88], [5.90, 113], [8.36, 93], [8.27, 97], [5.45, 110]])

# k-means++ start, step by step
rng = np.random.default_rng(3)
cents, steps = [X[rng.integers(len(X))]], []
while True:
    d2 = ((X[:, None, :] - np.array(cents)[None]) ** 2).sum(-1).min(1)
    prob = d2 / d2.sum()                                   # chance of each student to be the next centroid
    if len(cents) == K:
        steps.append(("start: 4 centroids, one per group", np.array(cents), None, None))
        break
    steps.append((f"{len(cents)} centroid{'s' if len(cents) > 1 else ''}: dot size = chance to be the next one",
                  np.array(cents), prob, None))
    cents.append(X[rng.choice(len(X), p=prob)])
C = np.array(cents, dtype=float)
rounds = 0
while True:
    lab = ((X[:, None, :] - C[None]) ** 2).sum(-1).argmin(1)
    rounds += 1
    steps.append((f"round {rounds}, assign: each student joins its nearest centroid", C.copy(), None, lab))
    newC = np.array([X[lab == k].mean(0) for k in range(K)])
    if np.allclose(newC, C):
        steps[-1] = (f"no student moves: done after {rounds} rounds, 4 clusters of 50", C.copy(), None, lab)
        break
    C = newC
    steps.append((f"round {rounds}, update: each centroid moves to the mean of its students", C.copy(), None, lab))
order = np.argsort(-C[:, 0] * 1000 - C[:, 1])                         # fixed colour order, as in Figure 1
assert all(np.bincount(lab) == 50)
ref = np.array([[8.87, 117.2], [8.20, 94.6], [5.89, 109.5], [4.97, 86.7]])
assert np.allclose(np.array(sorted(C.tolist(), key=lambda c: (-c[0], -c[1]))), ref, atol=0.05)
print("rounds:", rounds, "centroids:", C.round(2))
colour = {k: COLS[i] for i, k in enumerate(order)}


def frame(title, C, prob, lab):
    fig = go.Figure()
    if lab is None:
        size = 7 if prob is None else 4 + 900 * prob
        fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", showlegend=False,
                                 marker=dict(color=GREY, size=np.clip(size, 5, 26), line=dict(width=0))))
    else:
        for k in range(K):
            m = lab == k
            fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                                     marker=dict(color=colour[k] if len(C) == K else GREY, size=8)))
    fig.add_trace(go.Scatter(x=C[:, 0], y=C[:, 1], mode="markers", showlegend=False,
                             marker=dict(color=[colour[k] for k in range(len(C))] if lab is not None else "black",
                                         size=24, symbol="x", line=dict(width=2, color="black"))))
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=24)),
                      xaxis=dict(title="CGPA", range=[4.3, 9.6]), yaxis=dict(title="IQ", range=[80, 124]),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".kmeans_frames"
    tmp.mkdir(exist_ok=True)
    n, shots = 0, {}
    keys = [1, len(steps) - 1]
    for k, (title, C, prob, lab) in enumerate(steps):
        frame(title, C, prob, lab).write_image(tmp / "src.png")
        for _ in range(16 if k == len(steps) - 1 else 7):
            shutil.copy(tmp / "src.png", tmp / f"{n:03d}.png"); n += 1
        if k in keys:
            shots[k] = Image.open(tmp / "src.png").convert("RGB")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "kmeans_start.gif")], check=True)
    ims = [shots[k] for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")                # side by side: square-ish frames
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "kmeans_start_frames.png")
    shutil.rmtree(tmp)
