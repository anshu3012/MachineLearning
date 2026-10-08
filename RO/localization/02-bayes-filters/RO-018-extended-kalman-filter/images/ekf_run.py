"""The EKF on the corridor for 16 steps, passing the beacon at 6 m. Top: truth, estimate and a band of two standard
deviations. Bottom: the slope H of the distance at the prediction; near the beacon it is close to 0, so a reading
says little about position and the band widens. Run: python ekf_run.py -> ekf_run.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, RED
from ekfsim import B, X_TRUE, ekf

here = Path(__file__).parent
rows = ekf()
t = np.arange(1, 17)
x = np.array([r["x"] for r in rows])
sd = np.sqrt([r["p"] for r in rows])
H = [r["H"] for r in rows]
fig = make_subplots(rows=2, cols=1, row_heights=[0.62, 0.38], shared_xaxes=True, vertical_spacing=0.06)
fig.add_trace(go.Scatter(x=np.r_[t, t[::-1]], y=np.r_[x + 2 * sd, (x - 2 * sd)[::-1]], fill="toself",
                         fillcolor="rgba(76,120,168,0.25)", line=dict(width=0), name="estimate ± 2 sd"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=X_TRUE, mode="lines+markers", line=dict(color="black", width=3), name="true"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=x, mode="lines+markers", line=dict(color=BLUE, width=3), name="EKF estimate"), row=1, col=1)
fig.add_annotation(x=12, y=B, text="passing the beacon (6 m)", showarrow=True, ax=90, ay=60, font=dict(color=RED, size=16), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=H, mode="lines+markers", line=dict(color=RED, width=3), showlegend=False), row=2, col=1)
fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
fig.update_yaxes(title="position (m)", row=1, col=1)
fig.update_yaxes(title="slope H", range=[-1.05, 1.05], row=2, col=1)
fig.update_xaxes(title="step", dtick=1, row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=760, margin=dict(l=90, r=30, t=30, b=70),
                  legend=dict(x=0.01, y=0.99, font=dict(size=17)))
fig.write_image(here / "ekf_run.png")
