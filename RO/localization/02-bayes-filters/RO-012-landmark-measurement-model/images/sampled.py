"""200 poses drawn from the one reading of the pink pole (range 3.10 m, bearing 40 deg, noise 0.1 m and 5 deg):
they lie on a ring of radius about 3.1 m around the pole, and each one's heading (arrow) is set so that the pole
appears 40 deg to its left. The true pose A = (2, 2, 0) is drawn in black. Run -> sampled.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT
from lmmodel import LM, POSE_A, sample_poses

here = Path(__file__).parent
rng = np.random.default_rng(4)
x, y, th = sample_poses("pink", 200, rng)
fig = go.Figure()
fig.add_shape(type="rect", x0=0, x1=5, y0=0, y1=4, line=dict(color="#6B6B6B", width=4), fillcolor="rgba(0,0,0,0)")
L = 0.25
for a, b, t in zip(x, y, th):
    fig.add_trace(go.Scatter(x=[a, a + L * np.cos(t)], y=[b, b + L * np.sin(t)], mode="lines",
                             line=dict(color="#E377C2", width=1.5)))
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color="#E377C2", size=5)))
fig.add_trace(go.Scatter(x=[LM["pink"][0]], y=[LM["pink"][1]], mode="markers+text", text=["pink pole  "],
                         textposition="middle left", marker=dict(size=18, color="#E377C2", line=dict(color="black", width=2))))
fig.add_trace(go.Scatter(x=[POSE_A[0], POSE_A[0] + 0.5], y=[POSE_A[1], POSE_A[1]], mode="lines+markers",
                         line=dict(color="black", width=4), marker=dict(size=[12, 1], color="black")))
fig.add_annotation(x=2.0, y=1.8, text="true pose A", showarrow=False, font_size=18)
fig.add_annotation(x=2.5, y=0.6, text="room", showarrow=False, font_size=18, font_color="#6B6B6B")
fig.update_layout(template="simple_white", width=950, height=820, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=20, b=60))
fig.update_xaxes(title="x (m)", range=[0.9, 7.9], dtick=1, scaleanchor="y")
fig.update_yaxes(title="y (m)", range=[0.4, 7.2], dtick=1)
fig.write_image(here / "sampled.png")
