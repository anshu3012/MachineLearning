"""Overview: the robot of RO-001 at (2, 1, 30 deg) drives v = 0.5 m/s, omega = 1 rad/s for 1 s. Dashed: the arc the
kinematic model predicts, ending at (2.249, 1.409). Dots with ticks: 300 end poses sampled from the odometry motion
model (each tick shows the end heading). Seeded. Run: python drive_cloud.py -> drive_cloud.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from motion import ODO_END, START, odo_deltas, sample_odometry
from robotdraw import robot

here = Path(__file__).parent
rng = np.random.default_rng(1)
u = (0.500, 0.479, 0.500)
xs, ys, ts = sample_odometry(u, START, rng, 300)
fig = go.Figure()
t = np.linspace(START[2], START[2] + 1, 60)
fig.add_trace(go.Scatter(x=1.75 + 0.5 * np.sin(t), y=1.433 - 0.5 * np.cos(t), mode="lines",
                         line=dict(color=GREY, dash="dash", width=2)))
lx, ly = [], []
for x, y, th in zip(xs, ys, ts):
    lx += [x, x + 0.04 * np.cos(th), None]
    ly += [y, y + 0.04 * np.sin(th), None]
fig.add_trace(go.Scatter(x=lx, y=ly, mode="lines", line=dict(color=BLUE, width=1), opacity=0.6))
fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=4, color=BLUE)))
for tr in robot(START, scale=0.35):
    fig.add_trace(tr)
fig.add_trace(go.Scatter(x=[ODO_END[0]], y=[ODO_END[1]], mode="markers", marker=dict(size=14, color=RED, symbol="x")))
fig.add_annotation(x=2.0, y=0.88, text="start (2, 1), 30°", showarrow=False, font=dict(size=18))
fig.add_annotation(x=ODO_END[0], y=ODO_END[1], ax=2.5, ay=1.15, axref="x", ayref="y", arrowhead=2, arrowcolor=RED,
                   text="model's end<br>(2.249, 1.409)", showarrow=True, font=dict(size=18, color=RED))
fig.add_annotation(x=1.85, y=1.66, text="300 possible end poses<br>(dot = position, tick = heading)", showarrow=False,
                   font=dict(size=18, color=BLUE))
fig.update_xaxes(range=[1.55, 2.75], dtick=0.25, title="x (m)", showgrid=True, gridcolor="#eee")
fig.update_yaxes(range=[0.8, 1.8], dtick=0.25, title="y (m)", showgrid=True, gridcolor="#eee", scaleanchor="x")
fig.update_layout(template="simple_white", width=900, height=780, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70),
                  title=dict(text="v = 0.5 m/s, ω = 1 rad/s for 1 s: where does the robot end up?", x=0.5,
                             font=dict(size=22)))
fig.write_image(here / "drive_cloud.png")
