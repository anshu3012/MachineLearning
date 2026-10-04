"""The weights of the simple self-attention for both phrases as a grid of dots: the area of each dot is the weight.
Rows are query words (each row sums to 1). Data: data/weights_simple.csv (Notebook).
Dot grid after Sanderson (3Blue1Brown), "Attention in transformers, step-by-step", 2024 (8:30-10:03).
Run: python weights_dots.py -> weights_dots.png (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

HERE = Path(__file__).parent
BLUE = "#4C78A8"
w = pd.read_csv(HERE.parent / "data" / "weights_simple.csv", index_col=[0, 1])
keys = list(dict.fromkeys(w.index.get_level_values(0)))
fig = make_subplots(1, 2, subplot_titles=[f'"{k}"' for k in keys], horizontal_spacing=0.14)
for c, k in enumerate(keys, 1):
    m = w.loc[k].dropna(axis=1, how="all")
    words = list(m.index)
    m = m[words]
    n = len(words)
    xs, ys = np.meshgrid(range(n), range(n))
    v = m.values
    fig.add_trace(go.Scatter(x=xs.ravel(), y=ys.ravel(), mode="markers+text", text=[f"{a:.2f}" for a in v.ravel()],
                             textposition="bottom center", textfont=dict(size=17),
                             marker=dict(size=np.sqrt(v.ravel()) * 95, color=BLUE, opacity=0.85, line=dict(width=0)),
                             showlegend=False), 1, c)
    fig.update_yaxes(autorange="reversed", tickvals=list(range(n)), ticktext=words, range=[n - 0.3, -0.6],
                     title="query word (row)" if c == 1 else None, showline=False, ticks="", row=1, col=c)
    fig.update_xaxes(tickvals=list(range(n)), ticktext=words, range=[-0.6, n - 0.4], side="top", showline=False,
                     ticks="", row=1, col=c)
fig.update_layout(template="simple_white", width=950, height=520, font=dict(FONT, size=20),
                  margin=dict(l=110, r=20, t=110, b=20))
fig.update_annotations(y=1.13, font=dict(size=21))
fig.write_image(HERE / "weights_dots.png", scale=2)
