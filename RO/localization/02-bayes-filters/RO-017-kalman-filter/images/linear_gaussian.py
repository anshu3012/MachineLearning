"""A straight-line function keeps a normal distribution normal. x ~ N(1, 0.5^2) passed through y = 2x + 1 gives
y ~ N(3, 1^2): the mean goes through the line, the standard deviation is multiplied by the slope 2.
5000 samples (histograms) agree with the formula curves. Run: python linear_gaussian.py -> linear_gaussian.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE
from kfsim import normal

here = Path(__file__).parent
x = np.random.default_rng(0).normal(1, 0.5, 5000)
y = 2 * x + 1
assert abs(y.mean() - 3) < 0.05 and abs(y.std() - 1) < 0.05
fig = make_subplots(rows=2, cols=2, column_widths=[0.72, 0.28], row_heights=[0.3, 0.7], shared_xaxes=True,
                    shared_yaxes=True, horizontal_spacing=0.02, vertical_spacing=0.03)
g = np.linspace(-1, 3, 300)
fig.add_trace(go.Histogram(x=x, histnorm="probability density", marker_color=BLUE, opacity=0.4, nbinsx=50), row=1, col=1)
fig.add_trace(go.Scatter(x=g, y=normal(g, 1, 0.25), line=dict(color=BLUE, width=4)), row=1, col=1)
fig.add_trace(go.Scatter(x=g, y=2 * g + 1, line=dict(color="black", width=4)), row=2, col=1)
fig.add_trace(go.Scatter(x=x[:300], y=y[:300], mode="markers", marker=dict(color=GREY, size=5, opacity=0.5)), row=2, col=1)
gy = np.linspace(-1, 7, 300)
fig.add_trace(go.Histogram(y=y, histnorm="probability density", marker_color=ORANGE, opacity=0.4, nbinsy=50), row=2, col=2)
fig.add_trace(go.Scatter(x=normal(gy, 3, 1), y=gy, line=dict(color=ORANGE, width=4)), row=2, col=2)
fig.add_annotation(x=1, y=0.95, text="x: mean 1, sd 0.5", showarrow=False, font=dict(size=19, color=BLUE),
                   xanchor="left", xref="x", yref="y", xshift=60)
fig.add_annotation(x=0.2, y=6.3, text="y = 2x + 1", showarrow=False, font=dict(size=21), xref="x3", yref="y3")
fig.add_annotation(x=0.2, y=6.8, text="y: mean 3, sd 1", showarrow=False, font=dict(size=19, color=ORANGE),
                   xref="x4", yref="y4", xanchor="left")
fig.update_xaxes(range=[-1, 3], row=2, col=1, title="x")
fig.update_yaxes(range=[-1, 7], row=2, col=1, title="y")
fig.update_yaxes(title="density", row=1, col=1)
fig.update_xaxes(title="density", row=2, col=2)
fig.update_layout(template="simple_white", font=FONT, width=950, height=800, showlegend=False,
                  margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "linear_gaussian.png")
