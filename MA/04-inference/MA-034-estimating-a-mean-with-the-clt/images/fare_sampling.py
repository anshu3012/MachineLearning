"""Estimating the mean Titanic fare, sample by sample: 50 passengers are drawn (orange ticks on the fare
histogram), their mean drops into the pile of sample means below; after 100 samples the average of the means,
the 2-SE range and finally the true mean appear. Same sampling as the Notebook (seed 42).
Run: python fare_sampling.py  -> fare_sampling.gif, fare_sampling_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
data = HERE.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
fare = df["Fare"].dropna()
rng = np.random.default_rng(42)
samples = np.array([fare.sample(50, random_state=rng).to_numpy() for _ in range(100)])
means = samples.mean(axis=1)
est, se, TRUE = means.mean(), means.std(ddof=1) / 10, fare.mean()
assert round(means[0], 2) == 37.27 and round(est, 2) == 31.87 and round(TRUE, 2) == 33.30
assert round(est - 2 * se, 2) == 30.35 and round(est + 2 * se, 2) == 33.38

XMAX, BW = 120, 2.0
counts, edges = np.histogram(fare.clip(upper=XMAX - 0.01), bins=np.arange(0, XMAX + 5, 5), density=True)


def stack(vals):                                             # dot-plot positions: equal values pile up
    b = np.floor(vals / BW)
    ys = np.array([(b[:i] == b[i]).sum() + 1 for i in range(len(b))])
    return (b + 0.5) * BW, ys


def frame(k, stage=0):
    """k samples drawn; stage 1 adds the estimate, 2 the range, 3 the true mean."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.45, 0.55])
    fig.add_bar(x=(edges[:-1] + edges[1:]) / 2, y=counts, width=5, marker_color="#D9D9D9", row=1, col=1)
    if stage == 0:
        s = samples[k - 1]
        fig.add_scatter(x=np.minimum(s, XMAX - 1), y=np.full(50, 0.002) + rng_j.uniform(0, 0.006, 50),
                        mode="markers", marker=dict(color=ORANGE, size=9, symbol="line-ns-open",
                                                    line=dict(width=3, color=ORANGE)), row=1, col=1)
    x, y = stack(means[:k])
    col = [GREEN] * k
    if stage == 0:
        col[-1] = ORANGE
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color=col, size=11, line=dict(width=1, color="white")),
                    row=2, col=1)
    if stage == 0:                                           # after both panels hold data, or plotly skips one
        for r in (1, 2):
            fig.add_vline(x=means[k - 1], line=dict(color=ORANGE, width=4), opacity=1, row=r, col=1)
    if stage >= 2:
        fig.add_vrect(x0=est - 2 * se, x1=est + 2 * se, fillcolor=GREEN, opacity=0.45, line_width=0, row=2, col=1)
        fig.add_annotation(x=est + 2 * se, y=10.5, ax=110, ay=0, text="± 2 SE", font_color=GREEN, arrowcolor=GREEN,
                           arrowwidth=2, row=2, col=1)
    if stage >= 1:
        fig.add_vline(x=est, line=dict(color="black", width=3), opacity=1, row=2, col=1)
        fig.add_annotation(x=est, y=17, ax=-110, ay=0, text=f"estimate {est:.2f}", arrowwidth=2, row=2, col=1)
    if stage >= 3:
        fig.add_vline(x=TRUE, line=dict(color=RED, width=4, dash="dash"), opacity=1, row=2, col=1)
        fig.add_annotation(x=TRUE, y=14, ax=110, ay=0, text=f"true {TRUE:.2f}", font_color=RED, arrowcolor=RED,
                           arrowwidth=2, row=2, col=1)
    title = {0: f"sample {k} of 100: 50 fares, mean {means[k - 1]:.2f}",
             1: f"average of the 100 means: {est:.2f}",
             2: f"± 2 SE range: {est - 2 * se:.2f} to {est + 2 * se:.2f}",
             3: f"true mean {TRUE:.2f}: inside the range"}[stage]
    fig.update_layout(template="simple_white", width=900, height=820, showlegend=False, bargap=0,
                      font=dict(family="Latin Modern Roman", size=24), title=dict(text=title, x=0.5, y=0.97),
                      margin=dict(l=90, r=30, t=90, b=70))
    fig.update_xaxes(range=[0, XMAX])
    fig.update_xaxes(title_text="fare (pounds); fares above 120 sit at the edge", row=2, col=1)
    fig.update_yaxes(title_text="all fares", showticklabels=False, range=[0, counts.max() * 1.05], row=1, col=1)
    fig.update_yaxes(title_text="sample means", showticklabels=False, range=[0, 19], row=2, col=1)
    return fig


rng_j = np.random.default_rng(0)                             # vertical jitter of the ticks only
SCHEDULE = [(k, 0, 2) for k in range(1, 9)] + [(k, 0, 1) for k in (10, 13, 16, 20, 25, 30, 40, 50, 60, 75, 90)] \
    + [(100, 0, 3), (100, 1, 4), (100, 2, 4), (100, 3, 10)]    # (samples drawn, stage, frames to show)

if __name__ == "__main__":
    tmp = HERE / ".fare_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for k, stage, rep in SCHEDULE:
        frame(k, stage).write_image(tmp / f"{n:03d}.png")
        if (k, stage) in [(1, 0), (8, 0), (100, 0), (100, 3)]:
            keys.append(n)
        for _ in range(rep - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "fare_sampling.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "fare_sampling_frames.png")
    shutil.rmtree(tmp)
