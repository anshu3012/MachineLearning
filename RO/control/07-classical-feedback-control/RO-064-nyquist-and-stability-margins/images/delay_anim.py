"""The opening problem: RO-061's turn from 0 to 0.5 rad with the PD gains Kp = 0.4 N m/rad and Kd = 0.08 N m s/rad,
run three times with the heading reaching the controller later: no delay, 0.1 s, 0.25 s. Left: the robot from above.
Right: the heading over time, earlier runs kept faint. No delay: peak 0.763 rad (53 percent past the target);
0.1 s: 0.865 rad (73 percent); 0.25 s: the swings grow, 1.13, 1.48, 1.95 rad, and the torque sits at its 0.2 N m limit.
Run: python delay_anim.py -> delay_anim.gif, delay_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import find_peaks
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import simulate_heading
from robotdraw import robot

here = Path(__file__).parent
T_END, STEP = 12.0, 0.5
t = np.arange(0, T_END + 5e-4, 1e-3)
TAUS = [0.0, 0.1, 0.25]
COL = {0.0: BLUE, 0.1: ORANGE, 0.25: RED}
runs = {tau: simulate_heading(t, np.full_like(t, STEP), tau=tau) for tau in TAUS}
peaks = {tau: [runs[tau][0][i] for i in find_peaks(runs[tau][0])[0]] for tau in TAUS}
assert abs(peaks[0.0][0] - 0.763) < 5e-4 and abs(peaks[0.1][0] - 0.865) < 5e-4
assert np.allclose(np.round(peaks[0.25][:3], 2), [1.13, 1.48, 1.95])
LABEL = {0.0: "no delay: peak 0.763 rad, settles",
         0.1: "0.1 s late: peak 0.865 rad, settles slower",
         0.25: "0.25 s late: swings grow (1.13, 1.48, 1.95 rad)"}
TK = np.round(np.arange(0, T_END + 1e-9, STEP), 2)


def frame(tau, tk, last=False):
    th = runs[tau][0]
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.36, 0.64], horizontal_spacing=0.08,
                        subplot_titles=["the robot from above", "heading θ over time"])
    fig.add_trace(go.Scatter(x=[0, 0.66 * np.cos(STEP)], y=[0, 0.66 * np.sin(STEP)], mode="lines",
                             line=dict(color=GREY, width=3, dash="dash")), 1, 1)
    fig.add_annotation(x=0.66 * np.cos(STEP), y=0.66 * np.sin(STEP), text="target 0.5 rad", showarrow=False,
                       xanchor="right", yanchor="bottom", yshift=6, font=dict(color=GREY, size=19), row=1, col=1)
    for tr in robot((0, 0, th[k]), scale=1.6):
        fig.add_trace(tr, 1, 1)
    for old in TAUS[:TAUS.index(tau)]:
        fig.add_trace(go.Scatter(x=t, y=runs[old][0], mode="lines", line=dict(color=COL[old], width=3),
                                 opacity=0.35), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=th[:k + 1], mode="lines", line=dict(color=COL[tau], width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[t[k]], y=[th[k]], mode="markers", marker=dict(color=COL[tau], size=14)), 1, 2)
    fig.add_trace(go.Scatter(x=[0, T_END], y=[STEP, STEP], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  1, 2)
    shown = TAUS if last else TAUS[:TAUS.index(tau) + 1]
    for i, tt in enumerate(shown):
        fig.add_annotation(x=0.36, y=-0.52 - 0.2 * i, xref="x2", yref="y2", text=LABEL[tt], showarrow=False,
                           xanchor="left", font=dict(color=COL[tt], size=18))
    fig.update_xaxes(range=[-0.75, 0.75], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.75, 0.9], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, T_END], row=1, col=2)
    fig.update_yaxes(title="heading θ (rad)", range=[-1.3, 2.1], row=1, col=2)
    head = ("the same turn, three delays: only the delay changed" if last else
            f"turn 0 → 0.5 rad, {'no delay' if tau == 0 else f'heading {tau:g} s late'}:   t = {tk:.1f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=640, showlegend=False,
                      margin=dict(l=40, r=30, t=120, b=70), title=dict(x=0.5, y=0.95, text=head))
    fig.update_annotations(selector=dict(xref="paper"), font_size=21)
    return fig


figs, holds = [], []
for tau in TAUS:
    for j, tk in enumerate(TK):
        figs.append(frame(tau, tk))
        holds.append(6 if j == 0 else 1)
    holds[-1] = 8
figs.append(frame(0.25, T_END, last=True))
holds.append(30)
n = len(TK)
make_gif(figs, here / "delay_anim", fps=6, holds=holds, keys=[n - 1, 2 * n - 1, 2 * n + 12, len(figs) - 1], cols=2,
         width=900)
