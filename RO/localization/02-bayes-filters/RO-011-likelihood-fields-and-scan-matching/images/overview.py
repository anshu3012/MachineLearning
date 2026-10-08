"""The room of the beam-model Note with a box, the robot at pose A = (2, 2, 0) and its 12-beam scan.
Each beam ends at its reading (dot); the forward beam stops at the person, 1 m ahead. Run -> overview.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from fieldmodel import ANGLES, POSE_A, endpoints, scan_A
from gifkit import BLUE, FONT, ORANGE, RED
from roomdraw import robot_marker, room_shapes

here = Path(__file__).parent
z = scan_A()
px, py = endpoints(POSE_A, z)
fig = go.Figure()
room_shapes(fig)
for a, b in zip(px, py):
    fig.add_trace(go.Scatter(x=[2, a], y=[2, b], mode="lines", line=dict(color=RED, width=2)))
fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(color=RED, size=12)))
fig.add_trace(robot_marker(POSE_A))
fig.add_trace(go.Scatter(x=[3.12], y=[2], mode="markers", marker=dict(color=ORANGE, size=22)))
fig.add_annotation(x=3.12, y=2.18, text="person", showarrow=False, font=dict(color=ORANGE, size=20))
fig.add_annotation(x=3.9, y=0.9, text="box", showarrow=False, font=dict(size=20))
fig.add_annotation(x=2.0, y=1.75, text="robot A (2, 2, 0)", showarrow=False, font=dict(color=BLUE, size=19))
fig.update_layout(template="simple_white", width=820, height=680, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=20, b=60))
fig.update_xaxes(title="x (m)", range=[-0.3, 5.3], dtick=1, scaleanchor="y")
fig.update_yaxes(title="y (m)", range=[-0.3, 4.3], dtick=1)
fig.write_image(here / "overview.png")
