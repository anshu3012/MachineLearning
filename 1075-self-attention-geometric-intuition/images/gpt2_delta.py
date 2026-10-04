"""GPT-2 small, last token "bank" of two real sentences: the size of the change each attention block adds,
|Δe| / |e|, block by block (log scale). Data: data/gpt2_delta.csv (Notebook).
Run: python gpt2_delta.py -> gpt2_delta.png (Plotly)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "gpt2_delta.csv")
fig = go.Figure()
for (s, g), c in zip(d.groupby("sentence", sort=False), (ORANGE, BLUE)):
    fig.add_trace(go.Scatter(x=g.block, y=g.ratio, mode="lines+markers", name=f'"{s}"',
                             line=dict(color=c, width=3), marker=dict(size=10)))
fig.add_hline(y=1, line=dict(color=GREY, dash="dot"))
fig.add_annotation(x=6.5, y=-1.3, text="blocks 2 to 11: the change is 9 to 25 percent of the vector's length",
                   showarrow=False, font=dict(size=18))
fig.add_annotation(x=1, y=0.8, text="block 1: the change is about<br>6 times the vector's length", showarrow=True, ax=70, ay=40,
                   font=dict(size=16), xanchor="left")
fig.update_layout(template="simple_white", width=900, height=520, font=dict(FONT, size=19),
                  xaxis=dict(title="attention block", dtick=1),
                  yaxis=dict(title="|Δe| / |e|  (log scale)", type="log", range=[-1.5, 1.0], tickvals=[0.05, 0.1, 0.2, 0.5, 1, 2, 5]),
                  legend=dict(x=0.42, y=0.75), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(HERE / "gpt2_delta.png", scale=2)
