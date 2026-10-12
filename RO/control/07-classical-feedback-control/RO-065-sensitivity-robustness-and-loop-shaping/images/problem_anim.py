"""The opening problem: one wheel starts to drag at t = 1 s, a steady torque of 0.02 N m on the heading. Top: the PD
heading loop as modelled (inertia 0.1 kg m^2, no delay) rings, peaks at 0.076 rad and settles 0.05 rad (2.9 degrees)
off. Bottom: the real robot, carrying a payload (inertia 0.15 kg m^2) and with a 0.25 s motor-driver delay: the same
drag sets off a swing that keeps growing (0.26 rad by 20 s). Run: python problem_anim.py -> problem_anim.gif,
problem_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from shapekit import DRAG, I_PAY, TAU_REAL, sim

here = Path(__file__).parent
t = np.arange(0, 20.001, 1e-3)
th_m, _ = sim("pd", t, dist=DRAG)
th_r, _ = sim("pd", t, dist=DRAG, inertia=I_PAY, tau=TAU_REAL)
assert abs(th_m.max() - 0.0763) < 5e-4 and abs(th_m[-1] - 0.05) < 1e-4
assert abs(th_r.max() - 0.256) < 1e-3 and np.ptp(th_r[t > 15]) > np.ptp(th_r[(t > 5) & (t < 10)])


def frame(tn, last=False):
    k = t <= tn
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.17, subplot_titles=(
        "as modelled: inertia 0.1 kg·m², no delay",
        "the real robot: payload (inertia 0.15 kg·m²), 0.25 s delay"))
    for a in fig.layout.annotations:
        a.font = dict(size=20)
    for row, th in ((1, th_m), (2, th_r)):
        fig.add_trace(go.Scatter(x=[1, 1], y=[-0.3, 0.3], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                                 showlegend=False), row, 1)
        fig.add_trace(go.Scatter(x=[0, 20], y=[0.05, 0.05], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                                 showlegend=False), row, 1)
        fig.add_trace(go.Scatter(x=t[k][::20], y=th[k][::20], mode="lines", line=dict(color=BLUE, width=4),
                                 showlegend=False), row, 1)
        fig.add_annotation(x=1, y=0.27 if row == 2 else 0.115, text="drag starts", showarrow=False, xanchor="left",
                           xshift=6, font=dict(size=17, color=GREY), row=row, col=1)
    fig.add_annotation(x=20, y=0.05, text="0.05 rad", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(size=17, color=GREY), row=1, col=1)
    if last:
        fig.add_annotation(x=10, y=0.05, text="settles 0.05 rad (2.9°) off", ax=0, ay=-55, arrowcolor=BLUE,
                           font=dict(size=19, color=BLUE), row=1, col=1)
        fig.add_annotation(x=t[th_r.argmax()], y=th_r.max(), text="still growing: 0.26 rad", ax=-150, ay=-10,
                           arrowcolor=RED, font=dict(size=19, color=RED), row=2, col=1)
    fig.update_xaxes(range=[0, 20], title_text="time (s)")
    fig.update_yaxes(title_text="heading error (rad)", range=[-0.02, 0.13], row=1, col=1)
    fig.update_yaxes(title_text="heading error (rad)", range=[-0.3, 0.3], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=950, margin=dict(l=100, r=30, t=150, b=70),
                      title=dict(x=0.5, y=0.97, text=f"a wheel drags: 0.02 N·m on the heading, PD loop<br>t = {tn:.0f} s"))
    return fig


times = list(range(0, 21))
figs = [frame(x) for x in times] + [frame(20, last=True)]
make_gif(figs, here / "problem_anim", fps=3, holds=[3] + [1] * 20 + [12], keys=[8, 21], cols=2, width=800)
