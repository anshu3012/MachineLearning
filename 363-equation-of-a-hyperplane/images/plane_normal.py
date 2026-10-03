"""A plane through the origin in 3D, w1 x1 + w2 x2 + w3 x3 = 0, with its normal vector w = [1, 2, 2]."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
w = np.array([1.0, 2.0, 2.0])
g = np.linspace(-2, 2, 25)
X1, X2 = np.meshgrid(g, g)
X3 = -(w[0] * X1 + w[1] * X2) / w[2]                          # solve w . x = 0 for x3
pts = np.array([[2, -1, 0], [0, 1, -1], [-2, 2, -1]])         # three points on the plane: w . x = 0
assert np.allclose(pts @ w, 0)

fig = go.Figure()
fig.add_trace(go.Surface(x=X1, y=X2, z=X3, colorscale=[[0, "#C9D6E8"], [1, "#C9D6E8"]], opacity=0.75,
                         showscale=False, name="plane"))
fig.add_trace(go.Scatter3d(x=[0, w[0]], y=[0, w[1]], z=[0, w[2]], mode="lines", line=dict(color="#F58518", width=9),
                           name="w = [1, 2, 2], perpendicular to the plane"))
fig.add_trace(go.Cone(x=[w[0]], y=[w[1]], z=[w[2]], u=[w[0]], v=[w[1]], w=[w[2]], sizemode="absolute", sizeref=0.6,
                      anchor="tip", colorscale=[[0, "#F58518"], [1, "#F58518"]], showscale=False, showlegend=False))
for i, p in enumerate(pts):
    fig.add_trace(go.Scatter3d(x=[0, p[0]], y=[0, p[1]], z=[0, p[2]], mode="lines+markers",
                               line=dict(color="#4C78A8", width=6), marker=dict(size=[0, 6], color="#4C78A8"),
                               name="vectors x in the plane (w · x = 0)", showlegend=(i == 0)))
fig.update_layout(template="simple_white", width=900, height=650, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="The plane x1 + 2 x2 + 2 x3 = 0 and its normal vector w", x=0.5),
                  scene=dict(xaxis_title="x1", yaxis_title="x2", zaxis_title="x3", aspectmode="cube",
                             xaxis=dict(range=[-3, 3]), yaxis=dict(range=[-3, 3]), zaxis=dict(range=[-3, 3]),
                             camera=dict(eye=dict(x=2.0, y=0.9, z=0.8), center=dict(x=0, y=0, z=-0.1))),
                  legend=dict(x=0.02, y=0.95), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "plane_normal.png", scale=2)
fig.write_image(here / "plane_normal.pdf")
