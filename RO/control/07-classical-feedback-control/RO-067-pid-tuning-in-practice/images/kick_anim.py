"""Derivative kick on RO-060's heading PID (kp = 0.2, ki = 0.05, kd = 0.283). At t = 0.5 s the heading command steps
from 0 to 0.1 rad. Red: derivative on the error; in the step's sample the error jumps by 0.1 rad in 0.01 s and the D term
asks for 2.83 N m, so the torque request is 2.85 N m, 14 times the 0.2 N m limit. Blue: derivative on the measured
heading; the request starts at 0.02 N m. Bottom: the two headings are almost the same (21.1 and 22.5 percent overshoot).
Run: python kick_anim.py -> kick_anim.gif, kick_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from tunekit import TAU_MAX, heading_run, overshoot

here = Path(__file__).parent
T = 10.0
on_err = heading_run(T, beta=1.0, gamma=1.0)
on_meas = heading_run(T, beta=1.0, gamma=0.0)
k0 = 50
assert abs(on_err["c"][k0] - 2.85) < 1e-9 and abs(on_err["c"][k0] / TAU_MAX - 14.25) < 1e-6
assert abs(on_meas["c"][k0] - 0.02) < 1e-9 and on_meas["c"].max() <= 0.02 + 1e-9
assert abs(overshoot(on_err) - 21.1) < 0.05 and abs(overshoot(on_meas) - 22.5) < 0.05
RUNS = (("derivative on the error", on_err, RED), ("derivative on the measurement", on_meas, BLUE))


def frame(upto, final=False):
    n = int(round(upto / 0.01)) + 1
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.5, 0.5])
    for name, o, col in RUNS:
        fig.add_trace(go.Scatter(x=o["t"][:n], y=o["c"][:n], mode="lines", line=dict(color=col, width=3.5),
                                 name=name, cliponaxis=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=o["t"][:n], y=o["th"][:n], mode="lines", line=dict(color=col, width=3.5),
                                 showlegend=False), row=2, col=1)
    for lim in (TAU_MAX, -TAU_MAX):
        fig.add_hline(y=lim, line=dict(color=GREY, width=2, dash="dot"), row=1, col=1)
    fig.add_annotation(x=9.9, y=TAU_MAX, text="torque limit 0.2 N m", showarrow=False, xanchor="right",
                       yanchor="bottom", font=dict(size=17, color=GREY), row=1, col=1)
    fig.add_hline(y=0.1, line=dict(color="black", width=1, dash="dash"), row=2, col=1)
    if upto >= 0.5:
        fig.add_annotation(x=0.5, y=0.33, text="request 2.85 N m, above the axis range", ax=150, ay=10,
                           font=dict(size=19, color=RED), arrowcolor=RED, arrowwidth=2, xanchor="left",
                           row=1, col=1)
    title = (f"t = {upto:.1f} s: the heading command steps to 0.1 rad at t = 0.5 s" if not final else
             "same turn, no 2.85 N m spike: derivative on the measurement")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=800,
                      margin=dict(l=110, r=30, t=170, b=80), title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.03, yanchor="bottom",
                                  font=dict(size=18)))
    fig.update_yaxes(title_text="torque request (N m)", range=[-0.06, 0.35], row=1, col=1)
    fig.update_yaxes(title_text="heading (rad)", range=[-0.005, 0.135], row=2, col=1)
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, T], row=2, col=1)
    return fig


times = [0.3, 0.5, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
figs = [frame(x) for x in times] + [frame(T, final=True)]
make_gif(figs, here / "kick_anim", fps=3, holds=[3, 4] + [1] * (len(times) - 2) + [12],
         keys=[1, len(figs) - 1], cols=1, width=850)
