"""Two noisy sources and their blend: the true path of the robot over ten steps, the beacon readings (jumpy, sd
0.4 m), dead reckoning from the commands alone (smooth but off and drifting), and the Kalman filter estimate.
Run: python problem.py -> problem.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from kfsim import U, X0, X_TRUE, Z, kf1d

here = Path(__file__).parent
t = np.arange(11)
odo = X0 + U * t
est = [X0] + [r["x"] for r in kf1d()]
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=X_TRUE, mode="lines+markers", line=dict(color="black", width=3), name="true position"))
fig.add_trace(go.Scatter(x=t[1:], y=Z, mode="markers", marker=dict(color=ORANGE, size=13, symbol="x"),
                         name="beacon readings"))
fig.add_trace(go.Scatter(x=t, y=odo, mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                         name="commands only (dead reckoning)"))
fig.add_trace(go.Scatter(x=t, y=est, mode="lines+markers", line=dict(color=BLUE, width=4), name="Kalman filter"))
fig.update_layout(template="simple_white", font=FONT, width=1000, height=560, margin=dict(l=90, r=30, t=40, b=70),
                  legend=dict(x=0.01, y=0.99, font=dict(size=18)),
                  xaxis=dict(title="time step (1 s each)", dtick=1), yaxis=dict(title="position along the corridor (m)"))
fig.write_image(here / "problem.png")
