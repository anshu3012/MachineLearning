"""The range part of the pink pole's reading (3.10 m, spread 0.1 m) over every robot position (x, y), drawn as a
surface: a ring-shaped ridge of radius 3.10 m around the pole at (4.4, 3.8), clipped to the room.
Run -> ring_surface.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT
from lmmodel import LM, POSE_A, range_density_xy

here = Path(__file__).parent
xs, ys = np.linspace(0, 5, 201), np.linspace(0, 4, 161)
X, Y = np.meshgrid(xs, ys)
Z = range_density_xy(X, Y, "pink")
fig = go.Figure(go.Surface(x=xs, y=ys, z=Z, colorscale="Magenta", cmin=0, cmax=4, colorbar=dict(title="per m", len=0.7)))
fig.add_trace(go.Scatter3d(x=[LM["pink"][0]], y=[LM["pink"][1]], z=[0], mode="markers+text", text=["pink pole"],
                           marker=dict(size=6, color="black"), textposition="top center", textfont=dict(size=16)))
fig.add_trace(go.Scatter3d(x=[POSE_A[0]], y=[POSE_A[1]], z=[4.3], mode="markers+text", text=["A (2, 2)"],
                           marker=dict(size=6, color="#4C78A8"), textposition="top center", textfont=dict(size=16)))
fig.update_layout(template="simple_white", width=1000, height=700, font=FONT, showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
                  scene=dict(xaxis=dict(title="x (m)", tickfont=dict(size=14)), yaxis=dict(title="y (m)", tickfont=dict(size=14)),
                             zaxis=dict(title="density", range=[0, 4.5], tickfont=dict(size=14)),
                             aspectratio=dict(x=1.25, y=1, z=0.5), camera=dict(eye=dict(x=0.35, y=-1.25, z=1.55))))
fig.write_image(here / "ring_surface.png")
