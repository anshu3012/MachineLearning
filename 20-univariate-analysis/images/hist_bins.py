"""Histogram of Titanic ages with three bin widths: too few bins hide the shape, too many make it noisy."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna()
widths = [16, 5, 1]
fig = make_subplots(1, 3, subplot_titles=[f"{80 // w} bins, {w} year{"s" if w > 1 else ""} wide" for w in widths],
                    horizontal_spacing=0.07)
for i, w in enumerate(widths, start=1):
    fig.add_trace(go.Histogram(x=age, xbins=dict(start=0, end=80.001, size=w),
                               marker=dict(color="#4C78A8", line=dict(color="white", width=1 if w > 1 else 0.5))), 1, i)
    fig.update_xaxes(title="Age (years)", range=[0, 82], row=1, col=i)
fig.update_yaxes(title="Passengers", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=420, showlegend=False, bargap=0,
                  font=dict(family="Latin Modern Roman", size=22), margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=22)
fig.write_image(here / "hist_bins.png", scale=2)
fig.write_image(here / "hist_bins.pdf")
