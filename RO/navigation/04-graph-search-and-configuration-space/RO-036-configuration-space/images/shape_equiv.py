"""Same shape or not: the circle of headings (theta = 0 and theta = 2 pi are one point) is stretched into an ellipse
and a squashed loop: no cut and no glue, so the shape is the same (topologically equivalent). Then it is cut at
theta = 0 and opened into a straight segment from 0 to 2 pi: the cut gives two ends, which a circle does not have,
so the segment is a different shape. The point theta = pi stays where it is throughout.
Run: python shape_equiv.py -> shape_equiv.gif, shape_equiv_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
TH = np.linspace(0, 2 * np.pi, 400)


def stretched(a):
    """The circle stretched by amount a (0 = circle): still one closed loop."""
    x = np.cos(TH) * (1 + 0.45 * a) + 0.45 * a
    y = np.sin(TH) * (1 - 0.35 * a) + 0.25 * a * np.sin(2 * TH)
    return x, y


def opened(k):
    """The circle cut at theta = 0 and opened with curvature k (1 = circle, 0 = straight); theta = pi stays at
    (-1, 0) with the same tangent, and arc length is kept."""
    u = TH - np.pi
    if k < 1e-6:
        return -np.ones_like(u), -u
    R = 1 / k
    return -1 + R - R * np.cos(k * u), -R * np.sin(k * u)


def frame(title, x, y, closed, labels, note):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=BLUE, width=6)))
    k_pi = np.argmin(abs(TH - np.pi))
    fig.add_trace(go.Scatter(x=[x[k_pi]], y=[y[k_pi]], mode="markers+text", marker=dict(size=13, color=GREEN),
                             text=["θ = π  "], textposition="middle left", textfont=dict(size=24, color=GREEN)))
    if closed:
        fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode="markers+text", marker=dict(size=13, color=ORANGE),
                                 text=["  θ = 0 = 2π"], textposition="middle right",
                                 textfont=dict(size=24, color=ORANGE)))
    else:
        fig.add_trace(go.Scatter(x=[x[0], x[-1]], y=[y[0], y[-1]], mode="markers+text",
                                 marker=dict(size=13, color=RED), text=["  end θ = 0", "  end θ = 2π"],
                                 textposition="middle right", textfont=dict(size=24, color=RED)))
    for txt, (lx, ly) in labels:
        fig.add_annotation(x=lx, y=ly, text=txt, showarrow=False, font=dict(size=20))
    fig.add_annotation(x=0.5, y=-0.06, xref="paper", yref="paper", text=note, showarrow=False,
                       font=dict(size=22, color=BLUE if closed else RED))
    fig.update_layout(template="simple_white", font=FONT, width=760, height=860, showlegend=False,
                      margin=dict(l=20, r=20, t=110, b=80), title=dict(x=0.5, text=title),
                      xaxis=dict(visible=False, range=[-2.6, 3.0]),
                      yaxis=dict(visible=False, range=[-3.6, 3.6], scaleanchor="x"))
    return fig


figs, holds = [], []
SAME = "no cut, no glue: the same shape"
figs.append(frame("the headings form a circle:<br>θ = 0 and θ = 2π are one point", *stretched(0), True, [],
                  "a heading can turn round and round without meeting an end"))
holds.append(5)
for a in (0.33, 0.66, 1.0):
    figs.append(frame("stretch and bend the circle", *stretched(a), True, [], SAME))
    holds.append(2)
holds[-1] = 5
for a in (0.5, 0.0):
    figs.append(frame("back to the circle", *stretched(a), True, [], SAME))
    holds.append(1)
for k in (0.97, 0.7, 0.45, 0.2, 0.0):
    figs.append(frame("cut at θ = 0 and open it out", *opened(k), False, [],
                      "the cut made two ends: a different shape"))
    holds.append(2)
figs.append(frame("a segment from 0 to 2π:<br>not the same shape as the circle", *opened(0.0), False, [],
                  "two ends that the circle did not have"))
holds.append(10)
make_gif(figs, here / "shape_equiv", fps=2, holds=holds, keys=[0, 3, 8, len(figs) - 1], cols=2, width=620)
