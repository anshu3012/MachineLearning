"""Histograms of 1000 dot products q.k for d = 3, 100, 1000 (one row each), before and after dividing by sqrt(d)
(Plotly). One row per d, so each histogram gets its own height scale and none crowds the others."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "dot_products.csv")
ds = ((3, BLUE), (100, ORANGE), (1000, RED))
fig = make_subplots(3, 2, shared_xaxes="columns", vertical_spacing=0.06, horizontal_spacing=0.1,
                    column_titles=["q·k", "q·k / √d"])
for r, (d, c) in enumerate(ds, 1):
    s = a[a.d == d]
    for col, k, size in (("dot", 1, 2), ("scaled", 2, 0.25)):
        fig.add_trace(go.Histogram(x=s[col], marker_color=c, showlegend=False, xbins=dict(size=size)), r, k)
    fig.update_yaxes(title_text=f"d = {d}", row=r, col=1)
fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, bargap=0.05,
                  margin=dict(l=70, r=20, t=40, b=55))
fig.update_xaxes(range=[-110, 110], col=1)
fig.update_xaxes(range=[-5, 5], col=2)
fig.update_xaxes(title_text="dot product", row=3, col=1)
fig.update_xaxes(title_text="scaled dot product", row=3, col=2)
fig.write_image(here / "dot_spread.png", scale=2)
fig.write_image(here / "dot_spread.pdf")
