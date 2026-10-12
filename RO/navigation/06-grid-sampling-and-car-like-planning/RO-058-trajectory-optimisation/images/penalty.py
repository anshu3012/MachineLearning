"""A hard limit against a soft one, on one straight piece of the band 0.18 m long (both wheels at the speed v).
The time cost of the piece is dT^2 with dT = 0.18 / v; TEB's penalty for the wheel limit is 2 (v - 0.55)^2 above
0.55 m/s (weight 2, starting 0.05 m/s inside the 0.6 m/s limit), 0 below. Their sum is lowest at 0.62 m/s, above the
limit: a soft limit is a price, not a wall. With weight 1000 the lowest point moves to 0.550 m/s. Left of the hard
limit (dashed) every speed is allowed, right of it none is. Run -> penalty.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE
from scipy.optimize import minimize_scalar

here = Path(__file__).parent
D, LIM, EPS = 0.18, 0.6, 0.05


def time_cost(v):
    return (D / v) ** 2


def pen(v, w):
    return w * np.maximum(0, v - (LIM - EPS)) ** 2


best = {w: minimize_scalar(lambda v: time_cost(v) + pen(v, w), bounds=(0.3, 1.0), method="bounded",
                           options=dict(xatol=1e-9)).x for w in (2, 1000)}
assert round(best[2], 2) == 0.62 and round(best[1000], 3) == 0.550
v = np.linspace(0.45, 0.72, 400)
fig = go.Figure()
fig.add_vrect(x0=LIM, x1=0.72, fillcolor="#EEEEEE", line_width=0, layer="below")
fig.add_trace(go.Scatter(x=v, y=time_cost(v), mode="lines", line=dict(color=BLUE, width=4), name="time cost ΔT²"))
fig.add_trace(go.Scatter(x=v, y=pen(v, 2), mode="lines", line=dict(color=ORANGE, width=4),
                         name="penalty, weight 2"))
fig.add_trace(go.Scatter(x=v, y=time_cost(v) + pen(v, 2), mode="lines", line=dict(color=PURPLE, width=5),
                         name="sum"))
fig.add_trace(go.Scatter(x=[best[2]], y=[time_cost(best[2]) + pen(best[2], 2)], mode="markers",
                         marker=dict(size=14, color=PURPLE), showlegend=False))
fig.add_annotation(x=best[2], y=time_cost(best[2]) + pen(best[2], 2), text=f"lowest sum: {best[2]:.2f} m/s",
                   showarrow=True, ax=40, ay=-60, font=dict(size=19, color=PURPLE))
fig.add_vline(x=LIM, line=dict(color=GREY, dash="dash", width=3))
fig.add_annotation(x=LIM + 0.003, y=0.155, text="hard limit 0.6 m/s:<br>nothing to the right<br>is allowed",
                   showarrow=False, xanchor="left", align="left", font=dict(size=18, color=GREY))
fig.add_annotation(x=LIM - EPS, y=0.0, text="penalty starts<br>at 0.55 m/s", showarrow=True, ax=-60, ay=-70,
                   font=dict(size=18, color=ORANGE))
fig.update_xaxes(title="speed of both wheels v (m/s)", range=[0.45, 0.72])
fig.update_yaxes(title="cost of one 0.18 m piece", range=[0, 0.17])
fig.update_layout(template="simple_white", font=FONT, width=1100, height=700,
                  legend=dict(x=0.02, y=0.55, font_size=19, bgcolor="rgba(255,255,255,0.9)"),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "penalty.png", scale=2)
print({w: round(b, 4) for w, b in best.items()})
