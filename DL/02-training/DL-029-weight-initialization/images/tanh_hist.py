"""Histograms of tanh activations through three 500-node layers, small vs large random weights (Plotly). PNG only: the vector PDF drops the thin bars."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "tanh_hist.csv.gz")
titles = ["input"] + [f"hidden layer {i}" for i in (1, 2, 3)]
fig = make_subplots(rows=2, cols=4, subplot_titles=titles * 2, horizontal_spacing=0.05, vertical_spacing=0.2)
for r, (w, col) in enumerate((("small", BLUE), ("large", RED)), start=1):
    for c in range(4):
        v = h[(h.weights == w) & (h.layer == c)].value
        xb = dict(start=-4, end=4, size=0.2) if c == 0 else dict(start=-1.1, end=1.1, size=0.04)
        fig.add_trace(go.Histogram(x=v, xbins=xb, marker_color=GREY if c == 0 else col, showlegend=False,
                                   histnorm="probability"), r, c + 1)
        fig.update_xaxes(range=[-4, 4] if c == 0 else [-1.1, 1.1], row=r, col=c + 1)
        fig.update_yaxes(showticklabels=False, row=r, col=c + 1)
fig.update_yaxes(title_text="weights 0.01 x randn", row=1, col=1)
fig.update_yaxes(title_text="weights 1 x randn", row=2, col=1)
fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, bargap=0.02,
                  margin=dict(l=60, r=20, t=50, b=40))
fig.update_annotations(font=dict(family=FONT["family"], size=17))
fig.write_image(here / "tanh_hist.png", scale=2)
