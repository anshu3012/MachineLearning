"""Samples stand for a distribution, as an animation: positions are drawn one at a time from the exact belief after
the second reading (two modes, at door 2 and door 3). Top: the samples on the corridor (doors shaded), the newest one
red. Bottom: their histogram (share of samples per 0.25 m, as a density) against the exact belief (blue line). The
build-up pauses at 20, 200 and 2000 samples: ragged at 20, close at 200, following the curve at 2000.
Run: python cloud_anim.py -> cloud_anim.gif, cloud_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from pfsim import DOORS, LOOP, grid_belief

here = Path(__file__).parent
xs, _, bels = grid_belief()
bel, dx = bels[1], xs[1] - xs[0]                         # exact belief after reading 2 (per m), cell width (m)
share = [bel[(xs >= a) & (xs <= b)].sum() * dx for a, b in DOORS]
assert np.allclose(np.round(share, 2), [0.01, 0.50, 0.50])  # two modes: door 2 and door 3 (Section 4.5 table)
N = 2000
rng = np.random.default_rng(4)
cdf = np.cumsum(bel * dx)
S = xs[np.searchsorted(cdf, rng.uniform(0, cdf[-1], N))] + rng.uniform(-dx / 2, dx / 2, N)   # samples (m)
jitter = np.random.default_rng(7).uniform(0.15, 0.85, N)
COUNTS = list(range(1, 21)) + [30, 40, 60, 80, 100, 130, 160, 200] + [300, 400, 600, 800, 1000, 1300, 1600, 2000]
PAUSE = {20: "20 samples: the bars are ragged", 200: "200 samples: the bars come closer to the curve",
         2000: "2000 samples: the bars follow the two modes"}
assert set(PAUSE) <= set(COUNTS) and COUNTS[-1] == N


def frame(n, title):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.38, 0.62], vertical_spacing=0.12)
    for a, b in DOORS:
        for r in (1, 2):
            fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, yref="y domain" if r == 1 else "y2 domain",
                          xref="x" if r == 1 else "x2", fillcolor=ORANGE, opacity=0.18, line_width=0, layer="below")
    if n:
        fig.add_trace(go.Scatter(x=S[:n], y=jitter[:n], mode="markers", marker=dict(size=11 if n <= 200 else 6,
                                 color=BLUE, opacity=0.6 if n <= 200 else 0.4, line=dict(width=0))), row=1, col=1)
        hist, e = np.histogram(S[:n], bins=40, range=(0, LOOP))
        fig.add_trace(go.Bar(x=(e[:-1] + e[1:]) / 2, y=hist / (n * (e[1] - e[0])), width=e[1] - e[0],
                             marker_color=GREY, opacity=0.7), row=2, col=1)
    if 0 < n <= 20:                                         # the newest sample, one at a time
        fig.add_trace(go.Scatter(x=[S[n - 1]], y=[jitter[n - 1]], mode="markers", marker=dict(size=16, color=RED)),
                      row=1, col=1)
        fig.add_annotation(xref="x domain", yref="y domain", x=1, y=1.04, xanchor="right", yanchor="bottom",
                           showarrow=False, text=f"newest sample (red): {S[n - 1]:.2f} m", font=dict(size=20, color=RED))
    fig.add_trace(go.Scatter(x=xs, y=bel, mode="lines", line=dict(color=BLUE, width=3)), row=2, col=1)
    fig.add_annotation(xref="x domain", yref="y domain", x=0, y=1.04, xanchor="left", yanchor="bottom", showarrow=False,
                       text=f"<b>samples drawn: {n}</b>", font=dict(size=21))
    fig.update_xaxes(range=[0, LOOP], dtick=1, row=1, col=1, showticklabels=False)
    fig.update_yaxes(visible=False, range=[0, 1], row=1, col=1)
    fig.update_xaxes(title="position x (m)", range=[0, LOOP], dtick=1, row=2, col=1)
    fig.update_yaxes(title="belief (per m)", range=[0, 2.4], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=820, showlegend=False, bargap=0,
                      margin=dict(l=90, r=40, t=110, b=70),
                      title=dict(x=0.5, y=0.97, font=dict(size=23), text=title))
    fig.add_annotation(xref="paper", yref="paper", x=1, y=0.575, xanchor="right", showarrow=False, font=dict(size=16),
                       text="grey bars: share of samples per 0.25 m; blue line: exact belief after reading 2")
    return fig


figs, holds, keys = [frame(0, "1. the exact belief after reading 2: two modes, at door 2 and door 3")], [8], [0]
for n in COUNTS:
    title = PAUSE.get(n, "draw positions from the belief, one at a time" if n <= 20 else "keep drawing")
    figs.append(frame(n, title))
    holds.append(10 if n in PAUSE else 2 if n <= 20 else 1)
    if n in PAUSE:
        keys.append(len(figs) - 1)
holds[-1] = 20
make_gif(figs, here / "cloud_anim", fps=4, holds=holds, keys=keys, cols=2, width=900)
