"""KNN prediction step by step: a circle grows around one test tumour until it holds k = 5 training tumours,
then the 5 neighbours vote. Same data as the Note: breast cancer, mean radius and mean texture, scaled.
The query is the first test tumour whose 5-neighbour vote is split 3 to 2, so the vote is visible.
Run: python knn_vote.py  -> knn_vote.gif, knn_vote_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, NAMES, X_test, X_train, y_train

K = 5
sc = StandardScaler().fit(X_train)                       # KNN in the Note runs on scaled features
A, Q = sc.transform(X_train), sc.transform(X_test)
for q in Q:                                              # first test tumour with a 3-2 vote
    d = np.linalg.norm(A - q, axis=1)
    near = np.argsort(d)[:K]
    if sorted(np.bincount(y_train[near], minlength=2)) == [2, 3]:
        break
votes = np.bincount(y_train[near], minlength=2)
winner = int(votes.argmax())
R = d[near[-1]]                                          # radius that just holds k points
assert (d < R).sum() == K - 1 and (d <= R).sum() == K
print("query (scaled):", q.round(2), "votes malignant/benign:", votes, "->", NAMES[winner])

W = 2.2 * R                                        # zoom window around the query
GROW = 16
radii = np.r_[np.linspace(0, R, GROW)[1:], [R] * 3]      # circle grows, then the vote frames
th = np.linspace(0, 2 * np.pi, 120)


def frame(i):
    r = radii[min(i, len(radii) - 1)]
    voting = i >= GROW - 1
    caught = near[d[near] <= r + 1e-9]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.12,
                        subplot_titles=("", "votes"))
    for c in (0, 1):
        m = y_train == c
        fig.add_trace(go.Scatter(x=A[m, 0], y=A[m, 1], mode="markers", name=NAMES[c],
                                 marker=dict(color=COLOURS[c], size=13, opacity=0.55)), 1, 1)
    fig.add_trace(go.Scatter(x=q[0] + r * np.cos(th), y=q[1] + r * np.sin(th), mode="lines", showlegend=False,
                             line=dict(color="black", width=2, dash="dash")), 1, 1)
    qc = COLOURS[winner] if i >= GROW + 1 else "white"
    fig.add_trace(go.Scatter(x=[q[0]], y=[q[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=30, color=qc, line=dict(color="black", width=2))), 1, 1)
    fig.add_trace(go.Scatter(x=A[caught, 0], y=A[caught, 1], mode="markers", showlegend=False,
                             marker=dict(color=[COLOURS[c] for c in y_train[caught]], size=19,
                                         line=dict(color="black", width=3))), 1, 1)
    tally = np.bincount(y_train[caught], minlength=2)
    fig.add_trace(go.Bar(x=["malig-<br>nant", "benign"], y=tally, marker_color=[COLOURS[0], COLOURS[1]],
                         text=tally, textposition="outside", textfont=dict(size=26), showlegend=False), 1, 2)
    if i >= GROW + 1:
        title = f"prediction: <b>{NAMES[winner]}</b> ({votes[winner]} votes to {votes[1 - winner]})"
    elif voting:
        title = f"{K} neighbours caught: they vote"
    else:
        title = f"circle grows: {len(caught)} of {K} neighbours"
    fig.update_xaxes(range=[q[0] - W, q[0] + W], title="mean radius (scaled)", row=1, col=1)
    fig.update_yaxes(range=[q[1] - W, q[1] + W], title="mean texture (scaled)", scaleanchor="x", row=1, col=1)
    fig.update_annotations(font_size=24)
    fig.update_yaxes(range=[0, K + 0.8], showticklabels=False, row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=80, r=20, t=110, b=70),
                      legend=dict(orientation="h", x=0, y=1.0, yanchor="bottom"))
    return fig


def save(frames, name, keys, fps=4, hold=8):
    tmp = HERE / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    for k, f in enumerate(frames):
        f.write_image(tmp / f"{k:03d}.png")
    n = len(frames)
    for k in range(n, n + hold):                         # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    n = GROW + 2
    save([frame(i) for i in range(n)], "knn_vote", keys=(3, 9, GROW - 1, n - 1))
