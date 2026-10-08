"""The two-variable filter (position and speed) fed the same ten position readings and no commands. Its speed
estimate, never measured, starts at 0 and settles near the robot's true average speed of 0.48 m/s; bands are two
standard deviations. Run: python cv_speed.py -> cv_speed.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE
from kfsim import X_TRUE, Z, kf2d

here = Path(__file__).parent
rows = kf2d()
t = np.arange(0, 11)
pos = np.r_[0, [r["x"][0] for r in rows]]
spd = np.r_[0, [r["x"][1] for r in rows]]
sp = np.sqrt(np.r_[1, [r["P"][0, 0] for r in rows]])
ss = np.sqrt(np.r_[1, [r["P"][1, 1] for r in rows]])
true_speed = (X_TRUE[-1] - X_TRUE[0]) / 10
fig = make_subplots(rows=1, cols=2, subplot_titles=["position: measured", "speed: never measured"], horizontal_spacing=0.1)
for c, m, s, col in ((1, pos, sp, BLUE), (2, spd, ss, GREEN)):
    fig.add_trace(go.Scatter(x=np.r_[t, t[::-1]], y=np.r_[m + 2 * s, (m - 2 * s)[::-1]], fill="toself",
                             fillcolor="rgba(120,120,120,0.15)", line=dict(width=0)), row=1, col=c)
    fig.add_trace(go.Scatter(x=t, y=m, mode="lines+markers", line=dict(color=col, width=4)), row=1, col=c)
fig.add_trace(go.Scatter(x=t, y=X_TRUE, mode="lines", line=dict(color="black", width=2)), row=1, col=1)
fig.add_trace(go.Scatter(x=t[1:], y=Z, mode="markers", marker=dict(color=ORANGE, size=11, symbol="x")), row=1, col=1)
fig.add_hline(y=true_speed, line=dict(color="black", width=2, dash="dash"), row=1, col=2)
fig.add_annotation(x=10, y=true_speed, text=f"true average {true_speed:.2f} m/s", showarrow=False, yshift=14,
                   xanchor="right", font=dict(size=16), row=1, col=2)
fig.update_xaxes(title="step", dtick=2)
fig.update_yaxes(title="position (m)", row=1, col=1)
fig.update_yaxes(title="speed (m/s)", range=[-1.5, 2.2], row=1, col=2)
fig.update_layout(template="simple_white", font=FONT, width=1200, height=520, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=20)
fig.write_image(here / "cv_speed.png")
