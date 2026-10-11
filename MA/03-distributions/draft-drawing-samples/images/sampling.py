"""Drawing samples. Left: 20 000 uniform numbers in [-b, b], b = 0.1. Middle: half the sum of 12 of them, with the
normal density of standard deviation b on top. Right: sqrt(6)/2 times the sum of 2 of them, with the triangular
density of standard deviation b on top. Seeded. Run: python sampling.py -> sampling.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED
from plotly.subplots import make_subplots

here = Path(__file__).parent
b, n = 0.1, 20_000
rng = np.random.default_rng(3)
U = rng.uniform(-b, b, size=(12, n))
uni = U[0]
nor = 0.5 * U.sum(axis=0)
tri = np.sqrt(6) / 2 * (U[0] + U[1])
assert abs(nor.std() - b) < 0.003 and abs(tri.std() - b) < 0.003
x = np.linspace(-0.4, 0.4, 400)
fn = np.exp(-0.5 * (x / b) ** 2) / np.sqrt(2 * np.pi * b * b)
ft = np.maximum(0, 1 / (np.sqrt(6) * b) - np.abs(x) / (6 * b * b))
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                    subplot_titles=["1 uniform number", "half the sum of 12", "√6/2 × the sum of 2"])
for c, (s, f) in enumerate([(uni, np.where(np.abs(x) <= b, 1 / (2 * b), 0)), (nor, fn), (tri, ft)], start=1):
    fig.add_trace(go.Histogram(x=s, histnorm="probability density", xbins=dict(start=-0.4, end=0.4, size=0.01),
                               marker_color=BLUE, opacity=0.75), 1, c)
    fig.add_trace(go.Scatter(x=x, y=f, mode="lines", line=dict(color=RED, width=3)), 1, c)
    fig.update_xaxes(range=[-0.4, 0.4], dtick=0.2, title="value", row=1, col=c)
    fig.update_yaxes(range=[0, 5.6], row=1, col=c)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, showlegend=False, bargap=0,
                  margin=dict(l=80, r=30, t=110, b=70),
                  title=dict(text="20 000 samples each (blue) against the target density (red), b = 0.1", x=0.5,
                             y=0.95, font=dict(size=22)))
fig.update_annotations(font_size=20)
fig.write_image(here / "sampling.png")
