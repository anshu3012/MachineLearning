"""Attention-weight heatmaps (Plotly): the two short phrases, and a real IMDB review with fixed vs learned weights."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
data = here.parent / "data"


def pair(csv, titles, out, width, height, size):
    w = pd.read_csv(data / csv, index_col=[0, 1])
    keys = list(dict.fromkeys(w.index.get_level_values(0)))
    fig = make_subplots(1, 2, subplot_titles=titles, horizontal_spacing=0.16)
    for c, k in enumerate(keys, 1):
        m = w.loc[k]
        cols = [x.split(".")[0] for x in m.columns]
        fig.add_trace(go.Heatmap(z=m.values, x=cols, y=list(m.index), colorscale="Blues", zmin=0, zmax=1,
                                 text=m.values.round(2), texttemplate="%{text}", textfont=dict(size=size),
                                 showscale=(c == 2), colorbar=dict(title="weight")), 1, c)
        fig.update_yaxes(autorange="reversed", title="query word (row)" if c == 1 else None, row=1, col=c)
        fig.update_xaxes(title="word it attends to", side="bottom", row=1, col=c)
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, margin=dict(l=90, r=20, t=50, b=70))
    fig.write_image(here / f"{out}.png", scale=2)
    fig.write_image(here / f"{out}.pdf")


pair("weights_simple.csv", ["money bank grows", "river bank flows"], "weights_simple", 950, 430, 18)
pair("weights_review.csv", ["fixed: no parameters", "learned W_Q, W_K, W_V"], "weights_review", 1150, 560, 11)
