"""Why short readings fall off exponentially. The 3 m of beam in front of the wall is cut into 30 cells of
0.1 m; in each trial every cell is blocked (by a person, a chair leg...) with probability 0.2, independently.
The beam stops at the first blocked cell. The histogram of where it stops builds up trial by trial and
matches 0.2 x 0.8^(k-1) for cell k, which falls by the same factor 0.8 per cell. Run -> first_hit.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
rng = np.random.default_rng(3)
P, N = 0.2, 30
trials = rng.random((5000, N)) < P
first = np.where(trials.any(1), trials.argmax(1), N)          # index of the first blocked cell, N = reached the wall
SHOW = [1, 2, 3, 4, 5, 20, 100, 500, 5000]
k = np.arange(N)
geo = P * (1 - P) ** k


def frame(t):
    cells = trials[t - 1]
    fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75], vertical_spacing=0.17,
                        subplot_titles=[f"trial {t}: the beam stops at the first blocked cell",
                                        f"where the beam stopped, share of {t} trial{'s' if t > 1 else ''}"])
    for j in range(N):
        col = ORANGE if cells[j] else "white"
        fig.add_shape(type="rect", x0=j * 0.1, x1=j * 0.1 + 0.095, y0=0, y1=1, fillcolor=col, line=dict(color=GREY, width=1), opacity=1, layer="below",
                      row=1, col=1)
    f = first[t - 1]
    stop = (f * 0.1 if f < N else 3.0)
    fig.add_trace(go.Scatter(x=[0, stop], y=[0.5, 0.5], mode="lines", line=dict(color=RED, width=5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[stop], y=[0.5], mode="markers", marker=dict(color=RED, size=16)), row=1, col=1)
    fig.add_shape(type="rect", x0=3.0, x1=3.1, y0=0, y1=1, fillcolor=GREY, line=dict(width=0), row=1, col=1)
    fig.update_xaxes(range=[-0.05, 3.15], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[-0.1, 1.1], visible=False, row=1, col=1)
    share = np.bincount(first[:t], minlength=N + 1)[:N] / t
    fig.add_trace(go.Bar(x=k * 0.1 + 0.05, y=share, width=0.09, marker=dict(color=ORANGE)), row=2, col=1)
    fig.add_trace(go.Scatter(x=k * 0.1 + 0.05, y=geo, mode="lines+markers", line=dict(color=BLUE, width=3),
                             marker=dict(size=7)), row=2, col=1)
    fig.update_xaxes(title="distance along the beam (m); the wall is at 3 m", range=[-0.05, 3.15], dtick=0.5, row=2, col=1)
    fig.update_yaxes(title="share of trials", range=[0, 0.42 if t < 20 else 0.25], row=2, col=1)
    fig.add_annotation(x=1.6, y=0.85, xref="x2", yref="y2 domain", showarrow=False, font=dict(color=BLUE, size=19),
                       text="blue: 0.2 × 0.8<sup>k − 1</sup> for cell k")
    fig.update_layout(template="simple_white", width=1000, height=650, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=60, b=70))
    fig.update_annotations(selector=dict(yref="paper"), font_size=20)
    return fig


figs = [frame(t) for t in SHOW]
make_gif(figs, here / "first_hit", fps=2, holds=[3, 2, 2, 2, 2, 3, 3, 3, 8], keys=[0, len(SHOW) - 1], cols=1, width=900)
share = np.bincount(first, minlength=N + 1)[:N] / len(first)
assert abs(share[0] - 0.2) < 0.02 and abs(share[5] - geo[5]) < 0.015
