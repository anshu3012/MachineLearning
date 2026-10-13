"""A time delay in the heading loop. The same 0.5 rad turn with Kp = Kd = 0.4, but the controller sees the heading and
turn rate late by 0, 0.17, 0.3 or 0.33 s. With no delay or 0.17 s the turn settles at 2.92 s and 2.93 s with no
overshoot; with 0.3 s it overshoots 14.6 percent and rocks until 13.4 s; with 0.33 s the swing grows.
Run: python delay_anim.py -> delay_anim.gif, delay_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from tfkit import turn_with_delay

here = Path(__file__).parent
t = np.linspace(0, 15, 15001)
RUNS = [(d, c, turn_with_delay(t, d)) for d, c in ((0.0, BLUE), (0.17, GREEN), (0.3, ORANGE), (0.33, RED))]


def settle(th):
    out = np.where(np.abs(th - 0.5) > 0.01)[0]
    return t[out[-1] + 1] if out[-1] + 1 < len(t) else np.inf


assert abs(settle(RUNS[0][2]) - 2.92) < 0.01 and abs(settle(RUNS[1][2]) - 2.927) < 0.01 and RUNS[1][2].max() < 0.5 + 1e-4
assert abs(RUNS[2][2].max() - 0.5729) < 1e-4 and abs(settle(RUNS[2][2]) - 13.40) < 0.01
assert np.abs(RUNS[3][2][-2000:] - 0.5).max() > 0.3                   # 0.33 s: still swinging wider at 15 s
TK = np.round(np.arange(0, 15.01, 0.25), 2)


def frame(tk):
    k = int(round(tk * 1000))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 15], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                             showlegend=False))
    for d, c, th in RUNS:
        fig.add_trace(go.Scatter(x=t[:k + 1], y=th[:k + 1], mode="lines", line=dict(color=c, width=4 if d < 0.33 else 3),
                                 name=f"delay {d:g} s"))
    if tk >= 15:
        fig.add_annotation(x=1.2, y=0.08, text="0 and 0.17 s: no overshoot, settled by 2.93 s", showarrow=False,
                           xanchor="left", font=dict(color=GREEN, size=19))
        fig.add_annotation(x=1.2, y=0.15, text="0.3 s: 14.6 % past, oscillates until 13.4 s", showarrow=False,
                           xanchor="left", font=dict(color=ORANGE, size=19))
        fig.add_annotation(x=1.2, y=0.22, text="0.33 s: the swing grows", showarrow=False, xanchor="left",
                           font=dict(color=RED, size=19))
    fig.update_xaxes(title="time t (s)", range=[0, 15])
    fig.update_yaxes(title="heading θ (rad)", range=[0, 1.0])
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12, font=dict(size=20)),
                      margin=dict(l=80, r=30, t=150, b=70),
                      title=dict(x=0.5, y=0.97, text=f"0.5 rad turn, the controller sees the heading late:   t = {tk:.2f} s"))
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "delay_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[16, len(TK) - 1], cols=1,
         width=900)
