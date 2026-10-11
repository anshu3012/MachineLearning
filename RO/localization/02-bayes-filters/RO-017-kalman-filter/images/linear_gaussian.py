"""A linear function keeps a normal distribution normal. x ~ N(1, 0.5^2) passed through y = 2x + 1 gives
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
# Equal scales, so the picture shows the stretch: one unit of x and of y take the same length (the line rises 2 for
# every 1 across, and y's curve is visibly twice as wide), and both density panels share one scale (y's peak is half
# as high). Plot area 580 x 890 px: 3u + 20 + d = 580 and 6u + 20 + d = 890 give u = 103 px per unit, d = 250 px.
W, H, L, R, T, B = 700, 1000, 90, 30, 30, 80
fx, fy = 310 / 580, 620 / 890                      # main panel: 3 units wide, 6 units tall
gx, gy_ = 330 / 580, 640 / 890                     # where the density panels start (20 px gap)
fig = go.Figure()
g = np.linspace(-0.5, 2.5, 300)
gy = np.linspace(0, 6, 300)
fig.add_trace(go.Histogram(x=x, histnorm="probability density", marker_color=BLUE, opacity=0.4, nbinsx=50,
                           xaxis="x2", yaxis="y2"))
fig.add_trace(go.Scatter(x=g, y=normal(g, 1, 0.25), line=dict(color=BLUE, width=4), xaxis="x2", yaxis="y2"))
fig.add_trace(go.Scatter(x=g, y=2 * g + 1, line=dict(color="black", width=4)))
fig.add_trace(go.Scatter(x=x[:300], y=y[:300], mode="markers", marker=dict(color=GREY, size=5, opacity=0.5)))
fig.add_trace(go.Histogram(y=y, histnorm="probability density", marker_color=ORANGE, opacity=0.4, nbinsy=50,
                           xaxis="x3", yaxis="y3"))
fig.add_trace(go.Scatter(x=normal(gy, 3, 1), y=gy, line=dict(color=ORANGE, width=4), xaxis="x3", yaxis="y3"))
dens = [0, 0.9]
fig.update_layout(
    xaxis=dict(domain=[0, fx], range=[-0.5, 2.5], title="x", dtick=0.5),
    yaxis=dict(domain=[0, fy], range=[0, 6], title="y", dtick=1),
    xaxis2=dict(domain=[0, fx], range=[-0.5, 2.5], anchor="y2", matches="x", showticklabels=False),
    yaxis2=dict(domain=[gy_, 1], range=dens, anchor="x2", title="density", dtick=0.2),
    xaxis3=dict(domain=[gx, 1], range=dens, anchor="y3", title="density", tickvals=[0.2, 0.4, 0.6, 0.8]),
    yaxis3=dict(domain=[0, fy], range=[0, 6], anchor="x3", matches="y", showticklabels=False),
    template="simple_white", font=FONT, width=W, height=H, showlegend=False, bargap=0.05,
    margin=dict(l=L, r=R, t=T, b=B))
fig.add_annotation(x=1.55, y=0.85, text="x: mean 1, sd 0.5", showarrow=False, font=dict(size=19, color=BLUE),
                   xanchor="left", xref="x2", yref="y2")
fig.add_annotation(x=-0.4, y=5.6, text="y = 2x + 1", showarrow=False, font=dict(size=21), xref="x", yref="y",
                   xanchor="left")
fig.add_annotation(x=0.05, y=5.7, text="y: mean 3, sd 1", showarrow=False, font=dict(size=19, color=ORANGE),
                   xref="x3", yref="y3", xanchor="left")
fig.write_image(here / "linear_gaussian.png")
