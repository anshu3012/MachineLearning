"""Pushing a bell through the beacon's curve. Each frame: the input bell of positions (top), the curve h(x) with its
tangent line at the mean (middle), and the output: a histogram of 200,000 pushed samples against the bell the tangent
line predicts (right). Far from the beacon the two agree; near it the true output is skewed and the tangent bell
is too narrow and in the wrong place, worst when the input is wide.
Run: python curve_gaussian.py -> curve_gaussian.gif, curve_gaussian_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from ekfsim import dh, h

here = Path(__file__).parent
CASES = [(1.0, 0.5), (2.5, 0.5), (4.0, 0.5), (5.5, 0.5), (5.5, 1.5)]
rng = np.random.default_rng(0)


def normal(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def frame(mu, s):
    xs = rng.normal(mu, s, 200_000)
    ys = h(xs)
    m_lin, s_lin = h(mu), abs(dh(mu)) * s
    fig = make_subplots(rows=2, cols=2, column_widths=[0.7, 0.3], row_heights=[0.28, 0.72], shared_xaxes=True,
                        shared_yaxes=True, horizontal_spacing=0.02, vertical_spacing=0.03)
    g = np.linspace(-1, 12, 600)
    fig.add_trace(go.Scatter(x=g, y=normal(g, mu, s), line=dict(color=BLUE, width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=g, y=h(g), line=dict(color="black", width=4)), row=2, col=1)
    fig.add_trace(go.Scatter(x=g, y=h(mu) + dh(mu) * (g - mu), line=dict(color=PURPLE, width=3, dash="dash")), row=2, col=1)
    fig.add_trace(go.Scatter(x=[mu], y=[h(mu)], mode="markers", marker=dict(color=PURPLE, size=12)), row=2, col=1)
    gy = np.linspace(0, 8, 600)
    fig.add_trace(go.Histogram(y=ys, histnorm="probability density", ybins=dict(start=0, end=8, size=0.05),
                               marker_color=ORANGE, opacity=0.85), row=2, col=2)
    fig.add_trace(go.Scatter(x=normal(gy, m_lin, s_lin), y=gy, line=dict(color=PURPLE, width=4)), row=2, col=2)
    fig.update_xaxes(range=[-1, 12], row=2, col=1, title="position x (m)")
    fig.update_yaxes(range=[0, 8], row=2, col=1, title="reading h(x) (m)")
    fig.update_xaxes(title="density", range=[0, 3.6], row=2, col=2)
    fig.update_yaxes(title="density", row=1, col=1, range=[0, 0.9])
    fig.update_layout(template="simple_white", font=FONT, width=1050, height=820, showlegend=False,
                      margin=dict(l=80, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.97, font=dict(size=21), text=(
                          f"input: mean {mu} m, sd {s} m<br>true output: mean {ys.mean():.2f}, sd {ys.std():.2f}"
                          f"   |   tangent line: mean {m_lin:.2f}, sd {s_lin:.2f}")))
    fig.add_annotation(xref="paper", yref="paper", x=0.98, y=0.66, showarrow=False, align="right", font=dict(size=16),
                       text="orange: pushed samples<br>purple: tangent-line bell")
    return fig


figs = [frame(*c) for c in CASES]
make_gif(figs, here / "curve_gaussian", fps=1, holds=[3, 2, 2, 3, 4], keys=[0, 3, 4], cols=1, width=850)
