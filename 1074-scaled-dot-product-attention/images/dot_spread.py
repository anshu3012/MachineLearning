"""Histograms of 1000 dot products q.k for d = 3, 100, 1000, before and after dividing by sqrt(d) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "dot_products.csv")
fig = make_subplots(1, 2, subplot_titles=["q·k", "q·k / √d"], horizontal_spacing=0.08)
for d, c in ((1000, RED), (100, ORANGE), (3, BLUE)):
    s = a[a.d == d]
    for col, k in (("dot", 1), ("scaled", 2)):
        fig.add_trace(go.Histogram(x=s[col], name=f"d = {d}", marker_color=c, opacity=0.6, showlegend=k == 1,
                                   xbins=dict(size=2 if k == 1 else 0.25), legendgroup=str(d)), 1, k)
fig.update_layout(template="simple_white", barmode="overlay", width=1000, height=420, font=FONT,
                  legend=dict(x=0.36, y=0.98), margin=dict(l=60, r=20, t=40, b=55))
fig.update_xaxes(title_text="dot product", row=1, col=1, range=[-110, 110])
fig.update_xaxes(title_text="scaled dot product", row=1, col=2, range=[-5, 5])
fig.update_yaxes(title_text="count of pairs", row=1, col=1)
fig.write_image(here / "dot_spread.png", scale=2)
fig.write_image(here / "dot_spread.pdf")
