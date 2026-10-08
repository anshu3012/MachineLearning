"""Pushing a pose belief through the robot's motion (the kinematic model of the pose Note). Start pose (2, 1, 30 deg)
with standard deviations 0.1 m in x and y and 0.3 rad in heading; drive 1 m straight. 3000 sampled poses end on a
curved band (a banana); the EKF's bell, from the Jacobian G at the mean, is the ellipse (two standard deviations).
Run: python banana.py -> banana.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, PURPLE, RED

here = Path(__file__).parent
th, d = np.radians(30), 1.0
rng = np.random.default_rng(0)
X, Y, T = rng.normal(2, 0.1, 3000), rng.normal(1, 0.1, 3000), rng.normal(th, 0.3, 3000)
X2, Y2 = X + d * np.cos(T), Y + d * np.sin(T)
G = np.array([[1, 0, -d * np.sin(th)], [0, 1, d * np.cos(th)], [0, 0, 1]])
P = G @ np.diag([0.01, 0.01, 0.09]) @ G.T
mx, my = 2 + d * np.cos(th), 1 + d * np.sin(th)
vals, vecs = np.linalg.eigh(P[:2, :2])
a = np.linspace(0, 2 * np.pi, 200)
ell = (vecs @ (2 * np.sqrt(vals)[:, None] * np.vstack([np.cos(a), np.sin(a)]))) + np.array([[mx], [my]])
fig = go.Figure()
fig.add_trace(go.Scatter(x=X2, y=Y2, mode="markers", marker=dict(color=BLUE, size=4, opacity=0.35), name="3000 sampled end poses"))
fig.add_trace(go.Scatter(x=ell[0], y=ell[1], mode="lines", line=dict(color=PURPLE, width=4), name="EKF bell (2 sd ellipse)"))
fig.add_trace(go.Scatter(x=[X2.mean()], y=[Y2.mean()], mode="markers", marker=dict(color=RED, size=14, symbol="x"),
                         name=f"true mean ({X2.mean():.3f}, {Y2.mean():.3f})"))
fig.add_trace(go.Scatter(x=[mx], y=[my], mode="markers", marker=dict(color=PURPLE, size=14, symbol="diamond"),
                         name=f"EKF mean ({mx:.3f}, {my:.3f})"))
fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers+text", marker=dict(color="black", size=12), text=["start (2, 1)"],
                         textposition="bottom left", textfont=dict(size=17), showlegend=False))
fig.update_layout(template="simple_white", font=FONT, width=900, height=820, margin=dict(l=80, r=30, t=40, b=70),
                  legend=dict(x=0.01, y=0.99, font=dict(size=17)),
                  xaxis=dict(title="x (m)", range=[1.4, 3.6], scaleanchor="y"), yaxis=dict(title="y (m)", range=[0.5, 2.5]))
fig.write_image(here / "banana.png")
