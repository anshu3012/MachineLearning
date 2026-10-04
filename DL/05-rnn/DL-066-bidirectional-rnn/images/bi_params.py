"""Section 5.2: the Bidirectional wrapper adds a second, separate copy of the layer for the backward direction, so the
recurrent parameters double. Counts from data/params.csv (Keras, 5 nodes, 32-number input, in the Notebook).
Run: python bi_params.py  -> bi_params.png (Plotly grouped bars)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, GREEN

HERE = Path(__file__).parent
p = pd.read_csv(HERE.parent / "data" / "params.csv").set_index("layer")
assert (p.bidirectional == 2 * p.unidirectional).all()
assert list(p.unidirectional) == [190, 760, 585] and list(p.dense_bi) == [11] * 3

fig = go.Figure()
for col, name, colour in (("unidirectional", "unidirectional", BLUE), ("bidirectional", "Bidirectional(...)", GREEN)):
    fig.add_trace(go.Bar(x=p.index, y=p[col], name=name, marker_color=colour, text=[f"{v:,}" for v in p[col]],
                         textposition="outside"))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="recurrent-layer parameters, 5 nodes, input of 32 numbers", x=0.5, y=0.97),
                  barmode="group", yaxis=dict(title="parameters", range=[0, 1750]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                  margin=dict(l=80, r=20, t=110, b=50))

if __name__ == "__main__":
    fig.write_image(HERE / "bi_params.png", scale=2)
