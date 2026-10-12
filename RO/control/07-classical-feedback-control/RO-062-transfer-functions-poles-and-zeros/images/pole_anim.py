"""Where a pole sits sets the shape of what it adds to a response. Each pole p adds a term e^(p t); a pair of complex
poles sigma +- j omega adds e^(sigma t) cos(omega t). Left: the plane of complex numbers, the left half-plane shaded
green, the right half-plane red. Right: the term the pole (or pair) adds, starting at 1. Stage 1: one real pole moves
from -2 to +0.3: a fast fade, a slow fade, a constant at 0, growth. Stage 2: a pair with real part -0.5 moves up from
+-1j to +-3j: faster swings. Stage 3: the pair at +-2j moves right from -0.5 to +0.2: the swing fades slower, then
lasts for ever on the axis, then grows. Run: python pole_anim.py -> pole_anim.gif, pole_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
t = np.linspace(0, 6, 3001)
STEPS = ([("stage 1: one real pole", complex(p, 0)) for p in (-2, -1.5, -1, -0.5, -0.25, 0, 0.15, 0.3)]
         + [("stage 2: a pair moves up", complex(-0.5, w)) for w in (1, 1.5, 2, 2.5, 3)]
         + [("stage 3: a pair moves right", complex(s, 2)) for s in (-0.5, -0.3, -0.15, 0, 0.1, 0.2)])


def term(p):
    return np.exp(p.real * t) * np.cos(p.imag * t)


def frame(stage, p):
    pts = [p] if p.imag == 0 else [p, p.conjugate()]
    lab = f"pole at {p.real:g}" if p.imag == 0 else f"poles at {p.real:g} ± {p.imag:g}j"
    kind = ("fades" if p.real < 0 else "grows" if p.real > 0 else "stays") + \
           ("" if p.imag == 0 else ", swinging" if p.real != 0 else ", swinging for ever")
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], horizontal_spacing=0.1,
                        subplot_titles=[lab, f"the term it adds {kind}"])
    fig.add_trace(go.Scatter(x=[-2.5, 0, 0, -2.5, -2.5], y=[-3.5, -3.5, 3.5, 3.5, -3.5], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(84,162,75,0.15)"), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 1, 1, 0, 0], y=[-3.5, -3.5, 3.5, 3.5, -3.5], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(228,87,86,0.15)"), 1, 1)
    fig.add_trace(go.Scatter(x=[-2.5, 1], y=[0, 0], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-3.5, 3.5], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_annotation(x=-2.4, y=3.3, text="left half-plane", showarrow=False, xanchor="left", yanchor="top",
                       font=dict(color="#3d7a35", size=17), row=1, col=1)
    fig.add_annotation(x=0.95, y=3.3, text="right", showarrow=False, xanchor="right", yanchor="top",
                       font=dict(color=RED, size=17), row=1, col=1)
    fig.add_trace(go.Scatter(x=[q.real for q in pts], y=[q.imag for q in pts], mode="markers",
                             marker=dict(symbol="x", size=20, color=RED, line=dict(width=2))), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 6], y=[0, 0], mode="lines", line=dict(color=GREY, width=1.5, dash="dash")), 1, 2)
    fig.add_trace(go.Scatter(x=t, y=term(p), mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    fig.update_xaxes(range=[-2.5, 1], title="real part", row=1, col=1)
    fig.update_yaxes(range=[-3.5, 3.5], title="imaginary part", row=1, col=1)
    fig.update_xaxes(range=[0, 6], title="time t (s)", row=1, col=2)
    fig.update_yaxes(range=[-3, 3], row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1200, height=600, showlegend=False,
                      margin=dict(l=70, r=30, t=140, b=70), title=dict(x=0.5, y=0.96, text=stage))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(s, p) for s, p in STEPS]
holds = [10 if (p.real == 0 or i in (0, 8, 13)) else 5 for i, (_, p) in enumerate(STEPS)]
holds[-1] = 30
make_gif(figs, here / "pole_anim", fps=5, holds=holds, keys=[0, 3, 5, 7, 12, 15, 16, len(STEPS) - 1], cols=2,
         width=850)
