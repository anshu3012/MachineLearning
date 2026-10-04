"""Cross-attention of the trained transformer, one French position per frame, for "Tom likes to eat ice cream.":
left, the weight grid filling row by row (current row outlined); right, the current query's weights over the
English words, whose keys and values come from the encoder. Mean of the 4 heads of the model's single decoder block.
Data: data/cross_weights.csv (Notebook). Run: python cross_fill.py -> cross_fill.gif, cross_fill_frames.png
(Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREY, RED, FONT

HERE = Path(__file__).parent
a = pd.read_csv(HERE.parent / "data" / "cross_weights.csv")
a = a[a.pair == 0]
W = a.pivot(index="query_pos", columns="key_pos", values="weight").values
Q = a.drop_duplicates("query_pos").sort_values("query_pos")
INP = [w.replace("<", "&lt;").replace(">", "&gt;") for w in Q["query"]]
PRED = [w.replace("<", "&lt;").replace(">", "&gt;") for w in Q.predicts]
EN = a.drop_duplicates("key_pos").sort_values("key_pos").key.tolist()
ROWS = [f"{i} → {p}" for i, p in zip(INP, PRED)]


def frame(t):
    Z = np.full(W.shape, np.nan)
    Z[:t + 1] = W[:t + 1]
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=("weights so far (row: decoder input → word it predicts)",
                                        f"query from the decoder: {INP[t]} (predicts {PRED[t]})"))
    fig.add_trace(go.Heatmap(z=Z, x=list(range(len(EN))), y=list(range(len(ROWS))), colorscale="Blues", zmin=0, zmax=1,
                             showscale=False, text=[["" if np.isnan(v) or v < 0.1 else f"{v:.2f}" for v in r] for r in Z],
                             texttemplate="%{text}", textfont=dict(size=13)), 1, 1)
    fig.add_shape(type="rect", x0=-0.5, x1=len(EN) - 0.5, y0=t - 0.5, y1=t + 0.5, line=dict(color=RED, width=3),
                  fillcolor="rgba(0,0,0,0)", row=1, col=1)
    fig.add_trace(go.Bar(x=EN, y=W[t], marker_color=BLUE, text=[f"{v:.2f}" if v >= 0.01 else "" for v in W[t]],
                         textposition="outside"), 1, 2)
    fig.update_xaxes(tickvals=list(range(len(EN))), ticktext=EN, title="English word (keys and values from the encoder)",
                     row=1, col=1)
    fig.update_yaxes(tickvals=list(range(len(ROWS))), ticktext=ROWS, autorange="reversed", row=1, col=1)
    fig.update_yaxes(range=[0, 1.15], title="weight", row=1, col=2)
    fig.update_layout(template="simple_white", width=1250, height=600, font=dict(FONT, size=16), showlegend=False,
                      margin=dict(l=150, r=20, t=80, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cf_frames"
    tmp.mkdir(exist_ok=True)
    n = len(ROWS)
    for t in range(n):
        frame(t).write_image(tmp / f"{t:03d}.png")
    for k in range(n, n + 3):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cross_fill.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (2, n - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (w_, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h_ + 16)))
    sheet.save(HERE / "cross_fill_frames.png")
    shutil.rmtree(tmp)
