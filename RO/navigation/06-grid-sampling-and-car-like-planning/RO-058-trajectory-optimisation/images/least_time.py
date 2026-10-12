"""The least-time drive to the door pose found by collocation, 6.18 s, over time: its controls replayed in small
simulation steps (lines) and the 31 knot points (dots). Top: the forward speed v and the faster wheel's speed, both
under the 0.6 m/s limit (dashed). Middle: the acceleration a, at +0.5 m/s^2 to speed up and -0.5 m/s^2 to brake.
Bottom: the turn rate omega: a fast turn on the spot at the start and at the end, where the speed is near 0 and the
wheel limit allows up to 6 rad/s. Run -> least_time.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import trajkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE
from plotly.subplots import make_subplots

here = Path(__file__).parent
sol = tk.solutions()["time"]
T, X, U = sol["T"], sol["X"], sol["U"]
tk_ = np.linspace(0, T, len(X))
ts, xs = tk.drive_controls(X, U, T)
us = np.array([np.interp(ts, tk_, U[:, j]) for j in range(2)]).T
w1, w2 = tk.wheels(xs[:, 3], us[:, 1])
assert round(T, 2) == 6.18 and max(w1.max(), w2.max()) < 0.6025 and abs(U[:, 0]).max() <= 0.5 + 1e-9
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
                    subplot_titles=["speed (m/s): forward speed v, faster wheel", "acceleration a (m/s²)",
                                    "turn rate ω (rad/s)"])
fig.add_trace(go.Scatter(x=ts, y=np.maximum(w1, w2), mode="lines", line=dict(color=PURPLE, width=3),
                         name="faster wheel"), row=1, col=1)
fig.add_trace(go.Scatter(x=ts, y=xs[:, 3], mode="lines", line=dict(color=BLUE, width=4), name="forward speed v"),
              row=1, col=1)
fig.add_trace(go.Scatter(x=tk_, y=X[:, 3], mode="markers", marker=dict(size=7, color=BLUE), showlegend=False),
              row=1, col=1)
fig.add_trace(go.Scatter(x=tk_, y=U[:, 0], mode="lines+markers", line=dict(color=ORANGE, width=3),
                         marker=dict(size=7), showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=tk_, y=U[:, 1], mode="lines+markers", line=dict(color=GREY, width=3),
                         marker=dict(size=7), showlegend=False), row=3, col=1)
for r, ys in ((1, (0.6,)), (2, (0.5, -0.5))):
    for y in ys:
        fig.add_trace(go.Scatter(x=[0, T], y=[y, y], mode="lines", line=dict(color="#999999", dash="dash", width=2),
                                 showlegend=False), row=r, col=1)
fig.update_yaxes(range=[-0.15, 0.75], row=1, col=1)
fig.update_yaxes(range=[-0.6, 0.6], row=2, col=1)
fig.update_xaxes(title="time (s)", row=3, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000,
                  legend=dict(x=0.38, y=0.88, yanchor="top", font_size=18, bgcolor="rgba(255,255,255,0.9)"),
                  margin=dict(l=70, r=20, t=40, b=60))
fig.write_image(here / "least_time.png", scale=2)
