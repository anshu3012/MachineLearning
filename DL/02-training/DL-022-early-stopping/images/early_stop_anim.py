"""Early stopping as it happens: training and validation loss drawn epoch by epoch with Keras' patience counter
(left) and the decision boundary at the same epoch (right). Part 1 stops at epoch 503 like EarlyStopping(patience=50,
min_delta=0.00001); part 2 lets the same run go on to 3,500 epochs. Data: data/history_3500.csv and
data/boundary_snapshots.npz from the Notebook. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, RED

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
h = pd.read_csv(DATA / "history_3500.csv")
snap = np.load(DATA / "boundary_snapshots.npz")
SNAP = {int(e): p for e, p in zip(snap["epochs"], snap["p"])}
pts = pd.read_csv(DATA / "points.csv")
FONT = dict(family="Latin Modern Roman", size=22)
PATIENCE, MIN_DELTA = 50, 1e-5

# Keras' rule: the counter restarts only when val_loss beats the best so far by more than min_delta
wait, best, best_epoch, stop = [], np.inf, 0, None
for ep, v in zip(h.epoch, h.val_loss):
    if v < best - MIN_DELTA:
        best, best_epoch, w = v, ep, 0
    else:
        w = wait[-1][0] + 1
    wait.append((w, best_epoch))
    if w >= PATIENCE and stop is None:
        stop = ep
assert stop == len(pd.read_csv(DATA / "history_early_stopping.csv")) == 503

xs = snap["xs"]


def frame(ep, part):
    w, b = wait[ep - 1]
    d = h[h.epoch <= ep]
    fig = make_subplots(1, 2, column_widths=[0.56, 0.44], horizontal_spacing=0.09,
                        subplot_titles=["loss", "decision boundary"])
    if part == 2:
        fig.add_scatter(x=[stop, stop], y=[0, 1.05], mode="lines", line=dict(color=RED, dash="dash", width=2),
                        showlegend=False, row=1, col=1)
        fig.add_annotation(x=stop, y=1.0, text="early stop", showarrow=False, xanchor="left", xshift=6,
                           font=dict(color=RED), row=1, col=1)
    fig.add_scatter(x=d.epoch, y=d.loss, mode="lines", name="training loss", line=dict(color=BLUE, width=3), row=1, col=1)
    fig.add_scatter(x=d.epoch, y=d.val_loss, mode="lines", name="validation loss", line=dict(color=ORANGE, width=3), row=1, col=1)
    if part == 1:
        fig.add_scatter(x=[b], y=[h.val_loss[b - 1]], mode="markers", marker=dict(color="black", size=12),
                        name="best so far", row=1, col=1)
        txt = f"patience {w} / {PATIENCE}" + ("<br><b>stop</b>" if ep == stop else "")
        fig.add_annotation(x=0.98, y=0.98, xref="x domain", yref="y domain", text=txt, showarrow=False,
                           xanchor="right", yanchor="top", font=dict(size=24, color=RED if w else GREY),
                           row=1, col=1)
    z = SNAP[ep].astype(float).reshape(len(xs), len(xs))
    fig.add_trace(go.Heatmap(x=xs, y=xs, z=(z > 0.5).astype(int), showscale=False, opacity=0.2, zmin=0, zmax=1,
                             colorscale=[[0, ORANGE], [1, BLUE]]), 1, 2)
    if z.min() < 0.5 < z.max():
        fig.add_trace(go.Contour(x=xs, y=xs, z=z, showscale=False, contours=dict(start=0.5, end=0.5, size=1,
                      coloring="lines"), colorscale=[[0, "black"], [1, "black"]], line=dict(width=3)), 1, 2)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        for s, sym in (("train", "circle"), ("validation", "x")):
            q = pts[(pts.y == cls) & (pts.set == s)]
            fig.add_scatter(x=q.x1, y=q.x2, mode="markers", showlegend=False, row=1, col=2,
                            marker=dict(color=c, size=9, symbol=sym,
                                        line=dict(width=1, color="white") if sym == "circle" else None))
    fig.update_xaxes(title="epoch", range=[0, 600 if part == 1 else 3500], row=1, col=1)
    fig.update_yaxes(title="loss", range=[0, 1.05], row=1, col=1)
    fig.update_xaxes(range=[-1.6, 1.6], visible=False, row=1, col=2)
    fig.update_yaxes(range=[-1.6, 1.6], visible=False, scaleanchor="x2", row=1, col=2)
    title = f"epoch {ep}" if part == 1 else f"without early stopping: epoch {ep:,}"
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(orientation="h", x=0, y=-0.18), margin=dict(l=70, r=20, t=90, b=40))
    fig.update_annotations(font_size=22)
    return fig


EPOCHS1 = [1] + list(range(20, 441, 20)) + [460, 469, 480, 500, 503]   # epochs with a boundary snapshot
EPOCHS2 = list(range(750, 3501, 250))
SEQ = [(e, 1) for e in EPOCHS1] + [(stop, 1)] * 8 + [(e, 2) for e in EPOCHS2] + [(3500, 2)] * 8
KEYS = [(200, 1), (480, 1), (stop, 1), (3500, 2)]

if __name__ == "__main__":
    tmp = HERE / ".es_frames"
    tmp.mkdir(exist_ok=True)
    made = {}
    for k, key in enumerate(SEQ):
        out = tmp / f"{k:03d}.png"
        if key in made:
            shutil.copy(made[key], out)
        else:
            frame(*key).write_image(out)
            made[key] = out
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "early_stop_anim.gif")], check=True)
    keys = [Image.open(made[k]).convert("RGB") for k in KEYS]
    w, hh = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * hh + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (hh + 16)))
    sheet.save(HERE / "early_stop_anim_frames.png")
    shutil.rmtree(tmp)
