"""The trapezoid rule on the first 0.636 s of the straight drive (10 knot intervals of the least-time solution):
the speed rises in a straight line from 0 to 0.318 m/s at 0.5 m/s^2, and the distance covered is the area under it,
a triangle here (a trapezoid with one side 0): 0.636 / 2 x (0 + 0.318) = 0.101 m, exactly what constant
acceleration gives. Run -> trapezoid.png"""
from pathlib import Path

import plotly.graph_objects as go
import trajkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
r = tk.straight_collocation(N=10)
h = r["T"] / 10
v1, s1 = r["v"][1], r["s"][1]
assert round(h, 4) == 0.6364 and round(v1, 4) == 0.3182 and round(s1, 4) == 0.1013
assert abs(s1 - 0.5 * 0.5 * h * h) < 1e-4
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, h, h, 0], y=[0, v1, 0, 0], fill="toself", fillcolor="rgba(245,133,24,0.25)",
                         line=dict(color=ORANGE, width=1), mode="lines"))
fig.add_trace(go.Scatter(x=[0, h], y=[0, v1], mode="lines+markers", line=dict(color=BLUE, width=4),
                         marker=dict(size=12, color=BLUE)))
fig.add_annotation(x=h * 0.62, y=v1 * 0.25, text=f"area = distance<br>= {h:.4f} / 2 × (0 + {v1:.4f})<br>"
                   f"= {s1:.4f} m", showarrow=False, font=dict(size=20), align="center")
fig.add_annotation(x=0, y=0, text="knot k: v = 0", showarrow=True, ax=40, ay=-60, font=dict(size=18))
fig.add_annotation(x=h, y=v1, text=f"knot k + 1: v = {v1:.4f} m/s", showarrow=True, ax=-90, ay=-40, font=dict(size=18))
fig.add_annotation(x=h / 2, y=-0.035, text=f"h = {h:.4f} s", showarrow=False, font=dict(size=18, color=GREY))
fig.update_xaxes(title="time (s)", range=[-0.05, h + 0.1])
fig.update_yaxes(title="speed v (m/s)", range=[-0.06, 0.4])
fig.update_layout(template="simple_white", font=FONT, width=900, height=560, showlegend=False,
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "trapezoid.png", scale=2)
