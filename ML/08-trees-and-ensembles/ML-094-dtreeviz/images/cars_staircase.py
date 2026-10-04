"""A regression tree's staircase built one split at a time. Data: dtreeviz's cars.csv (392 cars), input WGT, output
MPG; the same depth-3 tree as cars_univar in figs.py (DecisionTreeRegressor, max_depth=3, random_state=0). Frame 0 is
one flat line (the mean of all cars); each later frame applies one more of the tree's 7 splits, in order of depth: a
vertical cut appears and the flat line on each side moves to the mean MPG of its own cars.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
BLUE, RED, GREY, ORANGE = "#4C78A8", "#E45756", "#6B6B6B", "#F58518"

cars = pd.read_csv(HERE.parent / "data" / "cars.csv")
t = DecisionTreeRegressor(max_depth=3, random_state=0).fit(cars[["WGT"]], cars["MPG"]).tree_
LO, HI = cars.WGT.min(), cars.WGT.max()
order, queue = [], [0]                                  # internal nodes, breadth-first: depth 1, then 2, then 3
while queue:
    n = queue.pop(0)
    if t.children_left[n] != -1:
        order.append(n)
        queue += [t.children_left[n], t.children_right[n]]
assert len(order) == 7 and round(float(t.threshold[0])) == 2764 and round(float(t.value[0][0][0]), 1) == 23.4


def leaves(k):
    """(low, high, mean MPG) of every region after the first k splits."""
    done, out = set(order[:k]), []

    def walk(n, lo, hi):
        if n in done:
            walk(t.children_left[n], lo, t.threshold[n])
            walk(t.children_right[n], t.threshold[n], hi)
        else:
            out.append((lo, hi, t.value[n][0][0]))
    walk(0, LO, HI)
    return out


def frame(k):
    fig = go.Figure()
    fig.add_scatter(x=cars.WGT, y=cars.MPG, mode="markers", marker=dict(color=BLUE, size=8, opacity=0.5))
    for j, n in enumerate(order[:k]):
        new = j == k - 1
        fig.add_vline(x=t.threshold[n], line=dict(color=ORANGE if new else GREY, dash="dot", width=4 if new else 2))
    for lo, hi, m in leaves(k):
        fig.add_scatter(x=[lo, hi], y=[m, m], mode="lines", line=dict(color=RED, width=6))
    title = ("<b>No split:</b> one prediction, the mean of all 392 cars" if k == 0 else
             f"<b>Split {k} of 7:</b> cut at WGT = {t.threshold[order[k - 1]]:,.0f} → {k + 1} flat steps")
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(title="WGT: weight (pounds)", range=[LO - 100, HI + 100]),
                      yaxis=dict(title="MPG: miles per gallon", range=[5, 50]), margin=dict(l=90, r=30, t=90, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cs_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(8):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    for j, k in enumerate([k for k in range(8) for _ in range(2)] + [7] * 5):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "cars_staircase.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (0, 1, 3, 7)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i % 2 * (w + 16), i // 2 * (h + 16)))
    sheet.save(HERE / "cars_staircase_frames.png")
    shutil.rmtree(tmp)
