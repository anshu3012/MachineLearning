"""Capping on the Note's CGPA column: the 1,000 students as dots, the limits 5.11 and 8.81 as dashed lines; the 5
outliers (red) slide onto the limit they crossed. No dot is removed. Our own design; no source to credit.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python capping_slide.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREY, ORANGE = "#4C78A8", "#E45756", "#6B6B6B", "#F58518"
x = pd.read_csv(HERE.parent / "data" / "placement.csv")["cgpa"].to_numpy()
mean, std = x.mean(), x.std(ddof=1)
lo, hi = mean - 3 * std, mean + 3 * std
out = (x < lo) | (x > hi)
capped = np.clip(x, lo, hi)
assert out.sum() == 5 and round(capped.min(), 2) == 5.11 and round(capped.max(), 2) == 8.81
jit = np.random.default_rng(0).uniform(-1, 1, len(x))       # vertical spread only, so dots do not overlap
N = 22


def frame(k):
    t = 0 if k < 5 else min(1, (k - 5) / 10)                 # 0 = original, 1 = capped
    now = x + t * (capped - x)
    title = ("1. five students lie outside the limits 5.11 and 8.81" if t == 0 else
             "2. capping: each outlier moves onto the limit it crossed" if t < 1 else
             "3. all 1,000 rows stay: minimum 5.11, maximum 8.81")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=now[~out], y=jit[~out], mode="markers", marker=dict(color=BLUE, size=7, opacity=0.35)))
    fig.add_trace(go.Scatter(x=now[out], y=jit[out], mode="markers",
                             marker=dict(color=RED if t < 1 else ORANGE, size=15, line=dict(color="white", width=1))))
    for v, name, anchor in ((lo, "lower limit 5.11", "left"), (hi, "upper limit 8.81", "right")):
        fig.add_vline(x=v, line=dict(color=GREY, width=3, dash="dash"))
        fig.add_annotation(x=v, y=1.3, text=name, showarrow=False, font=dict(size=22, color=GREY), xanchor=anchor,
                           xshift=8 if anchor == "left" else -8)
    fig.add_annotation(x=lo, y=-1.3, xanchor="left", xshift=8, showarrow=False, font=dict(size=22, color=RED),
                       text="outliers 4.89, 4.90, 4.92" + (" → 5.11" if t == 1 else ""))
    fig.add_annotation(x=hi, y=-1.3, xanchor="right", xshift=-8, showarrow=False, font=dict(size=22, color=RED),
                       text="outliers 8.87, 9.12" + (" → 8.81" if t == 1 else ""))
    fig.update_layout(template="simple_white", width=1000, height=480, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.02, y=0.95),
                      margin=dict(l=40, r=30, t=80, b=70))
    fig.update_xaxes(range=[4.5, 9.5], dtick=0.5, title="CGPA")
    fig.update_yaxes(visible=False, range=[-1.6, 1.6])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cap_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 12):                               # hold the last frame
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "capping_slide.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 10, N - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 3 * h + 32), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "capping_slide_frames.png")
    shutil.rmtree(tmp)
