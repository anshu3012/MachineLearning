"""How long are IMDB reviews? A histogram of the 25,000 training reviews (in words), with the median and the
longest review marked. Plotly: a data chart from the Notebook's CSV."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
L = pd.read_csv(here.parent / "data" / "imdb_lengths.csv").query("split == 'train'").length
med, top = float(np.median(L)), int(L.max())
assert (med, top) == (178.0, 2494)
fig = go.Figure(go.Histogram(x=L, xbins=dict(start=0, end=2500, size=25), marker_color=BLUE, showlegend=False))
for x, label, c in ((med, f"median {med:.0f} words", GREY), (top, f"longest {top:,} words", RED)):
    fig.add_vline(x=x, line=dict(color=c, width=3, dash="dash"))
    fig.add_annotation(x=x, y=1, yref="paper", text=label, showarrow=False, xanchor="left" if x < 1000 else "right",
                       xshift=6 if x < 1000 else -6, font=dict(color=c, size=18))
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT, bargap=0.05,
                  xaxis=dict(title="review length (words)", range=[0, 2550]), yaxis=dict(title="number of reviews"),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "imdb_lengths.png", scale=2)
fig.write_image(here / "imdb_lengths.pdf")
