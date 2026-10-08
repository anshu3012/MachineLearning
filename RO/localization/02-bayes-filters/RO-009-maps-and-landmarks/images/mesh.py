"""The table as a 3D triangle mesh: its four corners at floor height 0 and at table height 0.75 m give 8 points;
2 triangles for the top, 2 for the bottom and 2 for each of the 4 sides make 12 triangles.
Run: python mesh.py -> mesh.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT
from roommap import TABLE

here = Path(__file__).parent
h = 0.75
P = np.array([(x, y, 0) for x, y in TABLE] + [(x, y, h) for x, y in TABLE])      # 0-3 bottom, 4-7 top
tri = [(0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7)]
for i in range(4):
    j = (i + 1) % 4
    tri += [(i, j, j + 4), (i, j + 4, i + 4)]
assert len(tri) == 12
I, J, K = zip(*tri)
fig = go.Figure(go.Mesh3d(x=P[:, 0], y=P[:, 1], z=P[:, 2], i=I, j=J, k=K, color=BLUE, opacity=0.35, flatshading=True))
ex, ey, ez = [], [], []
for t in tri:
    for a, b in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
        ex += [P[a, 0], P[b, 0], None]
        ey += [P[a, 1], P[b, 1], None]
        ez += [P[a, 2], P[b, 2], None]
fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", line=dict(color="black", width=4)))
fig.add_trace(go.Scatter3d(x=P[:, 0], y=P[:, 1], z=P[:, 2], mode="markers", marker=dict(size=5, color="black")))
fig.update_layout(template="simple_white", width=900, height=650, font=FONT, showlegend=False,
                  margin=dict(l=0, r=0, t=70, b=0),
                  title=dict(text="the table as 12 triangles on 8 corner points", x=0.5, font=dict(size=22)),
                  scene=dict(xaxis=dict(title="x (m)", tickfont=dict(size=13), dtick=1),
                             yaxis=dict(title="y (m)", tickfont=dict(size=13), dtick=1),
                             zaxis=dict(title="z (m)", tickfont=dict(size=13), range=[0, 1], dtick=0.5),
                             aspectmode="manual", aspectratio=dict(x=1.25, y=1, z=0.5),
                             camera=dict(eye=dict(x=1.3, y=-1.7, z=1.0))))
fig.write_image(here / "mesh.png")
