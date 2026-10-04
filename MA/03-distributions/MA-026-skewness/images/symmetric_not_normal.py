"""Skewness near 0 does not mean normal: 10,000 values each from a normal, a uniform and a symmetric two-humped
distribution all have sample skewness close to 0, yet only the first is normal."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(0)
data = {"normal": rng.normal(0, 1, 10000), "uniform": rng.uniform(-2, 2, 10000),
        "two humps": np.r_[rng.normal(-2, 0.6, 5000), rng.normal(2, 0.6, 5000)]}
sk = {k: pd.Series(v).skew() for k, v in data.items()}
assert all(abs(v) < 0.05 for v in sk.values()), sk
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06, subplot_titles=[f"{k}: skewness {v:+.2f}" for k, v in sk.items()])
for j, v in enumerate(data.values(), start=1):
    fig.add_histogram(x=v, xbins=dict(start=-4, end=4, size=0.2), histnorm="probability density",
                      marker_color="#4C78A8" if j == 1 else "#9a9a9a", row=1, col=j)
    fig.update_xaxes(range=[-4, 4], row=1, col=j)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1400, height=460, showlegend=False, bargap=0.02,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=60, r=20, t=60, b=50))
fig.write_image(here / "symmetric_not_normal.png", scale=2)
fig.write_image(here / "symmetric_not_normal.pdf")
