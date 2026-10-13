"""Regulated pure pursuit's curvature rule (Nav2, regulation_functions.hpp curvatureConstraint): when the arc the
car is told to drive is tighter than r_min, the speed is cut in proportion to its radius, v_max x R / r_min, but
not below 0.25 m/s. With v_max = 5 m/s and r_min = 25 m: 2 m/s on our 10 m arc, 1 m/s on the car's tightest 5 m circle.
Run: python rpp_rule.py -> rpp_rule.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREY

here = Path(__file__).parent
V_MAX, R_MIN, V_MIN = 5.0, 25.0, 0.25
R = np.linspace(0.01, 40, 801)
v = np.where(R < R_MIN, np.maximum(V_MAX * R / R_MIN, V_MIN), V_MAX)
assert abs(np.interp(10, R, v) - 2.0) < 1e-6 and abs(np.interp(5, R, v) - 1.0) < 1e-6

fig = go.Figure()
fig.add_trace(go.Scatter(x=R, y=v, mode="lines", line=dict(color=BLUE, width=4), showlegend=False))
fig.add_trace(go.Scatter(x=[5, 10], y=[1, 2], mode="markers+text", marker=dict(color=BLUE, size=14),
                         text=["tightest circle, 5 m: 1 m/s", "our arc, 10 m: 2 m/s"],
                         textposition=["middle right", "middle right"], textfont=dict(size=19, color=BLUE),
                         showlegend=False))
fig.add_vline(x=R_MIN, line=dict(color=GREY, dash="dot", width=2))
fig.add_annotation(x=R_MIN - 0.5, y=5.3, text="25 m: any tighter arc slows the car", showarrow=False,
                   xanchor="right", font=dict(size=18, color=GREY))
fig.update_layout(template="simple_white", font=FONT, width=900, height=600, margin=dict(l=90, r=30, t=60, b=80),
                  title=dict(x=0.5, text="speed limit against the radius of the commanded arc"),
                  xaxis=dict(title="radius of the commanded arc (m)", range=[0, 40], dtick=5),
                  yaxis=dict(title="speed limit (m/s)", range=[0, 5.6], dtick=1))
fig.write_image(here / "rpp_rule.png")
