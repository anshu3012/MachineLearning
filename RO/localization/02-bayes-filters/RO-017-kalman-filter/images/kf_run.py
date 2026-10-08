"""The ten steps of the corridor run. Top: true position, readings and the Kalman estimate with its band of two
standard deviations (2 times the square root of P). Bottom: the gain K, which falls from 0.863 and settles near 0.22.
Run: python kf_run.py -> kf_run.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE, RED
from kfsim import X_TRUE, Z, kf1d

here = Path(__file__).parent
rows = kf1d()
t = np.arange(1, 11)
x = np.array([r["x"] for r in rows])
sd = np.sqrt([r["p"] for r in rows])
K = [r["K"] for r in rows]
fig = make_subplots(rows=2, cols=1, row_heights=[0.65, 0.35], shared_xaxes=True, vertical_spacing=0.06)
fig.add_trace(go.Scatter(x=np.r_[t, t[::-1]], y=np.r_[x + 2 * sd, (x - 2 * sd)[::-1]], fill="toself",
                         fillcolor="rgba(76,120,168,0.18)", line=dict(width=0), name="estimate ± 2 sd"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=X_TRUE[1:], mode="lines+markers", line=dict(color="black", width=3), name="true"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=Z, mode="markers", marker=dict(color=ORANGE, size=13, symbol="x"), name="readings"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=x, mode="lines+markers", line=dict(color=BLUE, width=4), name="estimate"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=K, mode="lines+markers+text", line=dict(color=RED, width=4), text=[f"{k:.2f}" for k in K],
                         textposition="top right", textfont=dict(size=15), showlegend=False), row=2, col=1)
fig.update_yaxes(title="position (m)", row=1, col=1)
fig.update_yaxes(title="gain K", range=[0, 1.05], row=2, col=1)
fig.update_xaxes(title="step", dtick=1, row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=760, margin=dict(l=90, r=30, t=30, b=70),
                  legend=dict(x=0.01, y=0.99, font=dict(size=17)))
fig.write_image(here / "kf_run.png")
