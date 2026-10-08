"""Systematic odometry error: the robot's model uses wheel radius 0.05 m for both wheels, but the right wheel is
really 0.0505 m (1 percent larger). Equal tick counts look like driving straight 10 m to odometry; the true robot turns
left by 0.5 rad and ends 2.49 m from where odometry says. Run: python calib_drift.py -> calib_drift.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
L = 0.2
s = np.linspace(0, 10, 200)                      # distance each wheel thinks it rolled (m)
dR, dL = 1.01 * s, s                             # true wheel distances
th = (dR - dL) / L
d = (dR + dL) / 2
Rt = d[-1] / th[-1]
xt, yt = Rt * np.sin(th), Rt * (1 - np.cos(th))
gap = np.hypot(xt[-1] - 10, yt[-1])
assert abs(th[-1] - 0.5) < 1e-9 and abs(gap - 2.487) < 0.001
fig = go.Figure()
fig.add_trace(go.Scatter(x=s, y=0 * s, mode="lines", line=dict(color=GREY, dash="dash", width=3)))
fig.add_trace(go.Scatter(x=xt, y=yt, mode="lines", line=dict(color=RED, width=3)))
fig.add_annotation(x=10, y=-0.25, text="odometry says: (10, 0)", showarrow=False, xanchor="right",
                   font=dict(size=18, color=GREY))
fig.add_annotation(x=xt[-1], y=yt[-1] + 0.3, text=f"true end ({xt[-1]:.2f}, {yt[-1]:.2f})", showarrow=False,
                   font=dict(size=18, color=RED))
fig.add_annotation(x=10.05, y=1.2, text=f"gap {gap:.2f} m", showarrow=False, xanchor="left", font=dict(size=18))
fig.add_shape(type="line", x0=10, y0=0, x1=xt[-1], y1=yt[-1], line=dict(color="black", width=1.5, dash="dot"))
fig.update_xaxes(range=[-0.3, 11.5], title="x (m)")
fig.update_yaxes(range=[-0.6, 3.2], title="y (m)", scaleanchor="x")
fig.update_layout(template="simple_white", width=1000, height=470, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70),
                  title=dict(text="right wheel 1 percent larger than the model thinks: 10 m 'straight'", x=0.5,
                             font=dict(size=22)))
fig.write_image(here / "calib_drift.png")
