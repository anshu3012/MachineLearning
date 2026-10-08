"""EM fits the beam model to the 1000 wall readings. Each frame is one EM round: the bars are the data
(counts per 0.05 m bin), the black line is how many readings the current model expects per bin, and the right
panel tracks the log-likelihood. Start: equal weights 0.25, sigma 0.3 m, lambda 0.5. Run -> em_fit.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from beammodel import em, load
from gifkit import BLUE, FONT, RED, make_gif
from histkit import EDGES, counts, expected_counts

here = Path(__file__).parent
z = load()
c = counts(z)
mid = (EDGES[:-1] + EDGES[1:]) / 2
w, sig, lam, hist = em(z, history=True)
ll = [h[3] for h in hist]
ITERS = [0, 1, 2, 3, 5, 10, 60]


def frame(k):
    wk, sk, lk, llk = hist[k]
    e = expected_counts(len(z), wk, sk, lk)
    fig = make_subplots(rows=2, cols=2, column_widths=[0.62, 0.38], specs=[[{}, {"rowspan": 2}], [{}, None]],
                        subplot_titles=["data and model", "log-likelihood", "zoom: counts up to 25"],
                        vertical_spacing=0.17, horizontal_spacing=0.11)
    for r in (1, 2):
        fig.add_trace(go.Bar(x=mid, y=c, width=0.05, marker=dict(color=BLUE, opacity=0.45, line=dict(width=0))), row=r, col=1)
        fig.add_trace(go.Scatter(x=mid, y=e, mode="lines", line=dict(color="black", width=2.5, shape="hvh")), row=r, col=1)
        fig.update_xaxes(range=[0, 5.1], dtick=1, row=r, col=1)
    fig.update_xaxes(title="reading z (m)", row=2, col=1)
    fig.update_yaxes(range=[0, 330], row=1, col=1)
    fig.update_yaxes(range=[0, 25], row=2, col=1)
    fig.add_trace(go.Scatter(x=list(range(k + 1)), y=ll[:k + 1], mode="lines+markers", line=dict(color=RED, width=3)),
                  row=1, col=2)
    fig.update_xaxes(title="EM round", range=[-1, 61], row=1, col=2)
    fig.update_yaxes(range=[-1000, 550], row=1, col=2)
    title = (f"round {k}:  hit {wk['hit']:.3f}, short {wk['short']:.3f}, max {wk['max']:.3f}, rand {wk['rand']:.3f}"
             f"<br>σ<sub>hit</sub> = {sk:.3f} m,  λ<sub>short</sub> = {lk:.2f} per m,  log-likelihood {llk:.0f}")
    fig.update_layout(template="simple_white", width=1150, height=720, font=FONT, showlegend=False, bargap=0,
                      margin=dict(l=70, r=30, t=130, b=70), title=dict(text=title, x=0.5, font_size=21))
    fig.update_annotations(selector=dict(yref="paper"), font_size=20)
    return fig


figs = [frame(k) for k in ITERS]
make_gif(figs, here / "em_fit", fps=2, holds=[4, 3, 3, 3, 3, 3, 8], keys=[0, 1, len(ITERS) - 1], cols=1, width=950)
assert all(b >= a - 1e-6 for a, b in zip(ll, ll[1:]))   # EM never lowers the log-likelihood
