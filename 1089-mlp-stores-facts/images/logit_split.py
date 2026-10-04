"""Exact split of logit(basketball) - logit(football) at the last position of "Michael Jordan plays the sport of"
in GPT-2 small: what each block's attention and MLP added to the stream, read through the final LayerNorm
(scale frozen at its value in this run). Data: data/logit_split_jordan.csv (Notebook).
Run: python logit_split.py -> logit_split.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import GREEN, ORANGE, FONT, DATA

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "logit_split_jordan.csv")
att = d[d.part.str.startswith("attn")].contribution.values
mlp = d[d.part.str.startswith("mlp")].contribution.values
blocks = list(range(1, 13))
fig = go.Figure([go.Bar(x=blocks, y=att, name="attention", marker_color=ORANGE),
                 go.Bar(x=blocks, y=mlp, name="MLP", marker_color=GREEN)])
fig.update_layout(template="simple_white", width=900, height=480, font=FONT, barmode="group",
                  xaxis=dict(title="block", dtick=1), yaxis=dict(title="push towards basketball<br>over football", zeroline=True),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=90, r=20, t=20, b=60))
fig.write_image(HERE / "logit_split.png", scale=2)
