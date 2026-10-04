"""Note 74, Section 2 (Plotly): e^(-z) with tangent lines at z = 0 and z = 1. Each tangent's slope is -e^(-z):
the curve's own height with a minus sign.  Run: python exp_slope.py -> exp_slope.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
z = np.linspace(-1, 3, 300)
fig = go.Figure(go.Scatter(x=z, y=np.exp(-z), mode="lines", line=dict(color=BLUE, width=4, simplify=False), name="e<sup>−z</sup>"))
h = 1e-6
for z0 in (0, 1):
    slope = (np.exp(-(z0 + h)) - np.exp(-(z0 - h))) / (2 * h)          # numerical slope
    assert abs(slope + np.exp(-z0)) < 1e-6                              # equals -e^(-z0)
    t = np.linspace(z0 - 0.9, z0 + 0.9, 2)
    fig.add_trace(go.Scatter(x=t, y=np.exp(-z0) + slope * (t - z0), mode="lines", line=dict(color=RED, width=3), showlegend=False))
    fig.add_trace(go.Scatter(x=[z0, z0], y=[0, np.exp(-z0)], mode="lines", line=dict(color=GREY, width=2, dash="dot"), showlegend=False))
    fig.add_trace(go.Scatter(x=[z0], y=[np.exp(-z0)], mode="markers+text", marker=dict(size=13, color=RED),
                             text=[f"z = {z0}: height {np.exp(-z0):.2f}, slope −{-slope:.2f}"], textposition="top right",
                             textfont=dict(size=19, color=RED), showlegend=False))
fig.update_layout(template="simple_white", width=950, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=60, r=20, t=30, b=60), xaxis=dict(title="z", range=[-1, 3]),
                  yaxis=dict(title="e<sup>−z</sup>", range=[0, 2.8]), legend=dict(x=0.8, y=0.95))
fig.write_image(HERE / "exp_slope.png", scale=2)
