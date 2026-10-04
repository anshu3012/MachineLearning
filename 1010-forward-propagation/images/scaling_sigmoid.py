"""Why scale first: layer 1's three sums for the raw student (7.2, 72, 69, 81) and for the scaled one
(0.72, 0.72, 0.69, 0.81), placed on the sigmoid. Raw sums sit on the flat tails, scaled ones on the steep middle.
Run: python scaling_sigmoid.py -> scaling_sigmoid.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
W1 = np.array([[0.2, -0.3, 0.5], [0.4, 0.1, -0.2], [-0.5, 0.2, 0.1], [0.3, -0.4, 0.2]])
b1 = np.array([0.1, -0.1, 0.2])
sig = lambda z: 1 / (1 + np.exp(-z))
raw = np.array([7.2, 72, 69, 81])
scaled = raw / np.array([10, 100, 100, 100])
z_raw, z_sc = W1.T @ raw + b1, W1.T @ scaled + b1
assert np.allclose(z_raw, [20.1, -13.7, 12.5], atol=0.05)          # the Note's Extra box
assert np.allclose(z_sc, [0.430, -0.430, 0.647], atol=5e-4)       # Section 4.2
slope = lambda z: sig(z) * (1 - sig(z))
assert np.allclose(slope(z_raw), [1.9e-9, 1.1e-6, 3.7e-6], rtol=0.06)
z = np.linspace(-22, 22, 800)
fig = go.Figure(go.Scatter(x=z, y=sig(z), mode="lines", line=dict(color=GREY, width=3), name="sigmoid"))
fig.add_trace(go.Scatter(x=z_raw, y=sig(z_raw), mode="markers", marker=dict(size=18, color=RED, symbol="x"),
                         name="raw inputs (slope near 0)"))
fig.add_trace(go.Scatter(x=z_sc, y=sig(z_sc), mode="markers", marker=dict(size=16, color=BLUE),
                         name="scaled inputs (slope 0.23 to 0.24)"))
assert np.all(slope(z_sc) > 0.22)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=24),
                  xaxis=dict(title="sum z entering a layer-1 node"), yaxis=dict(title="σ(z)", range=[-0.05, 1.05]),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"), margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(HERE / "scaling_sigmoid.png", scale=2)
