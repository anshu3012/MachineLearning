"""Animation for Note ML-041, Section 4: turning CGPA into z-scores. Subtract the mean (slide), then divide by the
standard deviation (squeeze). The limits 5.11 and 8.81 travel with the data and land on z = -3 and z = +3; the same
5 red students stay outside. Run: python zscore_slide.py -> zscore_slide.gif, zscore_slide_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
df = pd.read_csv(HERE.parent / "data" / "placement.csv")
x = df["cgpa"].to_numpy()
mean, std = x.mean(), x.std(ddof=1)
lo, hi = mean - 3 * std, mean + 3 * std
out = (x < lo) | (x > hi)
z = (x - mean) / std
assert round(mean, 4) == 6.9612 and round(std, 4) == 0.6159 and out.sum() == 5
assert round(z.max(), 2) == 3.51 and round(z.min(), 2) == -3.36 and ((np.abs(z) > 3) == out).all()
jit = np.random.default_rng(0).uniform(-1, 1, len(x))       # vertical spread only, so dots do not overlap


def stage(k):                                               # (shift fraction, scale fraction, title)
    if k < 6:
        return 0, 0, f"1. the CGPA of 1,000 students: mean {mean:.2f}, std {std:.2f}"
    if k < 16:
        return min(1, (k - 6) / 8), 0, f"2. subtract the mean {mean:.2f}: the centre moves to 0"
    if k < 26:
        return 1, min(1, (k - 16) / 8), f"3. divide by the std {std:.2f}: one std becomes one unit"
    return 1, 1, "4. the limits 5.11 and 8.81 are now z = -3 and z = +3"


def move(v, a, b):
    return (v - a * mean) / (1 + b * (std - 1))


def frame(k):
    a, b, title = stage(k)
    fig = go.Figure()
    for flag, c in ((~out, BLUE), (out, RED)):
        fig.add_trace(go.Scatter(x=move(x[flag], a, b), y=jit[flag], mode="markers",
                                 marker=dict(color=c, size=7 if c == BLUE else 13, opacity=0.35 if c == BLUE else 1)))
    for v, name in ((lo, "lower"), (hi, "upper")):
        p = move(v, a, b)
        lab = f"{name} {v:.2f}" if b < 1 else f"z = {'-3' if v == lo else '+3'}"
        fig.add_vline(x=p, line=dict(color=GREY, width=3, dash="dash"))
        fig.add_annotation(x=p, y=1.25, text=lab, showarrow=False, font=dict(size=22, color=GREY),
                           xanchor="right" if v == lo else "left")
    fig.add_vline(x=0, line=dict(color="black", width=1))
    fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.02, y=0.95),
                      margin=dict(l=40, r=30, t=90, b=70))
    fig.update_xaxes(range=[-5, 10], dtick=1, title="value" if b < 1 else "z-score")
    fig.update_yaxes(visible=False, range=[-1.5, 1.5])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".zslide_frames"
    tmp.mkdir(exist_ok=True)
    N = 30
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 10):                               # hold the last frame
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "zscore_slide.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 14, 21, N - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "zscore_slide_frames.png")
    shutil.rmtree(tmp)
