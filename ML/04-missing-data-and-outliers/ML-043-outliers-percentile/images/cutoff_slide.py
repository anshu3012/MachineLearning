"""Animation for Note ML-043, Section 8: sliding the percentile cut-offs on the 10,000 heights.
As the cut-offs move in from 0.5/99.5 to 5/95, the limits close in and the red share grows from 1% to 10%.
Run: python cutoff_slide.py -> cutoff_slide.gif, cutoff_slide_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
BINS = dict(start=54, end=79.5, size=0.5)
h = pd.read_csv(HERE.parent / "data" / "weight-height.csv")["Height"]
CUTS = np.round(np.arange(0.5, 5.01, 0.25), 2)
TABLE = {0.5: (57.31, 75.69, 100), 1.0: (58.13, 74.79, 200), 2.5: (59.26, 73.70, 500), 5.0: (60.25, 72.62, 1000)}


def limits(p):
    lo, hi = h.quantile([p / 100, 1 - p / 100])
    return lo, hi, int(((h < lo) | (h > hi)).sum())


for p, (a, b, n) in TABLE.items():                      # the table of Section 8
    lo, hi, k = limits(p)
    assert (round(lo, 2), round(hi, 2), k) == (a, b, n), p


def nth(v):
    return f"{v:g}" + ("st" if v == 1 else "th")


def frame(p):
    lo, hi, k = limits(p)
    out = (h < lo) | (h > hi)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=h[~out], xbins=BINS, marker_color=BLUE))
    fig.add_trace(go.Histogram(x=h[out], xbins=BINS, marker_color=RED))
    for v, s in ((lo, "right"), (hi, "left")):
        fig.add_vline(x=v, line=dict(color=GREY, width=3, dash="dash"), opacity=1)
        fig.add_annotation(x=v, y=1.0, yref="paper", yanchor="bottom", xanchor=s, showarrow=False, text=f"{v:.2f}")
    fig.add_annotation(x=0.01, y=0.85, xref="paper", yref="paper", xanchor="left", showarrow=False, align="left",
                       font=dict(color=RED, size=24), text=f"{k:,} outliers<br>({100 * k / len(h):g}%)")
    fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False, barmode="overlay",
                      bargap=0.05, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"cut-offs: {nth(p)} and {nth(100 - p)} percentile", x=0.02, y=0.96),
                      margin=dict(l=90, r=30, t=110, b=70))
    fig.update_xaxes(title="Height (inches)", range=[54, 79.5], dtick=2)
    fig.update_yaxes(title="people", range=[0, 520])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cutoff_frames"
    tmp.mkdir(exist_ok=True)
    seq = [p for p in CUTS for _ in range(3 if p in TABLE else 1)]   # pause on the four rows of the table
    for i, p in enumerate(seq + [CUTS[-1]] * 8):
        frame(p).write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cutoff_slide.gif")], check=True)
    keys = [frame(p) for p in TABLE]
    for i, f in enumerate(keys):
        f.write_image(tmp / f"key{i}.png")
    keys = [Image.open(tmp / f"key{i}.png").convert("RGB") for i in range(4)]
    w, hh = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * hh + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (hh + 16)))
    sheet.save(HERE / "cutoff_slide_frames.png")
    shutil.rmtree(tmp)
