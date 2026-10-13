"""How often a sense-plan-act loop must look to stop for the person. The robot drives at 0.595 m/s when the person
steps in 0.465 m ahead of its edge. In the worst case it sees them one whole loop period T later, after driving
0.595 T metres, and then needs 0.354 m to brake at 0.5 m/s^2. The loop stops in time only if the sum is below
0.465 m: T below 0.187 s. Run -> period.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, RED

here = Path(__file__).parent
v, a, gap = 0.595, 0.5, 0.465
stop = round(v ** 2 / (2 * a), 3)
T_max = round((gap - stop) / v, 3)
assert stop == 0.354 and T_max == 0.187
T = np.linspace(0, 1.0, 201)
fig = go.Figure()
fig.add_trace(go.Scatter(x=T, y=v * T + stop, mode="lines", line=dict(color=BLUE, width=4)))
fig.add_hline(y=gap, line=dict(color=RED, width=3, dash="dash"), opacity=1)
fig.add_annotation(x=0.98, y=gap, text="gap to the person, 0.465 m", showarrow=False, xanchor="right", yanchor="bottom",
                   font=dict(size=20, color=RED))
fig.add_annotation(x=0.62, y=v * 0.62 + stop, text="distance to stop:<br>0.595 T + 0.354 m", showarrow=False,
                   xanchor="left", yanchor="top", xshift=12, font=dict(size=20, color=BLUE))
for t in (0.05, 0.1, 0.2, 0.5, 1.0):
    d = v * t + stop
    ok = d < gap
    fig.add_trace(go.Scatter(x=[t], y=[d], mode="markers", marker=dict(size=13, color=GREEN if ok else RED)))
fig.add_vline(x=T_max, line=dict(color=GREY, width=2, dash="dot"), opacity=1)
fig.add_annotation(x=T_max, y=0.30, text="T = 0.187 s", showarrow=False, xanchor="left", xshift=6,
                   font=dict(size=20, color=GREY))
fig.add_annotation(x=0.25, y=0.37, text="green: stops in time", showarrow=False, xanchor="left",
                   font=dict(size=19, color=GREEN))
fig.add_annotation(x=1.0, y=v + stop, text="red: touches the person", showarrow=False, xanchor="right", yshift=22,
                   font=dict(size=19, color=RED))
fig.update_xaxes(title="loop period T (s)", range=[0, 1.05])
fig.update_yaxes(title="distance (m)", range=[0.28, 1.0])
fig.update_layout(template="simple_white", font=FONT, width=900, height=560, showlegend=False,
                  margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "period.png", scale=2)
