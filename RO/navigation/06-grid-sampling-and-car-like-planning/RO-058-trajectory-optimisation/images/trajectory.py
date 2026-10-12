"""The least-time drive as a trajectory: where the robot is and when. Left: its path, with a dot every 0.5 s and
the time written at 2, 3, 4 and 5 s; dots far apart mean fast. Right: its forward speed over time, with the 0.6 m/s limit
(dashed). Run -> trajectory.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import trajkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE
from plotly.subplots import make_subplots

here = Path(__file__).parent
sol = tk.solutions()["time"]
T = sol["T"]
ts, xs = tk.drive_controls(sol["X"], sol["U"], T)
assert round(T, 2) == 6.18
fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.08,
                    subplot_titles=["path, a dot every 0.5 s", "forward speed v (m/s)"])
rd.room(fig, rc=(1, 1))
fig.add_trace(go.Scatter(x=xs[:, 0], y=xs[:, 1], mode="lines", line=dict(color=BLUE, width=3)), row=1, col=1)
for t in np.arange(0, T, 0.5):
    p = xs[np.searchsorted(ts, t)]
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(size=9, color=ORANGE)), row=1, col=1)
    if abs(t - round(t)) < 1e-9 and 1 < t < 6:
        fig.add_annotation(x=p[0] - 0.12, y=p[1], text=f"{t:.0f} s", showarrow=False, xanchor="right",
                           font=dict(size=17, color="#444444"), row=1, col=1)
for x, y, th, lab in ((*tk.START[:3], "start, 0 s"), (*tk.GOAL[:3], f"door pose, {T:.2f} s")):
    rd.robot(fig, x, y, th, GREY, rc=(1, 1), width=2)
fig.add_annotation(x=2.0, y=0.62, text="start, 0 s", showarrow=False, font=dict(size=17), row=1, col=1)
fig.add_annotation(x=3.92, y=3.5, text=f"{T:.2f} s", showarrow=False, xanchor="left", font=dict(size=17), row=1, col=1)
rd.axes(fig, rc=(1, 1))
fig.add_trace(go.Scatter(x=ts, y=xs[:, 3], mode="lines", line=dict(color=BLUE, width=4)), row=1, col=2)
fig.add_trace(go.Scatter(x=[0, T], y=[0.6, 0.6], mode="lines", line=dict(color=GREY, dash="dash", width=2)),
              row=1, col=2)
fig.add_annotation(x=T / 2, y=0.64, text="limit 0.6 m/s", showarrow=False, font=dict(size=17, color=GREY),
                   row=1, col=2)
fig.update_xaxes(title="time (s)", range=[0, 6.5], row=1, col=2)
fig.update_yaxes(range=[0, 0.7], row=1, col=2)
fig.update_layout(template="simple_white", font=FONT, width=1300, height=760, showlegend=False,
                  margin=dict(l=10, r=20, t=50, b=60))
fig.write_image(here / "trajectory.png", scale=2)
