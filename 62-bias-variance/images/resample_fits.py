"""Bias and variance, watched: the same 20 inputs get fresh noise each frame (a new training set, from common.py);
a straight line (degree 1) and a degree-11 polynomial are refitted, and every old fit stays behind as a faint ghost.
At the end the average of the 20 fits appears: its gap to the truth is the bias, the spread of the ghosts the variance.
Run: python resample_fits.py  -> resample_fits.gif, resample_fits_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from common import X, Y, f, fits, xs

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
SETS, YR = 20, (-4, 4)
DEGS = (1, 11)
G = {d: fits(d)[1][:, :SETS] for d in DEGS}               # 200 grid points x 20 training sets
TITLES = {1: "straight line (degree 1)", 11: "degree 11 polynomial"}


def frame(k, stage=0):
    """k: number of training sets shown (the k-th is the current one). stage 1 adds the average, stage 2 the labels."""
    fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.04, subplot_titles=[TITLES[d] for d in DEGS])
    for col, d in enumerate(DEGS, start=1):
        g = G[d]
        for j in range(k - 1):                              # ghosts of the earlier fits
            fig.add_trace(go.Scatter(x=xs, y=g[:, j], mode="lines", line=dict(color=ORANGE, width=1.5), opacity=0.35), 1, col)
        fig.add_trace(go.Scatter(x=xs, y=f(xs), mode="lines", line=dict(color="black", width=3, dash="dash")), 1, col)
        if stage == 0:                                      # the current training set and its fit
            fig.add_trace(go.Scatter(x=X.ravel(), y=Y[:, k - 1], mode="markers",
                                     marker=dict(size=10, color=GREY, line=dict(color="white", width=1))), 1, col)
            fig.add_trace(go.Scatter(x=xs, y=g[:, k - 1], mode="lines", line=dict(color=ORANGE, width=4)), 1, col)
        if stage >= 1:
            m = g.mean(axis=1)
            fig.add_trace(go.Scatter(x=xs, y=m, mode="lines", line=dict(color=BLUE, width=5)), 1, col)
        if stage >= 2 and d == 1:                           # bias: the gap between average fit and truth
            fig.add_trace(go.Scatter(x=np.r_[xs, xs[::-1]], y=np.r_[g.mean(axis=1), f(xs)[::-1]], fill="toself",
                                     fillcolor="rgba(76,120,168,0.30)", line=dict(width=0), mode="lines"), 1, col)
    xref = {1: "x", 11: "x2"}
    if stage == 0:
        fig.add_annotation(x=0.5, y=1.25, xref="paper", yref="paper", showarrow=False, font=dict(size=26),
                           text=f"training set {k} of {SETS}: new noise, same 20 inputs")
    else:
        fig.add_annotation(x=0.5, y=1.25, xref="paper", yref="paper", showarrow=False, font=dict(size=26, color=BLUE),
                           text=f"blue = average of the {SETS} fits")
    if stage >= 2:
        fig.add_annotation(x=0, y=-3.3, xref=xref[1], yref="y", showarrow=False, font=dict(size=24, color=BLUE),
                           text="<b>high bias</b>: average misses the wave")
        fig.add_annotation(x=0, y=-3.3, xref=xref[11], yref="y", showarrow=False, font=dict(size=24, color=ORANGE),
                           text="<b>high variance</b>: fits scatter widely")
    fig.update_xaxes(title="x", range=[-2.9, 2.9])
    fig.update_yaxes(range=YR)
    fig.update_yaxes(title="y", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=150, b=60))
    fig.update_annotations(selector=dict(text=TITLES[1]), font_size=24)
    fig.update_annotations(selector=dict(text=TITLES[11]), font_size=24)
    return fig


# Check: with only 20 sets the average line still misses the wave (bias) and the degree-11 ghosts spread more (variance).
spread = {d: float(G[d].std(axis=1).mean()) for d in DEGS}
gap = {d: float(np.abs(G[d].mean(axis=1) - f(xs)).mean()) for d in DEGS}
assert spread[11] > 2 * spread[1] and gap[1] > 2 * gap[11], (spread, gap)
print("mean spread", spread, "mean gap to truth", gap)

if __name__ == "__main__":
    tmp = HERE / ".resample_frames"
    tmp.mkdir(exist_ok=True)
    plan = [(k, 0) for k in range(1, SETS + 1)] + [(SETS, 1)] * 4 + [(SETS, 2)] * 10   # holds: repeat a frame
    done = {}
    for i, key in enumerate(plan):
        if key not in done:
            frame(*key).write_image(tmp / f"{i:03d}.png")
            done[key] = i
        else:
            shutil.copy(tmp / f"{done[key]:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "resample_fits.gif")], check=True)
    keys = [Image.open(tmp / f"{done[key]:03d}.png").convert("RGB") for key in [(1, 0), (5, 0), (SETS, 0), (SETS, 2)]]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "resample_fits_frames.png")
    shutil.rmtree(tmp)
