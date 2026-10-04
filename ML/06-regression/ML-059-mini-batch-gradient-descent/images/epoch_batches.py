"""Three epochs of mini-batch gradient descent, batch size 10, on the 100-point example of Figure 1 (same data, start,
learning rate 0.05 and shuffle seed as gd_race.py). Each epoch starts with a new shuffle; each frame: one batch of 10 lights up, and the line moves once,
using the derivative averaged over those 10 observations only. Bottom strip: the shuffled order cut into 10 batches.
Run: python epoch_batches.py  -> epoch_batches.gif, epoch_batches_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from gd_race import x, y, n, run, mse, best_m, best_b

HERE = Path(__file__).parent
GREEN, GREY, LIGHT, BLACK = "#54A24B", "#B0B0B0", "#E4E4E4", "#222222"
TEN = ["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#54A24B", "#EECA3B", "#B279A2", "#FF9DA6", "#9D755D", "#BAB0AC"]
BS = 10
EPOCHS, NB = 3, n // BS
rng = np.random.default_rng(2)
orders = [rng.permutation(n) for _ in range(EPOCHS)]          # the shuffles run() makes (seed 2), one per epoch
path = run(BS)                                                # start + 30 updates = the green runner of Figure 1
# Check: redoing the updates by hand from the batches drawn here gives the same coefficients.
m, b = path[0]
for e in range(EPOCHS):
    for k in range(NB):
        j = orders[e][k * BS:(k + 1) * BS]; err = y[j] - m * x[j] - b
        m, b = m + 0.05 * 2 * np.mean(err * x[j]), b + 0.05 * 2 * np.mean(err)
        assert np.allclose((m, b), path[e * NB + k + 1])
L = [mse(p) for p in path]
assert len(path) == EPOCHS * NB + 1 and L[-1] < L[0] / 50     # 30 small updates take the loss down fiftyfold
print("loss start", round(L[0]), "after each epoch", [round(L[e * NB]) for e in (1, 2, 3)], "best", round(mse((best_m, best_b))))
xs = np.array([x.min() - 0.3, x.max() + 0.3])


def frame(e, k):
    """Epoch e (0-based); k = batches of this epoch already used (0..10)."""
    order, u = orders[e], e * NB + k                         # u = updates made so far
    fig = make_subplots(2, 1, row_heights=[0.8, 0.2], vertical_spacing=0.1)
    cur = order[(k - 1) * BS:k * BS] if k else np.array([], int)
    batch_of = np.empty(n, int); batch_of[order] = np.arange(n) // BS   # which batch each observation landed in
    dot = [TEN[g] for g in batch_of] if k == 0 else GREY                 # new shuffle: colour every point by its batch
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=11 if k == 0 else 8, color=dot),
                             showlegend=False), 1, 1)
    if k:
        fig.add_trace(go.Scatter(x=x[cur], y=y[cur], mode="markers", name=f"batch {k}: 10 observations",
                                 marker=dict(size=15, color=GREEN, line=dict(color="white", width=1.5))), 1, 1)
        pm, pb = path[u - 1]
        fig.add_trace(go.Scatter(x=xs, y=pm * xs + pb, mode="lines", name="line before this update",
                                 line=dict(color=GREY, width=3, dash="dash")), 1, 1)
    cm, cb = path[u]
    fig.add_trace(go.Scatter(x=xs, y=cm * xs + cb, mode="lines", name=f"line after {u} update{'' if u == 1 else 's'}",
                             line=dict(color=BLACK, width=4)), 1, 1)
    # the shuffled order, cut into 10 batches
    if k == 0:
        state = [TEN[i // BS] for i in range(n)]
    else:
        state = [GREEN if i // BS == k - 1 else (LIGHT if i // BS >= k else "#B5DBB0") for i in range(n)]
    fig.add_trace(go.Scatter(x=np.arange(n), y=np.zeros(n), mode="markers", showlegend=False,
                             marker=dict(symbol="square", size=16, color=state)), 2, 1)
    for s in range(BS, n, BS):
        fig.add_shape(type="line", x0=s - 0.5, x1=s - 0.5, y0=-0.6, y1=0.6, line=dict(color="white", width=6), layer="above", row=2, col=1)
    fig.update_xaxes(title="x", row=1, col=1, range=list(xs))
    fig.update_yaxes(title="y", row=1, col=1, range=[-200, 330])
    fig.update_xaxes(row=2, col=1, range=[-1, n], showticklabels=False, showline=False, ticks="",
                     title="shuffled observations, cut into 10 batches of 10")
    fig.update_yaxes(row=2, col=1, visible=False, range=[-1, 1])
    head = "new shuffle: colour = batch" if k == 0 else f"batch {k} of 10"
    fig.update_layout(template="simple_white", width=1000, height=760, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"epoch {e + 1} · {head} · loss {L[u]:,.0f}", x=0.5, y=0.97, font=dict(size=26)),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)", font=dict(size=20)),
                      margin=dict(l=70, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".epoch_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(e, k) for e in range(EPOCHS) for k in range(NB + 1)]
    for i, (e, k) in enumerate(seq):
        frame(e, k).write_image(tmp / f"{i:03d}.png")
    last = len(seq) - 1
    for i in range(last + 1, last + 7):                       # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "epoch_batches.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, NB + 1, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "epoch_batches_frames.png")
    shutil.rmtree(tmp)
