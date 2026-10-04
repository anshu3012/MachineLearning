"""What the second hidden layer receives during training, with and without batch normalisation (data from the
Notebook, data/passed_on.csv.gz: seed 0 of both circles models, all 500 rows, after every epoch). Each dot is one
observation's value at one of the 3 nodes; the bar is mean +- one standard deviation, the grey bar the same at the
start. Without batch normalisation the values drift and spread; with it they stay centred, as gamma and beta allow.
Run: python drift.py  -> drift.gif, drift_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, GREEN

HERE = Path(__file__).parent
P = pd.read_csv(HERE.parent / "data" / "passed_on.csv.gz")
NODES = ["node1", "node2", "node3"]
SIDES = ((False, "without batch normalisation", BLUE), (True, "with batch normalisation", GREEN))
JITTER = np.random.default_rng(0).uniform(-0.28, 0.28, (500, 3))     # fixed per dot, so each dot keeps its row
EPOCHS = list(range(0, 201, 4))
XR = [-2.2, 5.0]                                                    # one scale for both panels


def values(bn, epoch):
    return P[(P.bn == bn) & (P.epoch == epoch)][NODES].to_numpy()


def frame(epoch):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=[s[1] for s in SIDES])
    for col, (bn, _, c) in enumerate(SIDES, start=1):
        v, v0 = values(bn, epoch), values(bn, 0)
        for j in range(3):
            y = 3 - j
            for w, colour, lw in ((v0[:, j], "#C8C8C8", 10), (v[:, j], c, 6)):
                m, s = w.mean(), w.std()
                fig.add_trace(go.Scatter(x=[m - s, m + s], y=[y - 0.42] * 2, mode="lines", line=dict(color=colour, width=lw),
                                         showlegend=False), row=1, col=col)
            fig.add_trace(go.Scatter(x=[v[:, j].mean()], y=[y - 0.42], mode="markers", showlegend=False,
                                     marker=dict(symbol="diamond", size=15, color=c)), row=1, col=col)
            fig.add_trace(go.Scatter(x=v[:, j], y=y + JITTER[:, j], mode="markers", showlegend=False,
                                     marker=dict(size=5, color=c, opacity=0.5)), row=1, col=col)
        fig.update_xaxes(range=XR, title_text="value passed to layer 2", row=1, col=col)
        fig.update_yaxes(range=[0.4, 3.45], tickvals=[3, 2, 1], ticktext=["node 1", "node 2", "node 3"] if col == 1 else
                         ["", "", ""], ticks="", row=1, col=col)
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"epoch {epoch}", x=0.5, y=0.96, font=dict(size=30)),
                      margin=dict(l=100, r=30, t=120, b=80))
    fig.update_annotations(font=dict(size=24))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".drift_frames"
    tmp.mkdir(exist_ok=True)
    seq = []
    for e in EPOCHS:
        p = tmp / f"{e:03d}.png"
        frame(e).write_image(p)
        seq.append((p, 15 if e == 0 else 1.5))
    seq[-1] = (seq[-1][0], 40)
    with open(tmp / "list.txt", "w") as f:
        for p, t in seq:
            f.write(f"file '{p.name}'\nduration {t / 10}\n")
        f.write(f"file '{seq[-1][0].name}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", str(tmp / "list.txt"), "-vf",
                    "fps=10,scale=680:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "drift.gif")], check=True)
    ims = [Image.open(tmp / f"{e:03d}.png").convert("RGB") for e in (0, 20, 100, 200)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "drift_frames.png")
    shutil.rmtree(tmp)
