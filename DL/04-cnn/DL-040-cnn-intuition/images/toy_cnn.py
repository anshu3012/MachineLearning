"""A 6 x 6 letter passes through the toy CNN of experiments/toy_cnn.py, one step per frame: the 3 x 3 filter slides
and fills the feature map, ReLU zeroes the negative values, 2 x 2 max pooling keeps four numbers, a dense node and
two outputs give the answer. First the O, then the X (final state).
Plotly frames because numbers fill grids step by step. Our own letters, weights and code; the pipeline on a 6 x 6
O and X is the idea of StatQuest, "Neural Networks Part 8: Image Classification with Convolutional Neural Networks".
Data: data/toy_cnn.json.  Run: python toy_cnn.py -> toy_cnn.gif, toy_cnn_frames.png"""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image
from common import BLUE, GREEN, GREY, RED

ORANGE, PURPLE = "#F58518", "#B279A2"
HERE = Path(__file__).parent
d = json.load(open(HERE.parent / "data" / "toy_cnn.json"))
w = {k: np.array(v) for k, v in d["walk"].items()}
LETTERS = [("O", np.array(d["O"])), ("X", np.array(d["X"]))]
FAM = "Latin Modern Roman"
W, H = 1100, 900
X_F, X_M = 7.5, 12.0                     # left edges of the filter and feature-map panels (top row)
Y2 = -7.6                                # top edge of the bottom row
X_R, X_P, X_D = 0.0, 5.5, 9.0            # bottom row: after ReLU, pooled, dense part


def tint(v, top, base):
    t = float(np.clip(abs(v) / top, 0, 1)) if top else 0.0
    b = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
    return "rgb({},{},{})".format(*[int(255 + (c - 255) * 0.7 * t) for c in b])


def grid(fig, M, x0, y0, color, fmt, title, size=19):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            fig.add_shape(type="rect", x0=x0 + j, x1=x0 + j + 1, y0=y0 - i, y1=y0 - i - 1, layer="below",
                          line=dict(color=GREY, width=1), fillcolor="white" if np.isnan(v) else color(v))
            if not np.isnan(v):
                fig.add_annotation(x=x0 + j + 0.5, y=y0 - i - 0.5, text=fmt(v), showarrow=False,
                                   font=dict(family=FAM, size=size, color="black"))
    fig.add_annotation(x=x0, y=y0 + 0.15, text=title, showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(family=FAM, size=21, color=GREY))


def box(fig, x0, y0, r, c, h, wd, color=ORANGE):
    fig.add_shape(type="rect", x0=x0 + c, x1=x0 + c + wd, y0=y0 - r, y1=y0 - r - h, line=dict(color=color, width=6), fillcolor="rgba(0,0,0,0)")


f2 = lambda v: f"{v:.2f}".replace("-0.00", "0.00")


def frame(n, stage, k=15):
    """stage: 'slide' (window k of 16), 'relu', 'pool', 'answer'."""
    name, img = LETTERS[n]
    fig = go.Figure()
    grid(fig, img, 0, 0, lambda v: tint(v, 1, BLUE), lambda v: f"{v:g}", f"image of the letter {name} (1 = ink)")
    grid(fig, w["K"], X_F, 0, lambda v: tint(v, 1.3, RED if v > 0 else BLUE), f2, "filter (bias −0.50)", 17)
    fmap = np.full((4, 4), np.nan)
    fmap.flat[:k + 1] = w["fmap"][n].flat[:k + 1]
    grid(fig, fmap, X_M, 0, lambda v: tint(v, 2.5, GREEN if v > 0 else GREY), f2, "feature map", 17)
    if stage == "slide":
        r, c = divmod(k, 4)
        box(fig, 0, 0, r, c, 3, 3)
        box(fig, X_M, 0, r, c, 1, 1)
        text = f"step 1: the filter slides. Window {k + 1} of 16: sum of 9 products + bias = {f2(w['fmap'][n][r, c])}"
    done = ["relu", "pool", "answer"]
    if stage in done:
        grid(fig, w["relu"][n], X_R, Y2, lambda v: tint(v, 2.5, GREEN), f2, "after ReLU", 17)
        text = "step 2: ReLU turns every negative value into 0"
    if stage in done[1:]:
        grid(fig, w["pooled"][n], X_P, Y2, lambda v: tint(v, 2.5, ORANGE), f2, "max pooled", 17)
        for i in range(2):
            for j in range(2):
                box(fig, X_R, Y2, 2 * i, 2 * j, 2, 2, ORANGE)
        text = "step 3: 2 × 2 max pooling keeps the largest value of each block"
    if stage == "answer":
        out, hid = w["out"][n], w["hidden"][n]
        lines = [f"dense node (ReLU) = {f2(hid)}",
                 f"output O = {f2(out[0])}", f"output X = {f2(out[1])}"]
        for i, t in enumerate(lines):
            win = i > 0 and out[i - 1] == out.max()
            fig.add_annotation(x=X_D, y=Y2 - 0.6 - 1.1 * i, text=("<b>" + t + "</b>") if win else t, showarrow=False,
                               xanchor="left", font=dict(family=FAM, size=22, color=PURPLE if win else "black"))
        text = f"step 4: flatten the 4 values, one dense node, two outputs: the answer is {'OX'[int(out.argmax())]}"
    fig.update_layout(template="simple_white", width=W, height=H, showlegend=False,
                      title=dict(text=text, x=0.5, y=0.975, font=dict(family=FAM, size=23)),
                      xaxis=dict(visible=False, range=[-0.3, 16.6], scaleanchor="y"),
                      yaxis=dict(visible=False, range=[-12.2, 1.2]), margin=dict(l=10, r=10, t=60, b=10))
    return fig


if __name__ == "__main__":
    seq = [(0, "slide", k) for k in range(16)] + [(0, s, 15) for s in ("relu", "relu", "pool", "pool", "answer", "answer", "answer")]
    seq += [(1, "slide", 15)] + [(1, s, 15) for s in ("relu", "pool", "answer", "answer", "answer", "answer")]
    tmp = HERE / ".toy_frames"
    tmp.mkdir(exist_ok=True)
    pio.write_images([frame(*s) for s in seq], [tmp / f"{i:03d}.png" for i in range(len(seq))], width=W, height=H)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.25", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "toy_cnn.gif")],
                   check=True)
    keys = [5, 17, 19, len(seq) - 1]
    imgs = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    sheet = Image.new("RGB", (2 * W + 16, 2 * H + 16), "white")
    for i, im in enumerate(imgs):
        sheet.paste(im.resize((W, H)), ((i % 2) * (W + 16), (i // 2) * (H + 16)))
    sheet.save(HERE / "toy_cnn_frames.png")
    shutil.rmtree(tmp)
