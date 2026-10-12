"""Bounded input, bounded output? Three systems driven by small, bounded inputs, drawn over 20 s.
Left: the speed plant 1 / (8 s + 2) (pole -0.25) under a constant 1 N: the speed levels off at 0.5 m/s.
Middle: the heading plant 10 / s^2 (two poles at 0) under a constant 0.02 N m: the heading grows as 0.1 t^2, 40 rad.
Right: a torque wobble 0.02 sin(2 t) N m on two heading loops: P only (poles +-2j) swings wider by 0.05 rad every
second, 0.94 rad by 20 s; PD (poles -2, -2) stays within 0.03 rad.
Run: python bibo_anim.py -> bibo_anim.gif, bibo_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import scipy.signal as sig
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
t = np.linspace(0, 20, 20001)
v = 0.5 * (1 - np.exp(-0.25 * t))                          # 1 N into 1 / (8 s + 2)
th = 0.1 * t ** 2                                           # 0.02 N m into 10 / s^2
w = 0.02 * np.sin(2 * t)
_, thP, _ = sig.lsim(sig.lti([10], [1, 0, 4]), U=w, T=t)     # P only: 10 / (s^2 + 4)
_, thPD, _ = sig.lsim(sig.lti([10], [1, 4, 4]), U=w, T=t)    # PD: 10 / (s^2 + 4 s + 4)
assert abs(v[-1] - 0.5) < 5e-3 and abs(th[-1] - 40) < 1e-9
assert abs(np.abs(thP).max() - 0.942) < 1e-3 and np.abs(thPD).max() < 0.03   # P only: 0.025 sin 2t - 0.05 t cos 2t
TK = np.round(np.arange(0, 20.01, 0.5), 1)


def frame(tk):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.09,
                        subplot_titles=["speed plant, 1 N", "heading plant, 0.02 N·m", "heading loops, wobble"])
    fig.add_trace(go.Scatter(x=t[:k + 1], y=v[:k + 1], mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=th[:k + 1], mode="lines", line=dict(color=ORANGE, width=4), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=thP[:k + 1], mode="lines", line=dict(color=RED, width=3),
                             name="P only: poles ±2j"), 1, 3)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=thPD[:k + 1], mode="lines", line=dict(color=GREEN, width=4),
                             name="PD: poles −2, −2"), 1, 3)
    if tk >= 20:
        fig.add_annotation(x=19.5, y=0.12, text="bounded:<br>levels at 0.5 m/s", showarrow=False, xanchor="right",
                           font=dict(color=BLUE, size=18), row=1, col=1)
        fig.add_annotation(x=1, y=36, text="unbounded:<br>0.1 t², 40 rad", showarrow=False, xanchor="left",
                           yanchor="top", font=dict(color=ORANGE, size=18), row=1, col=2)
    fig.update_yaxes(title="speed v (m/s)", range=[0, 0.6], row=1, col=1)
    fig.update_yaxes(title="heading θ (rad)", range=[0, 42], row=1, col=2)
    fig.update_yaxes(title="heading θ (rad)", range=[-1.1, 1.1], row=1, col=3)
    fig.update_xaxes(title="time t (s)", range=[0, 20])
    fig.update_layout(template="simple_white", font=FONT, width=1350, height=600,
                      legend=dict(orientation="h", x=0.83, xanchor="center", y=1.2, font=dict(size=19)),
                      margin=dict(l=70, r=30, t=160, b=70),
                      title=dict(x=0.32, y=0.96, text=f"small bounded inputs:   t = {tk:.1f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "bibo_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[10, len(TK) - 1], cols=1,
         width=950)
