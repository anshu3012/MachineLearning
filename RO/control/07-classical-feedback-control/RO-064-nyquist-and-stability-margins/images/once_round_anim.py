"""Once round the loop at the gain crossover frequency, 2.08 rad/s, where the heading loop's gain is 1. Left: the sine
put in at A (grey, dashed) and the sine that comes back at B, B = -L(j w) x A. With no delay B leads A by 22.6 degrees
(0.19 s). Each frame adds 0.02 s of delay, which slides B later; at 0.19 s B lands on A, so the loop can keep the sine
going by itself. Right: the same in the complex plane: the point L(j w) e^{-j w tau} on the circle of radius 1 turns
clockwise from -157.4 degrees to -180 degrees, the point -1.
Run: python once_round_anim.py -> once_round_anim.gif, once_round_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import L_head, deg, margins

here = Path(__file__).parent
m = margins(L_head)
W, DM = m["wgc"], m["dm"]
L0 = L_head(1j * W)
assert abs(W - 2.08) < 5e-3 and abs(abs(L0) - 1) < 1e-9 and abs(deg(L0) + 157.4) < 0.05 and abs(m["pm"] - 22.6) < 0.05
assert abs(DM - 0.19) < 5e-3
t = np.linspace(0, 6, 601)
A = np.sin(W * t)
TAUS = list(np.round(np.arange(0, 0.181, 0.02), 2)) + [DM]


def frame(tau, last=False):
    Lt = L0 * np.exp(-1j * W * tau)
    ph = np.angle(-Lt)                       # B = -L x A: phase of B relative to A
    B = np.sin(W * t + ph)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.1,
                        subplot_titles=["dashed: in at A; solid: back at B", "L(jω) × the delay's factor, at ω = 2.08 rad/s"])
    fig.add_trace(go.Scatter(x=t, y=A, mode="lines", line=dict(color=GREY, width=4, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=t, y=B, mode="lines", line=dict(color=RED if last else BLUE, width=4)), 1, 1)
    lead = np.degrees(ph)
    txt = ("B lies on A: the loop feeds itself" if last else
           f"B ahead of A by {lead:.1f}° ({lead / np.degrees(W):.2f} s)")
    fig.add_annotation(x=3.0, y=1.32, text=txt, showarrow=False, font=dict(color=RED if last else BLUE, size=20),
                       row=1, col=1)
    a = np.linspace(0, 2 * np.pi, 361)
    fig.add_trace(go.Scatter(x=np.cos(a), y=np.sin(a), mode="lines", line=dict(color=GREY, width=1.5, dash="dot")), 1, 2)
    fig.add_trace(go.Scatter(x=[-1.6, 1.3], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)), 1, 2)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.15, 1.15], mode="lines", line=dict(color=GREY, width=1)), 1, 2)
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="x")), 1, 2)
    fig.add_annotation(x=-1, y=0, text="−1", showarrow=False, yshift=22, xshift=-10, font=dict(color=RED, size=20),
                       row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, Lt.real], y=[0, Lt.imag], mode="lines+markers",
                             line=dict(color=RED if last else BLUE, width=4),
                             marker=dict(size=[0, 16], color=RED if last else BLUE)), 1, 2)
    fig.add_annotation(x=-0.15, y=-1.32, text=f"angle {deg(Lt) if not last else -180:.1f}°, length 1".replace("-", "−"),
                       showarrow=False, font=dict(size=19, color=RED if last else BLUE), xanchor="center", row=1, col=2)
    fig.update_xaxes(title="time t (s)", range=[0, 6], row=1, col=1)
    fig.update_yaxes(title="signal", range=[-1.2, 1.5], row=1, col=1)
    fig.update_xaxes(range=[-1.6, 1.3], visible=False, row=1, col=2)
    fig.update_yaxes(range=[-1.45, 1.2], visible=False, scaleanchor="x2", scaleratio=1, row=1, col=2)
    head = (f"delay T<sub>d</sub> = {DM:.2f} s: the point is at −1, gain 1 and phase −180°" if last else
            f"extra delay T<sub>d</sub> = {tau:.2f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=560, showlegend=False,
                      margin=dict(l=80, r=30, t=120, b=70), title=dict(x=0.5, y=0.95, text=head))
    fig.update_annotations(selector=dict(xref="paper"), font_size=20)
    return fig


figs = [frame(tau, last=(i == len(TAUS) - 1)) for i, tau in enumerate(TAUS)]
make_gif(figs, here / "once_round_anim", fps=2, holds=[4] + [1] * (len(figs) - 2) + [12], keys=[0, 5, len(figs) - 1],
         cols=1, width=900)
