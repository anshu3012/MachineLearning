"""BERT-base, layer 1: the singular values of each head's value map W_V^i W_O^i (768 x 768), largest first.
Exactly 64 are non-zero; the 65th falls to rounding-error size. Data: data/bert_value_svals.csv (Notebook).
Run: python value_rank.py -> value_rank.png (Plotly)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, FONT

HERE = Path(__file__).parent
sv = pd.read_csv(HERE.parent / "data" / "bert_value_svals.csv")
fig = go.Figure()
for h, g in sv.groupby("head"):
    fig.add_trace(go.Scatter(x=g.k, y=g.singular_value, mode="lines", line=dict(color=BLUE, width=1.5),
                             opacity=0.6, showlegend=False))
fig.add_vline(x=64.5, line=dict(color=RED, dash="dash", width=2))
fig.add_annotation(x=64.5, y=-2, text="64 = the head's size", showarrow=False, xanchor="left", xshift=8,
                   font=dict(color=RED, size=19))
fig.add_annotation(x=80, y=-6.4, text="rounding errors only", showarrow=False, font=dict(color=GREY, size=18))
fig.update_layout(template="simple_white", width=900, height=500, font=dict(FONT, size=19),
                  xaxis=dict(title="singular value number (largest first)", range=[0, 97]),
                  yaxis=dict(title="singular value (log scale)", type="log", exponentformat="power"),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(HERE / "value_rank.png", scale=2)
