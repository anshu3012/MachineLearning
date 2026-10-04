"""The trained attention model writing "elle lui conseilla de parler de sa vie en amérique ." one French word per frame:
left, the weight grid filling row by row (the current row outlined); right, the weights of the current word over the
English words, and the context vector they build. Data: data/attention_weights.csv (Notebook).
Run: python attention_fill.py -> attention_fill.gif, attention_fill_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import FONT

HERE = Path(__file__).parent
ORANGE, RED, GREY = "#F58518", "#E45756", "#6B6B6B"
w = pd.read_csv(HERE.parent / "data" / "attention_weights.csv", index_col=0, keep_default_na=False)
EN, FR = list(w.columns), list(w.index)
cols = [c + "​" * j for j, c in enumerate(EN)]
rows = [r.replace("<", "&lt;") + "​" * i for i, r in enumerate(FR)]
W = w.values


def frame(t):
    Z = np.full(W.shape, np.nan)
    Z[:t + 1] = W[:t + 1]
    fig = make_subplots(1, 2, column_widths=[0.56, 0.44], horizontal_spacing=0.1,
                        subplot_titles=("weights so far (one row per French word)",
                                        f'writing "{FR[t]}": weights α over the English words'))
    fig.add_trace(go.Heatmap(z=Z, x=cols, y=rows, colorscale="Oranges", zmin=0, zmax=1, showscale=False,
                             text=[["" if np.isnan(v) or v < 0.005 else f"{v:.2f}" for v in r] for r in Z],
                             texttemplate="%{text}", textfont=dict(size=11)), 1, 1)
    fig.add_shape(type="rect", x0=-0.5, x1=len(EN) - 0.5, y0=t - 0.5, y1=t + 0.5, line=dict(color=RED, width=3), fillcolor="rgba(0,0,0,0)",
                  row=1, col=1)
    fig.add_trace(go.Bar(x=W[t], y=cols, orientation="h", marker_color=ORANGE,
                         text=[f"{v:.2f}" if v >= 0.01 else "" for v in W[t]], textposition="outside"), 1, 2)
    top = np.argsort(W[t])[::-1][:3]
    terms = " + ".join(f"{W[t, j]:.2f} h<sub>{EN[j]}</sub>" for j in top if W[t, j] >= 0.01)
    fig.add_annotation(xref="paper", yref="paper", x=1.0, y=-0.2, xanchor="right", showarrow=False,
                       text=f"context vector c<sub>{t + 1}</sub> ≈ {terms} + …", font=dict(size=18, color=GREY))
    fig.update_yaxes(autorange="reversed", row=1, col=1)
    fig.update_yaxes(autorange="reversed", row=1, col=2)
    fig.update_xaxes(side="top", tickangle=-35, row=1, col=1)
    fig.update_xaxes(range=[0, 1.2], title="weight α", row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=700, font=dict(FONT, size=16), showlegend=False,
                      margin=dict(l=110, r=30, t=150, b=110))
    for a in fig.layout.annotations[:2]:
        a.y = 1.17
    return fig


if __name__ == "__main__":
    tmp = HERE / ".fill_frames"
    tmp.mkdir(exist_ok=True)
    n = len(FR)
    for t in range(n):
        frame(t).write_image(tmp / f"{t:03d}.png")
    for k in range(n, n + 3):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "attention_fill.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (4, n - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (w_, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h_ + 16)))
    sheet.save(HERE / "attention_fill_frames.png")
    shutil.rmtree(tmp)
