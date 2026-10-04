"""Section 6: where one encoder block's 3,152,384 parameters sit (d_model 512, d_ff 2048), from data/param_counts.csv
(formula and Keras count, the Notebook). Two-thirds are in the feed-forward network.
Run: python param_share.py  -> param_share.png (Plotly horizontal stacked bar)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, GREEN, ORANGE

HERE = Path(__file__).parent
p = pd.read_csv(HERE.parent / "data" / "param_counts.csv", index_col=0)["Keras"]
assert p["one block"] == 3152384 and p["6 blocks"] == 18914304
assert round(p["feed-forward network"] / p["one block"], 3) == 0.666

fig = go.Figure()
for part, c in (("multi-head attention", BLUE), ("feed-forward network", ORANGE), ("two layer norms", GREEN)):
    share = p[part] / p["one block"]
    fig.add_trace(go.Bar(y=["one block"], x=[p[part]], orientation="h", name=f"{part}: {p[part]:,}", marker_color=c,
                         text=f"{share:.1%}" if share > 0.05 else "", textposition="inside",
                         textfont=dict(size=26, color="white")))
fig.update_layout(template="simple_white", barmode="stack", width=1100, height=360,
                  font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="parameters of one encoder block: 3,152,384", x=0.5, y=0.95),
                  xaxis=dict(title="parameters", range=[0, 3.2e6]), yaxis=dict(visible=False),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.75, yanchor="top", traceorder="normal"),
                  margin=dict(l=20, r=30, t=60, b=150))

if __name__ == "__main__":
    fig.write_image(HERE / "param_share.png", scale=2)
