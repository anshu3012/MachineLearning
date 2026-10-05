"""Why the learning rate has a limit (Plotly frames -> overshoot.gif, overshoot_frames.png). One direction of the loss
bowl with curvature h = 353 (the steepest direction of the diabetes data). Each step multiplies the distance from the
bottom by 1 - eta * h: with eta = 0.005 that is -0.765 (jumps across, lands closer); with eta = 0.006 it is -1.118
(jumps across, lands farther). Our own design."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
h, STEPS = 353.0, 6
RATES = {0.005: BLUE, 0.006: RED}
paths = {eta: [(1 - eta * h) ** k for k in range(STEPS + 1)] for eta in RATES}
assert round(1 - 0.005 * h, 3) == -0.765 and round(1 - 0.006 * h, 3) == -1.118
assert abs(paths[0.005][-1]) < 0.25 and abs(paths[0.006][-1]) > 1.9
xs = np.linspace(-2.2, 2.2, 200)


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                        subplot_titles=[f"learning rate {eta}: each step × {1 - eta * h:.3f}" for eta in RATES])
    for c, (eta, col) in enumerate(RATES.items(), start=1):
        fig.add_trace(go.Scatter(x=xs, y=0.5 * h * xs ** 2, mode="lines", line=dict(color=GREY, width=3)), 1, c)
        p = np.array(paths[eta][:k + 1])
        fig.add_trace(go.Scatter(x=p, y=0.5 * h * p ** 2, mode="lines+markers", line=dict(color=col, width=3),
                                 marker=dict(size=13, color=col)), 1, c)
        fig.add_trace(go.Scatter(x=[0], y=[930], mode="text", text=[f"<b>distance now {p[-1]:+.2f}</b>"],
                                 textfont=dict(size=24, color=col)), 1, c)
        fig.update_xaxes(title_text="distance from the bottom", range=[-2.2, 2.2], row=1, col=c)
        fig.update_yaxes(range=[0, 1000], showticklabels=c == 1, row=1, col=c)
    fig.update_yaxes(title_text="loss", row=1, col=1)
    fig.add_annotation(text=f"step {k}", x=0.5, y=1.2, xref="paper", yref="paper", showarrow=False,
                       font=dict(size=26))
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=110, b=70))
    for a in fig.layout.annotations[:2]:
        a.font = dict(size=22)
    return fig


figs = [frame(k) for k in range(STEPS + 1)]
make_gif(figs, here / "overshoot.gif", fps=2, holds=[2] * STEPS + [6], keys=[1, STEPS], cols=1, width=900)
