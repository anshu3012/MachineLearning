"""GELU (x times the standard normal CDF) next to ReLU. GPT-2 uses the tanh approximation `gelu_new`;
on [-6, 6] it differs from the exact GELU by at most 0.0005 (Notebook), invisible here.
Run: python gelu.py -> gelu.png"""
from math import erf, sqrt
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, GREY, FONT

HERE = Path(__file__).parent
x = np.linspace(-4, 3, 701)
gelu = np.array([0.5 * v * (1 + erf(v / sqrt(2))) for v in x])
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=np.maximum(x, 0), name="ReLU: max(0, x)", line=dict(color=GREY, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=x, y=gelu, name="GELU: x · Φ(x)", line=dict(color=BLUE, width=4, simplify=False)))
fig.add_annotation(x=-0.75, y=-0.17, text="lowest value −0.17 at x = −0.75", ax=-60, ay=-90, font=dict(size=18))
fig.update_layout(template="simple_white", width=820, height=480, font=FONT, legend=dict(x=0.03, y=0.97),
                  xaxis=dict(title="x", zeroline=True), yaxis=dict(title="output", zeroline=True, range=[-0.6, 3.1]),
                  margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(HERE / "gelu.png", scale=2)
