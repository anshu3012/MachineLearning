"""Marginalising, step by step, on the Titanic joint table (891 passengers): the three cells of each column slide
down and add up into the bottom margin, P(died) = 0.616 and P(survived) = 0.384; then the two cells of each row
slide right into the right margin, P(class) = 0.242, 0.207, 0.551.
Run: python marginalise.py  -> marginalise.gif, marginalise_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")
J = pd.crosstab(df["Pclass"], df["Survived"], normalize="all").values      # rows: class 1-3, cols: died, survived
assert np.allclose(J.sum(0).round(3), [0.616, 0.384]) and np.allclose(J.sum(1).round(3), [0.242, 0.207, 0.551])
CX, RY = [1, 2], [3, 2, 1]                     # cell centres: column x, row y; bottom margin y = 0, right margin x = 3


def cell(fig, x, y, text, fill, bold=False):
    fig.add_shape(type="rect", x0=x - 0.48, x1=x + 0.48, y0=y - 0.45, y1=y + 0.45, fillcolor=fill,
                  line=dict(color="white", width=3), layer="below")
    fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>" if bold else text, showarrow=False, font=dict(size=26))


def frame(col_t, row_t, col_done, row_done, msg):
    """col_t, row_t in [0, 1]: how far the moving copies have travelled; *_done: margins filled so far."""
    fig = go.Figure()
    for i, y in enumerate(RY):
        for j, x in enumerate(CX):
            cell(fig, x, y, f"{J[i, j]:.3f}", "rgba(76,120,168,0.35)")
    for j, x in enumerate(CX):
        cell(fig, x, 0, f"{J[:, j].sum():.3f}" if j < col_done else "", "rgba(245,133,24,0.4)", bold=True)
    for i, y in enumerate(RY):
        cell(fig, 3, y, f"{J[i].sum():.3f}" if i < row_done else "", "rgba(245,133,24,0.4)", bold=True)
    if col_t is not None:                                      # copies of one column's cells sliding down
        j = col_done
        for i, y in enumerate(RY):
            fig.add_annotation(x=CX[j], y=y + (0 - y) * col_t, text=f"{J[i, j]:.3f}", showarrow=False,
                               font=dict(size=26, color=ORANGE), bgcolor="white")
    if row_t is not None:                                      # copies of every row's cells sliding right
        for i, y in enumerate(RY):
            for j, x in enumerate(CX):
                fig.add_annotation(x=x + (3 - x) * row_t, y=y + (0.2 - 0.4 * j) * row_t, text=f"{J[i, j]:.3f}", showarrow=False,
                                   font=dict(size=26, color=ORANGE), bgcolor="white")
    for x, t in ((1, "died"), (2, "survived"), (3, "P(class)")):
        fig.add_annotation(x=x, y=3.75, text=f"<b>{t}</b>", showarrow=False, font=dict(size=24))
    for y, t in ((3, "class 1"), (2, "class 2"), (1, "class 3"), (0, "P(Y = y)")):
        fig.add_annotation(x=0.35, y=y, text=f"<b>{t}</b>", showarrow=False, xanchor="right", font=dict(size=24))
    fig.add_annotation(x=1.7, y=-0.85, text=msg, showarrow=False, font=dict(size=24, color=GREY))
    fig.update_xaxes(visible=False, range=[-0.9, 3.6])
    fig.update_yaxes(visible=False, range=[-1.2, 4.1])
    fig.update_layout(template="simple_white", width=900, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=10, r=10, t=10, b=10))
    return fig


STEPS = (0.25, 0.5, 0.75, 1.0)
PLAN = [((None, None, 0, 0, "the joint table: six cells"), 5)]
PLAN += [((t, None, 0, 0, "add down the died column"), 1) for t in STEPS]
PLAN += [((None, None, 1, 0, "0.0898 + 0.1089 + 0.4175 = 0.6162, so 0.616"), 5)]
PLAN += [((t, None, 1, 0, "add down the survived column"), 1) for t in STEPS]
PLAN += [((None, None, 2, 0, "0.1526 + 0.0976 + 0.1336 = 0.3838, so 0.384"), 5)]
PLAN += [((None, t, 2, 0, "add across each row"), 1) for t in STEPS]
PLAN += [((None, None, 2, 3, "the margins: marginal probabilities"), 14)]

if __name__ == "__main__":
    tmp = HERE / ".marg_frames"
    tmp.mkdir(exist_ok=True)
    m, keys = 0, []
    for i, (args, hold) in enumerate(PLAN):
        frame(*args).write_image(tmp / f"{m:03d}.png")
        if i in (2, 5, 14, len(PLAN) - 1):
            keys.append(m)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{m:03d}.png", tmp / f"{m + 1:03d}.png")
            m += 1
        m += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "marginalise.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (keys[1], keys[3])]   # first sum, final table
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "marginalise_frames.png")
    shutil.rmtree(tmp)
