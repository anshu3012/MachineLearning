"""Probability surface sigma(x1 + x2) (left) and the same surface seen from above, as a contour map (right), with the
line x1 + x2 = 0 (sigma = 0.5) marked on both (Plotly). Writes probability_map.png/.pdf."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from surface_tilt import surface_traces, scene

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
sig = lambda z: 1 / (1 + np.exp(-z))
xs = np.linspace(-4, 4, 161)
X1, X2 = np.meshgrid(xs, xs)
P = sig(X1 + X2)
CS = [[0, "#C9D9EC"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]]
tr, zf = surface_traces(xs, xs, P, (0.1, 0.9, 0.1), colorscale=CS)
tr.append(go.Scatter3d(x=[-4, 4], y=[4, -4], z=[0.5, 0.5], mode="lines", line=dict(color="black", width=7)))
tr.append(go.Scatter3d(x=[-4, 4], y=[4, -4], z=[zf, zf], mode="lines", line=dict(color="black", width=5)))
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], column_widths=[0.5, 0.5], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = σ(x₁ + x₂)", "the same surface seen from above"))
for t in tr:
    fig.add_trace(t, 1, 1)
fig.update_scenes(scene(xs, xs, P, zf, "x₁", "x₂", "P(placed)", (1.9, -1.1, 1.0), 3), row=1, col=1)
fig.add_trace(go.Contour(x=xs, y=xs, z=P, colorscale=CS, zmin=0, zmax=1,
                         contours=dict(start=0.1, end=0.9, size=0.1, showlabels=True, labelfont=dict(size=13)),
                         line=dict(width=1, color="#888888"), colorbar=dict(title="P(placed)", len=0.8)), 1, 2)
fig.add_trace(go.Scatter(x=[-4, 4], y=[4, -4], mode="lines", line=dict(color="black", width=4)), 1, 2)
fig.update_xaxes(title="x₁", range=[-4, 4], row=1, col=2)
fig.update_yaxes(title="x₂", range=[-4, 4], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=560, showlegend=False, font=font,
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "probability_map.png", scale=2)
fig.write_image(here / "probability_map.pdf")
