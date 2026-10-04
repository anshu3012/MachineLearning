"""Sections 2 to 4 on 14 people: who loves candy and who loves soda. Cells: candy and soda 2, candy only 4, soda only 5,
neither 3. Frames: the dots in a 2 x 2 table; each cell / 14 = joint probability; row and column totals = marginal
probabilities; condition on "loves soda" (the other column dims): 5 of 7 = 0.71 = (5/14)/(7/14); condition on
"no candy" instead (the other row dims): the same cell, 5 of 8 = 0.625.
Run: python candy_soda.py  -> candy_soda.gif, candy_soda_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#DDDDDD"
COUNTS = {(0, 0): 2, (0, 1): 4, (1, 0): 5, (1, 1): 3}       # (row: candy yes/no, col: soda yes/no)
assert sum(COUNTS.values()) == 14 and round(5 / 7, 2) == 0.71 and 5 / 8 == 0.625
ROWS, COLS = ["loves candy", "no candy"], ["loves soda", "no soda"]
TITLES = ["14 people: candy? soda?", "Joint: each cell ÷ 14", "Marginal: add each row and column",
          "Given: loves soda", "Given: no candy"]


def cell_xy(r, c):
    return 1.5 + 2.2 * c, 3.0 - 2.0 * r                     # centre of a cell


def frame(step):
    fig = go.Figure()
    keep_col = 0 if step == 3 else None
    keep_row = 1 if step == 4 else None
    for (r, c), n in COUNTS.items():
        cx, cy = cell_xy(r, c)
        dim = (keep_col is not None and c != keep_col) or (keep_row is not None and r != keep_row)
        target = (r, c) == (1, 0) and step >= 3
        fig.add_shape(type="rect", x0=cx - 1.1, x1=cx + 1.1, y0=cy - 1.0, y1=cy + 1.0,
                      line=dict(color="black", width=2), layer="below",
                      fillcolor=GREY if dim else ("rgba(228,87,86,0.35)" if target else "white"))
        k = np.arange(n)
        fig.add_scatter(x=cx - 0.7 + 0.35 * (k % 5), y=cy + 0.45 - 0.4 * (k // 5), mode="markers",
                        marker=dict(size=22, color="#BBBBBB" if dim else BLUE, line=dict(width=1.5)))
        label = f"{n}" if step == 0 else f"{n}/14 = {n / 14:.2f}"
        fig.add_annotation(x=cx, y=cy - 0.55, text=label, showarrow=False,
                           font=dict(size=24, color="#999999" if dim else "black"))
    for c, name in enumerate(COLS):
        fig.add_annotation(x=cell_xy(0, c)[0], y=4.35, text=f"<b>{name}</b>", showarrow=False)
    for r, name in enumerate(ROWS):
        fig.add_annotation(x=-0.15, y=cell_xy(r, 0)[1], text=f"<b>{name}</b>", showarrow=False, xanchor="right")
    if step >= 2:
        for r in range(2):
            tot = COUNTS[(r, 0)] + COUNTS[(r, 1)]
            fig.add_annotation(x=5.85, y=cell_xy(r, 0)[1], text=f"{tot}/14", showarrow=False,
                               font=dict(color=ORANGE, size=24))
        for c in range(2):
            tot = COUNTS[(0, c)] + COUNTS[(1, c)]
            fig.add_annotation(x=cell_xy(0, c)[0], y=-0.4, text=f"{tot}/14", showarrow=False,
                               font=dict(color=ORANGE, size=24))
    if step == 3:
        box = "no candy, given soda:<br>5 of 7 = <b>0.71</b><br>= (5/14) / (7/14)<br>= joint / marginal"
    elif step == 4:
        box = "given no candy:<br>5 of 8 = <b>0.625</b><br>same top, new bottom"
    else:
        box = ""
    if box:
        fig.add_annotation(x=7.0, y=2.0, xanchor="left", text=box, showarrow=False, align="left",
                           font=dict(size=28, color=RED))
    fig.update_layout(template="simple_white", width=1150, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=26), title=dict(text=TITLES[step], x=0.5, y=0.96),
                      xaxis=dict(visible=False, range=[-2.6, 10.6]), yaxis=dict(visible=False, range=[-0.9, 4.7]),
                      margin=dict(l=10, r=10, t=70, b=10))
    return fig


PLAN = [(0, 6), (1, 8), (2, 8), (3, 12), (4, 14)]

if __name__ == "__main__":
    tmp = HERE / ".candy_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step, hold in PLAN:
        frame(step).write_image(tmp / f"{n:03d}.png")
        keys[step] = n
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "candy_soda.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[k]:03d}.png").convert("RGB") for k in (1, 2, 3, 4)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "candy_soda_frames.png")
    shutil.rmtree(tmp)
