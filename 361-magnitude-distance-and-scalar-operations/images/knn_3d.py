"""Nearest-neighbour idea in 3D: five labelled vectors, a query vector [1, 1, 1], and the line to its nearest neighbour."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
X = np.array([[3, 1, 3], [5, 4, 5], [6, 5, 4], [1, 2, 1], [5, 6, 6]])   # five example vectors
y = np.array([0, 1, 1, 0, 1])                                         # their classes
q = np.array([1, 1, 1])                                               # the query vector
d = np.linalg.norm(X - q, axis=1)                                     # Euclidean distance to each
near = d.argmin()

fig = go.Figure()
for k, (name, col) in enumerate([("class 0", "#4C78A8"), ("class 1", "#F58518")]):
    m = y == k
    fig.add_trace(go.Scatter3d(x=X[m, 0], y=X[m, 1], z=X[m, 2], mode="markers+text", name=name,
                               text=[f"d = {v:.2f}" for v in d[m]], textposition="top center",
                               textfont=dict(size=14, color=col), marker=dict(size=8, color=col)))
fig.add_trace(go.Scatter3d(x=[q[0]], y=[q[1]], z=[q[2]], mode="markers", name="query [1, 1, 1]",
                           marker=dict(size=9, color="#54A24B", symbol="diamond")))
fig.add_trace(go.Scatter3d(x=[q[0], X[near, 0]], y=[q[1], X[near, 1]], z=[q[2], X[near, 2]], mode="lines",
                           name=f"nearest: distance {d[near]:.2f}, class {y[near]}", line=dict(color="#E45756", width=6)))
fig.update_layout(template="simple_white", width=900, height=650, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="The query takes the class of its nearest vector", x=0.5),
                  scene=dict(xaxis_title="x1", yaxis_title="x2", zaxis_title="x3",
                             xaxis=dict(range=[0, 7]), yaxis=dict(range=[0, 7]), zaxis=dict(range=[0, 7]),
                             camera=dict(eye=dict(x=1.6, y=-1.5, z=0.75), center=dict(x=0, y=0, z=-0.12)), aspectmode="cube"),
                  legend=dict(x=0.02, y=0.95), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "knn_3d.png", scale=2)
fig.write_image(here / "knn_3d.pdf")
print(dict(zip(range(5), d.round(2))), "nearest", near)
