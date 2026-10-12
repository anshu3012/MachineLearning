"""The heading loop as a mass on a spring and a damper. Under PD control (Kp = 0.4 N m/rad, Kd = 0.08 N m s/rad,
inertia I = 0.1 kg m^2) the heading error e = 0.5 rad - heading obeys I e'' + Kd e' + Kp e = 0, the equation of a
block of mass I on a spring of stiffness Kp and a damper Kd. Left: the block, its position is the error; the dashed
line is zero error. Right: the error over time, starting at 0.5 rad, swinging to -0.263 rad at 1.60 s.
Run: python spring_anim.py -> spring_anim.gif, spring_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from stepkit import I, KD_OLD, KP_TH, TH_REF, heading_pd

here = Path(__file__).parent
t = np.linspace(0, 12, 12001)
th, _, _ = heading_pd(t, kd=KD_OLD)
e = TH_REF - th
ep = np.gradient(e, t)
assert abs(e.min() + 0.263) < 5e-4 and abs(t[e.argmin()] - 1.603) < 2e-3
assert np.max(np.abs(I * np.gradient(ep, t)[5:-5] + KD_OLD * ep[5:-5] + KP_TH * e[5:-5])) < 1e-4   # the ODE holds
WALL, HALF = -1.05, 0.11                                  # wall position and half-width of the block (drawing units)
TK = np.round(np.arange(0, 12.01, 0.25), 2)


def spring(x0, x1, y, n=9, amp=0.06):
    xs = np.linspace(x0, x1, 2 * n + 3)
    ys = np.r_[y, y + amp * np.array([(-1) ** i for i in range(2 * n + 1)]), y]
    return xs, ys


def frame(tk, last=False):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.08,
                        subplot_titles=["block on a spring and a damper", f"heading error e<sub>θ</sub> = {e[k]:.3f} rad"])
    x = e[k]
    left = x - HALF
    fig.add_trace(go.Scatter(x=[WALL, WALL], y=[-0.42, 0.42], mode="lines", line=dict(color="black", width=8)), 1, 1)
    sx, sy = spring(WALL, left, 0.17)
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    cyl0, cyl1 = WALL + 0.12, WALL + 0.62                 # damper: a fixed cylinder and a rod moving with the block
    fig.add_trace(go.Scatter(x=[WALL, cyl0], y=[-0.17, -0.17], mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[cyl1, cyl0, cyl0, cyl1], y=[-0.08, -0.08, -0.26, -0.26], mode="lines",
                             line=dict(color=BLUE, width=4)), 1, 1)
    piston = min(max(left - 0.35, cyl0 + 0.05), cyl1 - 0.02)
    fig.add_trace(go.Scatter(x=[piston, piston], y=[-0.24, -0.10], mode="lines", line=dict(color=BLUE, width=6)), 1, 1)
    fig.add_trace(go.Scatter(x=[piston, left], y=[-0.17, -0.17], mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[left, x + HALF, x + HALF, left, left], y=[-0.3, -0.3, 0.3, 0.3, -0.3], fill="toself",
                             mode="lines", line=dict(color="black", width=2), fillcolor="rgba(107,107,107,0.35)"), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-0.45, 0.45], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, 1)
    fig.add_annotation(x=0, y=0.47, text="e<sub>θ</sub> = 0", showarrow=False, yanchor="bottom", font=dict(color=GREY, size=18),
                       row=1, col=1)
    fig.add_annotation(x=WALL + 0.02, y=0.31, text="spring Kp = 0.4", showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(color=ORANGE, size=18), row=1, col=1)
    fig.add_annotation(x=WALL + 0.02, y=-0.33, text="damper Kd = 0.08", showarrow=False, xanchor="left", yanchor="top",
                       font=dict(color=BLUE, size=18), row=1, col=1)
    fig.add_annotation(x=x, y=0, text="I", showarrow=False, font=dict(size=20), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 12], y=[0, 0], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=e[:k + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[t[k]], y=[e[k]], mode="markers", marker=dict(color=ORANGE, size=14)), 1, 2)
    if tk >= 1.6:
        fig.add_annotation(x=1.603, y=e.min(), text="swings past zero to −0.263 rad", ax=150, ay=0, xanchor="left",
                           arrowcolor=RED, font=dict(color=RED, size=18), row=1, col=2)
    fig.update_xaxes(range=[-1.15, 0.75], title="block position = error e<sub>θ</sub> (rad)", row=1, col=1)
    fig.update_yaxes(range=[-0.6, 0.6], visible=False, row=1, col=1)
    fig.update_xaxes(range=[0, 12], title="time t (s)", row=1, col=2)
    fig.update_yaxes(range=[-0.35, 0.55], title="heading error e<sub>θ</sub> (rad)", row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1200, height=580, showlegend=False,
                      margin=dict(l=40, r=30, t=130, b=80),
                      title=dict(x=0.5, y=0.95, text=f"I e<sub>θ</sub>″ + Kd e<sub>θ</sub>′ + Kp e<sub>θ</sub> = 0, released from 0.5 rad:   t = {tk:.2f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "spring_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30],
         keys=[0, 4, 7, len(figs) - 1], cols=2, width=900)
