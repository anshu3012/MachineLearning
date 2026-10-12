"""Open-loop calibration: the steady speed for each constant force, on the flat hard floor (drag 2 N per m/s), on the
ramp (its pull, 0.785 N, comes off the force) and on carpet (drag 3 N per m/s). The flat-floor test: 0.5 N settles at
0.25 m/s, so 1 N is chosen for 0.5 m/s. The same 1 N gives 0.108 m/s on the ramp and 0.333 m/s on carpet.
Run -> calibration.png (and its interactive twin)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import speedkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED

here = Path(__file__).parent
u = np.linspace(0, 2.0, 201)
flat, ramp, carpet = u / s.B, (u - s.D_RAMP) / s.B, u / s.B_CARPET
assert round(0.5 / s.B, 2) == 0.25 and s.u_open(0.5) == 1.0
assert round(s.steady_open(d=s.D_RAMP), 3) == 0.108 and round(s.steady_open(b=s.B_CARPET), 3) == 0.333

fig = go.Figure()
fig.add_trace(go.Scatter(x=u, y=flat, mode="lines", line=dict(color=BLUE, width=4), name="flat hard floor (the test)"))
fig.add_trace(go.Scatter(x=u, y=ramp, mode="lines", line=dict(color=RED, width=4, dash="dash"),
                         name="on the ramp"))
fig.add_trace(go.Scatter(x=u, y=carpet, mode="lines", line=dict(color=PURPLE, width=4, dash="dot"),
                         name="on carpet"))
fig.add_vline(x=1.0, line=dict(color=GREY, width=2, dash="dash"))
fig.add_hline(y=0.5, line=dict(color=GREY, width=1.5, dash="dot"))
pts = [(0.5, 0.25, BLUE, "test: 0.5 N gives 0.25 m/s", 0.08, 0.62),
       (1.0, 0.5, BLUE, "so 1 N for 0.5 m/s", 0.62, 0.75),
       (1.0, float(s.steady_open(b=s.B_CARPET)), PURPLE, "carpet: 0.333 m/s", 1.4, 0.2),
       (1.0, float(s.steady_open(d=s.D_RAMP)), RED, "ramp: 0.108 m/s", 1.4, 0.05)]
for x, y, c, txt, tx, ty in pts:
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=c, size=15), showlegend=False))
    fig.add_annotation(x=x, y=y, ax=tx, ay=ty, axref="x", ayref="y", text=txt, showarrow=True, arrowhead=2,
                       arrowwidth=1.5, arrowcolor=c, xanchor="left", font=dict(size=19, color=c),
                       bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=1.0, y=1.02, yref="paper", text="the open-loop force, 1 N", showarrow=False,
                   font=dict(size=18, color=GREY))
fig.update_layout(template="simple_white", font=FONT, width=900, height=640, margin=dict(l=90, r=30, t=70, b=80),
                  legend=dict(x=0.01, y=0.99, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="constant force from the motors (N)", range=[0, 2.0], dtick=0.25),
                  yaxis=dict(title="speed it settles at (m/s)", range=[-0.05, 1.0], dtick=0.1))
fig.write_image(here / "calibration.png", scale=2)
