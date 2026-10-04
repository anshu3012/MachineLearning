"""Training against inference, with the masked weights of the trained decoder (head 1 of the first block, decoder
input "<start> comment ça va ?"). Left: training fills every row in one pass. Right: inference computes one new row
per step, as each word is written; the rows are the same numbers. Data: data/trained_grid.csv.
Run: python train_infer_anim.py -> train_infer_anim.gif, train_infer_anim_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, GREY, RED, FONT

HERE = Path(__file__).parent
g = pd.read_csv(HERE.parent / "data" / "trained_grid.csv")
g = g[g["head"] == 1]
WORDS = list(dict.fromkeys(g["query"]))
N = len(WORDS)
W = g.pivot(index="i", columns="j", values="weight").values
LAB = [w.replace("<", "&lt;").replace(">", "&gt;") for w in WORDS]


def panel(fig, col, rows):
    xs, ys, s, t = [], [], [], []
    for i in rows:
        for j in range(i + 1):
            xs.append(j); ys.append(i); s.append(np.sqrt(W[i, j]) * 52 + 2); t.append(f"{W[i, j]:.2f}")
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text", text=t, textposition="bottom center",
                             textfont=dict(size=14, color=GREY), marker=dict(size=s, color=BLUE, opacity=0.85),
                             showlegend=False), 1, col)
    mx = [j for i in rows for j in range(i + 1, N)]
    my = [i for i in rows for j in range(i + 1, N)]
    fig.add_trace(go.Scatter(x=mx, y=my, mode="text", text=["-∞"] * len(mx), textfont=dict(size=14, color="#BBBBBB"),
                             showlegend=False), 1, col)
    fig.update_yaxes(autorange=False, range=[N - 0.05, -0.7], tickvals=list(range(N)), ticktext=LAB, showline=False,
                     ticks="", row=1, col=col)
    fig.update_xaxes(range=[-0.6, N - 0.4], tickvals=list(range(N)), ticktext=LAB, side="top", showline=False,
                     ticks="", tickangle=0, row=1, col=col)


def frame(t):
    fig = make_subplots(1, 2, horizontal_spacing=0.14,
                        subplot_titles=("training: one pass, decoder runs 1 time",
                                        f"inference: step {t}, decoder has run {t} time{'s' if t > 1 else ''}"))
    panel(fig, 1, range(N))
    panel(fig, 2, range(t))
    if t <= N:
        fig.add_shape(type="rect", x0=-0.5, x1=N - 0.5, y0=t - 1.5, y1=t - 0.5, line=dict(color=RED, width=3), fillcolor="rgba(0,0,0,0)",
                      row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=17),
                      margin=dict(l=90, r=20, t=110, b=20))
    fig.update_annotations(y=1.17, font=dict(size=19))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ti_frames"
    tmp.mkdir(exist_ok=True)
    for t in range(1, N + 1):
        frame(t).write_image(tmp / f"{t:03d}.png")
    for k in range(N + 1, N + 4):
        shutil.copy(tmp / f"{N:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-start_number", "1", "-i",
                    str(tmp / "%03d.png"), "-vf", "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "train_infer_anim.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (2, N)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "train_infer_anim_frames.png")
    shutil.rmtree(tmp)
