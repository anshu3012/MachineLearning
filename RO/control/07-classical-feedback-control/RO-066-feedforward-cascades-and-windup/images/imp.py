"""The internal model principle at the dock's creep speed, 0.05 m/s: an out-of-round wheel (radius 0.05 m, so one
turn per 6.28 s at 1 rad/s) pushes and drags with 0.5 sin(t) N. One frame per 0.3 s for 30 s. Top: speed; PI alone
swings from 0.027 to 0.073 m/s for ever (amplitude 0.023 m/s); PI plus a resonator at 1 rad/s settles
on 0.05 m/s. Bottom: the wheel's push and the resonator's output; the resonator learns a 0.5 N wave that mirrors the
wheel's push and cancels it. Run: python imp.py -> imp.gif, imp_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from robotctl import RES, speed_loop

here = Path(__file__).parent
T = 30
d = lambda t: 0.5 * np.sin(t)
pi_ = speed_loop(60, lambda t: 0.05, v0=0.05, ff=True, i0=0.0, dist=d)
rs = speed_loop(60, lambda t: 0.05, v0=0.05, ff=True, i0=0.0, dist=d, res=RES)
late = pi_["t"] >= 40
assert abs(pi_["v"][late].min() - 0.027) < 5e-4 and abs(pi_["v"][late].max() - 0.073) < 5e-4
assert abs((pi_["v"][late].max() - pi_["v"][late].min()) / 2 - 0.0227) < 1e-4
assert np.abs(rs["v"][late] - 0.05).max() < 1e-6 and abs(np.abs(rs["ures"][late]).max() - 0.5) < 1e-3
n = int(round(T / 0.01)) + 1
t = pi_["t"][:n]
dist = d(t)


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.13)
    fig.add_trace(go.Scatter(x=[0, T], y=[0.05, 0.05], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="wanted, 0.05 m/s"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=pi_["v"][:k + 1], mode="lines", line=dict(color=RED, width=4),
                             name="PI"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=rs["v"][:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="PI + resonant term at 1 rad/s"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=dist[:k + 1], mode="lines", line=dict(color=ORANGE, width=4),
                             name="wheel's push"), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=rs["ures"][:k + 1], mode="lines", line=dict(color=BLUE, width=4, dash="dash"),
                             name="resonant term's output"), row=2, col=1)
    fig.add_annotation(x=0.02, y=1.04, xref="paper", yref="paper", text=f"creeping at 0.05 m/s, t = {t[k]:.1f} s",
                       showarrow=False, font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0.0, 0.1], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[-0.8, 0.8], title="force (N)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=800, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.5, xanchor="center", y=-0.14, orientation="h", font=dict(size=18)))
    return fig


ks = list(range(0, n, 30))
figs = [frame(k) for k in ks]
make_gif(figs, here / "imp", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(600), len(ks) - 1], cols=1, width=850)
