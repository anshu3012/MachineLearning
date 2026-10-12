"""Pole-zero cancellation hides a slow pole. RO-060's speed loop under PI control, P gain 20 N per m/s, with two
integral gains: 5 N per m puts the controller's zero on the robot's pole at -0.25 and cancels it (blue); RO-060's own
10 N per m does not (orange). The robot cruises at 0.4 m/s; at t = 0 the command steps to 0.5 m/s; from t = 10 s the
1 % ramp of RO-059 pulls back with 0.785 N.
To the command, the cancelling loop is a clean first-order reply: no overshoot, within 0.01 m/s from 0.92 s; RO-060's
gains overshoot by 0.005 m/s and are within 0.01 m/s from 0.76 s. To the ramp, the cancelled pole returns: the blue
speed dips to 0.470 m/s and is back within 0.01 m/s only 5.89 s later, the orange one after 3.14 s.
Run: python cancel_anim.py -> cancel_anim.gif, cancel_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from tfkit import speed_pi

here = Path(__file__).parent
t = np.linspace(0, 25, 25001)
vc, vn = speed_pi(t, 5.0), speed_pi(t, 10.0)


def back_after(v):
    post = np.where((t >= 10) & (np.abs(v - 0.5) > 0.01))[0]
    return t[post[-1] + 1] - 10


def settle(v):
    pre = np.where((t < 10) & (np.abs(v - 0.5) > 0.01))[0]
    return t[pre[-1] + 1]


assert abs(settle(vc) - 0.922) < 0.002 and abs(settle(vn) - 0.759) < 0.002 and vc[t < 10].max() <= 0.5 + 1e-6
assert abs(vn[t < 10].max() - 0.5049) < 1e-4 and abs(vc[t >= 10].min() - 0.4696) < 1e-4
assert abs(back_after(vc) - 5.89) < 0.01 and abs(back_after(vn) - 3.14) < 0.01
TK = np.round(np.arange(0, 25.01, 0.25), 2)


def frame(tk):
    k = int(round(tk * 1000))
    fig = go.Figure()
    fig.add_shape(type="rect", x0=10, x1=25, y0=0.38, y1=0.53, fillcolor="rgba(107,107,107,0.10)", line=dict(width=0))
    fig.add_annotation(x=10.2, y=0.527, text="the 1 % ramp pulls back 0.785 N from 10 s", showarrow=False,
                       xanchor="left", yanchor="top", font=dict(color=GREY, size=19))
    fig.add_trace(go.Scatter(x=[0, 25], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                             showlegend=False))
    fig.add_trace(go.Scatter(x=t[:k + 1], y=vc[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="integral gain 5: its zero cancels the pole at −0.25"))
    fig.add_trace(go.Scatter(x=t[:k + 1], y=vn[:k + 1], mode="lines", line=dict(color=ORANGE, width=4),
                             name="integral gain 10 (RO-060): poles −0.57, −2.18"))
    if tk >= 10:
        fig.add_annotation(x=1.5, y=0.43, text="to the command: blue within 0.01 m/s from 0.92 s,<br>"
                           "no overshoot; orange from 0.76 s", showarrow=False, xanchor="left", font=dict(size=19))
    if tk >= 25:
        fig.add_annotation(x=11.0, y=vc[t >= 10].min(), text="back within 0.01 m/s: blue after 5.89 s,<br>"
                           "orange after 3.14 s", ax=130, ay=55, xanchor="left", arrowcolor=RED,
                           font=dict(size=19, color=RED))
    fig.update_xaxes(title="time t (s)", range=[0, 25])
    fig.update_yaxes(title="speed v (m/s)", range=[0.38, 0.53])
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620,
                      legend=dict(x=0.5, xanchor="center", y=1.16, orientation="v", font=dict(size=19)),
                      margin=dict(l=90, r=30, t=170, b=70),
                      title=dict(x=0.5, y=0.97, text=f"speed loop, PI with two integral gains:   t = {tk:.2f} s"))
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "cancel_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[40, len(TK) - 1], cols=1,
         width=900)
