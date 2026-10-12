"""The opening problem: the robot is told to turn in place from 0 to 0.5 rad. Its PD heading loop has the first-try
gains Kp = 0.4 N m/rad and Kd = 0.08 N m s/rad. Left: the robot from above, the target direction dashed. Right: the
heading over time. The heading swings to 0.763 rad, 53 percent past the target, and stays outside the 2 percent band
until 9.8 s. Run: python problem_anim.py -> problem_anim.gif, problem_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from robotdraw import robot
from stepkit import KD_OLD, TH_REF, heading_pd, step_info

here = Path(__file__).parent
t = np.linspace(0, 12, 12001)
th, _, _ = heading_pd(t, kd=KD_OLD)
info = step_info(t, th, TH_REF, TH_REF)
assert abs(info["peak"] - 0.763) < 5e-4 and abs(info["overshoot"] - 0.527) < 5e-4 and abs(info["settle"] - 9.8) < 0.01
TK = np.round(np.arange(0, 12.01, 0.25), 2)


def ray(ang, r=0.66):
    return [0, r * np.cos(ang)], [0, r * np.sin(ang)]


def frame(tk, last=False):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                        subplot_titles=["the robot from above", f"heading θ = {th[k]:.3f} rad"])
    x, y = ray(TH_REF)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=3, dash="dash")), 1, 1)
    fig.add_annotation(x=x[1], y=y[1], text="target 0.5 rad", showarrow=False, xanchor="right", yanchor="bottom", xshift=-30,
                       yshift=6, font=dict(color=GREY, size=19), row=1, col=1)
    for tr in robot((0, 0, th[k]), scale=1.6):
        fig.add_trace(tr, 1, 1)
    far = th[:k + 1].max()
    arc = np.linspace(0, far, 60)
    fig.add_trace(go.Scatter(x=0.56 * np.cos(arc), y=0.56 * np.sin(arc), mode="lines",
                             line=dict(color=RED, width=3, dash="dot")), 1, 1)
    if far > TH_REF:
        fig.add_annotation(x=-0.72, y=0.86, text=f"red dots: furthest swing, {far:.3f} rad",
                           showarrow=False, xanchor="left", yanchor="top", font=dict(color=RED, size=18),
                           row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=th[:k + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[0, 12], y=[TH_REF, TH_REF], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  1, 2)
    fig.add_trace(go.Scatter(x=[t[k]], y=[th[k]], mode="markers", marker=dict(color=ORANGE, size=14)), 1, 2)
    if tk >= info["t_peak"]:
        fig.add_annotation(x=info["t_peak"], y=info["peak"], text="peak 0.763 rad:<br>53 % past the target",
                           ax=95, ay=-25, arrowcolor=RED, font=dict(color=RED, size=19), row=1, col=2)
    if last:
        fig.add_trace(go.Scatter(x=[0, 12, 12, 0, 0], y=[0.49, 0.49, 0.51, 0.51, 0.49], fill="toself", mode="lines",
                                 line=dict(width=0), fillcolor="rgba(84,162,75,0.25)"), 1, 2)
        fig.add_trace(go.Scatter(x=[info["settle"]] * 2, y=[0, 0.85], mode="lines",
                                 line=dict(color=RED, width=3, dash="dot")), 1, 2)
        fig.add_annotation(x=info["settle"], y=0.12, text="inside the 2 % band<br>(green) only after 9.8 s", showarrow=False,
                           xanchor="right", xshift=-8, font=dict(color=RED, size=19), row=1, col=2)
    fig.update_xaxes(range=[-0.75, 0.75], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.6, 0.9], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, 12], row=1, col=2)
    fig.update_yaxes(title="heading θ (rad)", range=[0, 0.85], row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620, showlegend=False,
                      margin=dict(l=40, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.95, text=f"turn 0 → 0.5 rad with Kp = 0.4, Kd = 0.08:   t = {tk:.2f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK] + [frame(12.0, last=True)]
make_gif(figs, here / "problem_anim", fps=8, holds=[8] + [1] * (len(TK) - 1) + [30],
         keys=[0, 6, 16, len(figs) - 1], cols=2, width=900)
