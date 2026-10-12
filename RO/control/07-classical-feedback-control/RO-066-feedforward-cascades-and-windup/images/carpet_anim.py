"""Driving straight (heading 0), one wheel rolls onto carpet at t = 1 s: the extra drag on that wheel turns the robot
with a torque of -0.05 N m. One frame per 0.15 s for 14 s. Purple: RO-060's heading PID (0.2, 0.283, 0.05) swings
11.1 degrees off at t = 3.65 s and is back within 0.5 degrees only at 11.56 s. Blue: the cascade; the gyro loop's
integral cancels the torque, the yaw rate is back within 0.01 rad/s at 1.21 s and the heading dips 0.21 degrees.
Top: yaw rate from the gyro. Bottom: heading. Run: python carpet_anim.py -> carpet_anim.gif, carpet_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, make_gif
from robotctl import heading_loop, heading_pid

here = Path(__file__).parent
T = 14
dist = lambda t: -0.05 if t >= 1 else 0.0
cas = heading_loop(T, lambda t: 0.0, tau_d=dist)
pid = heading_pid(T, lambda t: 0.0, tau_d=dist)
t = cas["t"]
k_back = np.where(np.abs(cas["w"]) > 0.01)[0][-1] + 1
assert abs(np.degrees(cas["th"].min()) + 0.212) < 5e-4 and abs(t[k_back] - 1.21) < 1e-9
j = pid["th"].argmin()
assert abs(np.degrees(pid["th"][j]) + 11.12) < 5e-3 and abs(t[j] - 3.65) < 1e-9
k_pid = np.where(np.abs(np.degrees(pid["th"])) > 0.5)[0][-1] + 1
assert abs(t[k_pid] - 11.56) < 1e-9


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.45, 0.55], vertical_spacing=0.12)
    for row in (1, 2):
        fig.add_vrect(x0=1, x1=T, fillcolor=GREY, opacity=0.12, layer="below", line_width=0,
                      exclude_empty_subplots=False, row=row, col=1)
    for s, col, name in ((pid, PURPLE, "RO-060's heading PID"), (cas, BLUE, "cascade")):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["w"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=1, col=1)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=np.degrees(s["th"][:k + 1]), mode="lines", line=dict(color=col, width=4),
                                 showlegend=False), row=2, col=1)
    fig.add_annotation(x=1.2, y=0.04, xref="x", yref="y", text="one wheel on carpet", showarrow=False, xanchor="left",
                       font=dict(size=18, color=GREY))
    if k >= j:
        fig.add_annotation(x=t[j], y=np.degrees(pid["th"][j]), xref="x2", yref="y2", ax=60, ay=20, xanchor="left",
                           text="11.1° off", font=dict(size=19, color=PURPLE), arrowcolor=PURPLE)
    if k >= len(t) - 15:
        fig.add_annotation(x=1.37, y=-0.21, xref="x2", yref="y2", ax=40, ay=-40, xanchor="left",
                           text="cascade: dips 0.21°", font=dict(size=19, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=0.02, y=1.05, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-0.15, 0.06], title="yaw rate (rad/s)", row=1, col=1)
    fig.update_yaxes(range=[-12.5, 2], title="heading (°)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=780, margin=dict(l=110, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=0.77, yanchor="top", font=dict(size=18)))
    return fig


ks = list(range(0, len(t), 15))
figs = [frame(k) for k in ks]
make_gif(figs, here / "carpet_anim", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(360), len(ks) - 1], cols=1, width=850)
