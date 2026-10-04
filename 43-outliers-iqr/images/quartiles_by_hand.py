"""Quartiles by hand on nine values: the exam marks of the first nine students of the placement data. Sort, mark the
median, split into a lower and an upper half, take the middle of each half (Q1, Q3), then draw the box and its arms.
Idea (median of each half on a small sorted list) after Khan Academy, "How to calculate interquartile range IQR";
data and code are ours. Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python quartiles_by_hand.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY, GREEN = "#4C78A8", "#F58518", "#E45756", "#6B6B6B", "#54A24B"
raw = pd.read_csv(HERE.parent / "data" / "placement.csv")["placement_exam_marks"].head(9).to_numpy()
s = np.sort(raw)
med, q1, q3 = np.median(s), np.median(s[:4]), np.median(s[5:])
assert list(s) == [8, 11, 17, 23, 26, 38, 38, 39, 40] and (med, q1, q3) == (26, 14, 38.5)
assert list(np.quantile(raw, [0.25, 0.75])) == [17, 38]          # pandas/NumPy interpolation gives other quartiles
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
assert (iqr, lo, hi) == (24.5, -22.75, 75.25)
ys = np.zeros(9)
ys[6] = 0.22                                                     # the second 38 sits above the first
fmt = lambda a: ", ".join(f"{v:g}" for v in a)
TITLES = ["1. the marks of nine students", "2. sort them",
          "3. median = the middle value: 4 marks on each side",
          "4. Q1 = middle of the lower half = (11 + 17) / 2 = 14",
          "5. Q3 = middle of the upper half = (38 + 39) / 2 = 38.5",
          "6. IQR = Q3 - Q1 = 38.5 - 14 = 24.5: the box, and its arms"]


def frame(k):
    fig = go.Figure()
    fig.add_annotation(x=0.5, y=1.03, xref="paper", yref="paper", yanchor="bottom", showarrow=False, font=dict(size=30),
                       text=fmt(raw if k == 0 else s))
    if k >= 1:
        colour = [BLUE] * 9
        if k >= 2:
            colour[4] = RED
        fig.add_trace(go.Scatter(x=s, y=ys, mode="markers+text", text=[f"{v:g}" for v in s],
                                 textposition=["bottom center"] * 4 + ["bottom left", "bottom left", "middle left", "bottom center", "bottom right"],
                                 textfont=dict(size=22), marker=dict(color=colour, size=20)))
    if k >= 2:
        fig.add_annotation(x=med, y=0.62, text=f"median {med:g}", showarrow=False, font=dict(color=RED, size=24))
        fig.add_shape(type="line", x0=med, x1=med, y0=-0.45, y1=0.5, line=dict(color=RED, width=3), opacity=1)
    if k == 3 or k == 4:                                          # shade the half in use
        a, b = (s[0] - 1.5, s[3] + 1.5) if k == 3 else (s[5] - 1.5, s[8] + 1.5)
        fig.add_shape(type="rect", x0=a, x1=b, y0=-0.45, y1=0.5, fillcolor=ORANGE, opacity=0.15, line_width=0)
    if k >= 3:
        fig.add_shape(type="line", x0=q1, x1=q1, y0=-0.45, y1=0.5, line=dict(color=ORANGE, width=3), opacity=1)
        fig.add_annotation(x=q1, y=0.62, text=f"Q1 = {q1:g}", showarrow=False, font=dict(color=ORANGE, size=24))
    if k >= 4:
        fig.add_shape(type="line", x0=q3, x1=q3, y0=-0.45, y1=0.5, line=dict(color=ORANGE, width=3), opacity=1)
        fig.add_annotation(x=q3, y=0.62, text=f"Q3 = {q3:g}", showarrow=False, font=dict(color=ORANGE, size=24),
                           xanchor="left", xshift=-30)
    if k >= 5:
        fig.add_shape(type="rect", x0=q1, x1=q3, y0=-1.05, y1=-0.65, line=dict(color="black", width=3),
                      fillcolor="rgba(76,120,168,0.25)", opacity=1)
        fig.add_shape(type="line", x0=med, x1=med, y0=-1.05, y1=-0.65, line=dict(color=RED, width=3), opacity=1)
        for a, b in ((s[0], q1), (q3, s[-1])):                    # arms end at the last value inside the fences
            fig.add_shape(type="line", x0=a, x1=b, y0=-0.85, y1=-0.85, line=dict(color="black", width=3), opacity=1)
        for v in (s[0], s[-1]):
            fig.add_shape(type="line", x0=v, x1=v, y0=-0.95, y1=-0.75, line=dict(color="black", width=3), opacity=1)
        fig.add_annotation(x=(q1 + q3) / 2, y=-1.25, text=f"IQR = {iqr:g}", showarrow=False,
                           font=dict(color=BLUE, size=24))
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=TITLES[k], x=0.02, y=0.96),
                      margin=dict(l=40, r=40, t=150, b=70))
    fig.update_xaxes(range=[0, 46], dtick=5, title="placement_exam_marks", visible=k >= 1)
    fig.update_yaxes(visible=False, range=[-1.45, 0.85])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".quart_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(6):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(2 if k < 5 else 4):                        # 2 s per step, hold the last
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "quartiles_by_hand.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (2, 3, 4, 5)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "quartiles_by_hand_frames.png")
    shutil.rmtree(tmp)
