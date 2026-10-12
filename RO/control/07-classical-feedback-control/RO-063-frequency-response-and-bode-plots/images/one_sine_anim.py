"""Sine in, sine out on the robot: the heading command is 0.1 sin(t), a weave at 1 rad/s, and the PD heading loop
(Kp = 0.4, Kd = 0.08) starts from rest. Top: the heading over 30 s; the start-up swing dies away by about 10 s and the
heading settles on a sine of the same frequency. Bottom (last frame): one period of the settled part, zoomed: the
heading swings 0.1288 rad against the command's 0.1 (gain 1.288) and its crests come 0.261 s later (phase -14.9
degrees of the 6.28 s period). Run: python one_sine_anim.py -> one_sine_anim.gif, one_sine_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import G_yr, deg, simulate_heading, sine_fit

here = Path(__file__).parent
A, w = 0.1, 1.0
t = np.arange(0, 30.0001, 1e-3)
cmd = A * np.sin(w * t)
th, _, tq = simulate_heading(t, cmd)
k = t >= 15
amp, ph = sine_fit(t[k], th[k], w)
g = G_yr(1j * w)
assert abs(amp / A - 1.288) < 1e-3 and abs(abs(g) - 1.288) < 5e-4 and abs(deg(g) + 14.9) < 0.05
assert abs(-np.radians(deg(g)) / w - 0.261) < 5e-4 and abs(-np.degrees(ph) - 14.9) < 0.1
env = np.abs(th - A * abs(g) * np.sin(w * t + np.angle(g)))     # the start-up part: what is left over
assert env[t >= 10].max() < 0.005 and env[t < 3].max() > 0.04
T = 2 * np.pi / w
t0 = 3 * T                                                         # zoom: the period starting at 18.85 s
zoom = (t >= t0) & (t <= t0 + T)
tc = t0 + np.pi / 2 / w                                            # command crest
th_c = tc - np.angle(g) / w                                        # heading crest, 0.261 s later


def frame(tk, last=False):
    n = int(round(tk / 1e-3))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.5, 0.5], vertical_spacing=0.17,
                        subplot_titles=[f"heading θ (blue) and command θ<sub>r</sub> (dashed): t = {tk:.1f} s",
                                        "one period of the settled part, zoomed" if last else ""])
    fig.add_trace(go.Scatter(x=t, y=cmd, mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=t[:n + 1], y=th[:n + 1], mode="lines", line=dict(color=BLUE, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=[t[n]], y=[th[n]], mode="markers", marker=dict(color=ORANGE, size=12)), 1, 1)
    if tk >= 10:
        fig.add_shape(type="rect", x0=0, x1=10, y0=-0.2, y1=0.2, fillcolor="rgba(228,87,86,0.13)", line_width=0,
                      row=1, col=1)
        fig.add_annotation(x=5, y=0.185, text="start-up swing dies away", showarrow=False, font=dict(color=RED, size=18),
                           row=1, col=1)
    if last:
        tz = t[zoom]
        fig.add_trace(go.Scatter(x=tz, y=cmd[zoom], mode="lines", line=dict(color=GREY, width=3, dash="dash")), 2, 1)
        fig.add_trace(go.Scatter(x=tz, y=th[zoom], mode="lines", line=dict(color=BLUE, width=4)), 2, 1)
        fig.add_trace(go.Scatter(x=[tc, th_c], y=[A, A * abs(g)], mode="markers", marker=dict(color=[GREY, RED], size=13)),
                      2, 1)
        fig.add_annotation(x=th_c, y=A * abs(g), text="heading crest 0.1288 rad", ax=120, ay=-8, arrowcolor=RED,
                           font=dict(color=RED, size=18), row=2, col=1)
        fig.add_annotation(x=tc, y=A, text="command crest 0.1 rad", ax=-120, ay=-30, arrowcolor=GREY,
                           font=dict(color=GREY, size=18), row=2, col=1)
        fig.add_annotation(x=t0 + T / 2, y=-0.16, showarrow=False, font=dict(color=RED, size=19),
                           text="gain 0.1288 / 0.1 = 1.288 · crest 0.2606 s later = −14.9° of the 6.283 s period", row=2, col=1)
        fig.update_xaxes(title="time t (s)", range=[t0, t0 + T], row=2, col=1)
        fig.update_yaxes(title="angle (rad)", range=[-0.19, 0.17], row=2, col=1)
    else:
        fig.add_annotation(x=0.5, y=0.22, xref="paper", yref="paper", showarrow=False, font=dict(size=20, color=GREY),
                           text="the last frame zooms on one settled period")
        fig.update_xaxes(visible=False, row=2, col=1)
        fig.update_yaxes(visible=False, row=2, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, 30], row=1, col=1)
    fig.update_yaxes(title="angle (rad)", range=[-0.2, 0.2], row=1, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1000, showlegend=False,
                      margin=dict(l=90, r=30, t=140, b=70),
                      title=dict(x=0.5, y=0.97, text="weave at 1 rad/s: the heading settles on a sine of the same rate"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


TK = list(np.arange(0, 30.01, 1.0))
figs = [frame(tk) for tk in TK] + [frame(30.0, last=True)]
make_gif(figs, here / "one_sine_anim", fps=6, holds=[4] + [1] * (len(TK) - 1) + [30], keys=[0, 8, len(TK) - 1, len(figs) - 1],
         cols=2, width=900)
