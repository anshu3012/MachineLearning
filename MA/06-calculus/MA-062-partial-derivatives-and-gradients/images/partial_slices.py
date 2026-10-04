"""The two partial derivatives of f(x1, x2) = x1^2 + x1 x2 + 2 x2^2 at (1, 1) as slopes (Plotly 3D).
Slice with x2 = 1 fixed (orange): tangent slope df/dx1 = 3. Slice with x1 = 1 fixed (green): slope df/dx2 = 5."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
g = np.linspace(-0.5, 2, 60)
A, B = np.meshgrid(g, g)
fig = go.Figure(go.Surface(x=A, y=B, z=f(A, B), colorscale="Blues", reversescale=True, showscale=False, opacity=0.35))
fig.add_trace(go.Scatter3d(x=g, y=np.ones_like(g), z=f(g, 1), mode="lines", line=dict(color=ORANGE, width=5)))
fig.add_trace(go.Scatter3d(x=np.ones_like(g), y=g, z=f(1, g), mode="lines", line=dict(color=GREEN, width=5)))
t = np.array([-0.7, 0.7])
fig.add_trace(go.Scatter3d(x=1 + t, y=[1, 1], z=4 + 3 * t, mode="lines", line=dict(color=ORANGE, width=10)))
fig.add_trace(go.Scatter3d(x=[1, 1], y=1 + t, z=4 + 5 * t, mode="lines", line=dict(color=GREEN, width=10)))
fig.add_trace(go.Scatter3d(x=[1], y=[1], z=[4], mode="markers", marker=dict(size=6, color="black")))
ann = [dict(x=1, y=1.7, z=7.5, text="slope 5 (x1 fixed)", xanchor="right", xshift=-8),
       dict(x=1.7, y=1, z=6.1, text="slope 3 (x2 fixed)", xanchor="left", xshift=8, yshift=6)]
for d, col in zip(ann, (GREEN, ORANGE)):
    d.update(showarrow=False, font=dict(color=col, size=20), bgcolor="white")
fig.update_scenes(annotations=ann)
fig.update_scenes(xaxis_title="x1", yaxis_title="x2", zaxis_title="f", camera=dict(eye=dict(x=1.25, y=-1.58, z=0.62), center=dict(x=0, y=0, z=-0.08)),
                  xaxis=dict(tickvals=[0, 1]), yaxis=dict(nticks=5), zaxis=dict(nticks=5))
fig.update_layout(template="simple_white", width=800, height=620, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=0, r=0, t=0, b=0))
fig.write_image(here / "partial_slices.png", scale=2)
fig.write_image(here / "partial_slices.pdf")
