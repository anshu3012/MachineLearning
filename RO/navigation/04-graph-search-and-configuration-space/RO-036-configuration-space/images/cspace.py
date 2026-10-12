"""The configuration space of the floor robot drawn as a box: x (0 to 7 m) and y (0 to 4 m) across the room's floor,
heading theta upward from 0 to 2 pi. The robot at (2, 1, 0.524) is one point; the same spot facing the other way,
(2, 1, 3.142), is the point straight above it. The top and bottom faces are the same headings (theta = 2 pi is
theta = 0). Copied from the RO-005 draft and resized to the room. Run: python cspace.py -> cspace.png, cspace.pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
X, Y, T = 7, 4, 2 * np.pi
fig = go.Figure()
edges = [((0, 0, 0), (X, 0, 0)), ((X, 0, 0), (X, Y, 0)), ((X, Y, 0), (0, Y, 0)), ((0, Y, 0), (0, 0, 0)),
         ((0, 0, T), (X, 0, T)), ((X, 0, T), (X, Y, T)), ((X, Y, T), (0, Y, T)), ((0, Y, T), (0, 0, T)),
         ((0, 0, 0), (0, 0, T)), ((X, 0, 0), (X, 0, T)), ((X, Y, 0), (X, Y, T)), ((0, Y, 0), (0, Y, T))]
for a, b in edges:
    fig.add_trace(go.Scatter3d(x=[a[0], b[0]], y=[a[1], b[1]], z=[a[2], b[2]], mode="lines",
                               line=dict(color=GREY, width=3)))
for z, c in ((0, "rgba(76,120,168,0.25)"), (T, "rgba(76,120,168,0.25)")):
    fig.add_trace(go.Mesh3d(x=[0, X, X, 0], y=[0, 0, Y, Y], z=[z] * 4, i=[0, 0], j=[1, 2], k=[2, 3], color=BLUE,
                            opacity=0.18))
q = (2, 1, np.radians(30))
fig.add_trace(go.Scatter3d(x=[q[0]], y=[q[1]], z=[q[2]], mode="markers+text", marker=dict(size=7, color=RED),
                           text=["  the robot: (2, 1, 0.524)"], textposition="middle right",
                           textfont=dict(size=19, color=RED)))
fig.add_trace(go.Scatter3d(x=[q[0], q[0]], y=[q[1], q[1]], z=[0, q[2]], mode="lines",
                           line=dict(color=RED, width=4, dash="dash")))
q2 = (2, 1, np.pi)                                           # same spot, facing the other way: another point
fig.add_trace(go.Scatter3d(x=[q2[0]], y=[q2[1]], z=[q2[2]], mode="markers+text", marker=dict(size=7, color=BLUE),
                           text=["  same spot, facing backward: (2, 1, 3.142)"], textposition="middle right",
                           textfont=dict(size=19, color=BLUE)))
fig.add_trace(go.Scatter3d(x=[q[0], q[0]], y=[q[1], q[1]], z=[q[2], q2[2]], mode="lines",
                           line=dict(color=GREY, width=3, dash="dot")))
fig.update_layout(scene=dict(xaxis=dict(title="x (m)", range=[0, X], dtick=1, tickfont=dict(size=15)),
                             yaxis=dict(title="y (m)", range=[0, Y], dtick=1, tickfont=dict(size=15)),
                             zaxis=dict(title="θ (rad)", range=[0, T], tickvals=[0, np.pi, T], ticktext=["0", "π", "2π"],
                                        tickfont=dict(size=16)),
                             aspectmode="manual", aspectratio=dict(x=1.6, y=0.95, z=1.0),
                             camera=dict(eye=dict(x=1.55, y=-2.05, z=1.05), center=dict(x=0, y=0, z=-0.08))),
                  font=FONT, width=900, height=780, showlegend=False, margin=dict(l=0, r=0, t=70, b=0),
                  title=dict(x=0.5, y=0.96, font=dict(size=21), text="each point is one configuration; the top face (θ = 2π) is the same as the bottom face (θ = 0)"))
fig.write_image(here / "cspace.png")
fig.write_image(here / "cspace.pdf")
