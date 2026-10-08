"""Binary Bayes filter on a door that nobody touches, in log odds. Start l = 0 (p = 0.5). Each 'sense open' adds
ln 3 = 1.10, each 'sense closed' adds ln(1/2) = -0.69. Readings: open, open, closed, open, open ->
l = 1.10, 2.20, 1.50, 2.60, 3.70 -> p = 0.75, 0.90, 0.82, 0.93, 0.976.
Run: python binary_door.py -> binary_door.gif, binary_door_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, RED, make_gif

here = Path(__file__).parent
READ = ["open", "open", "closed", "open", "open"]
STEP = {"open": np.log(3), "closed": np.log(0.5)}
ls = np.concatenate([[0], np.cumsum([STEP[z] for z in READ])])
ps = 1 - 1 / (1 + np.exp(ls))
assert abs(ps[-1] - 0.9759) < 1e-4


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=["log odds: add one block per reading", "probability that the door is open"])
    base = 0.0
    for i in range(k):                                # one block per reading, stacked from 0
        d = STEP[READ[i]]
        fig.add_bar(x=[i + 1], y=[d], base=[base], marker_color=GREEN if d > 0 else RED, width=0.6, row=1, col=1,
                    text=[f"{d:+.2f}"], textposition="inside", insidetextanchor="middle", textfont=dict(size=16, color="white"))
        base += d
    fig.add_scatter(x=list(range(k + 1)), y=ls[:k + 1], mode="markers", marker=dict(size=12, color=BLUE), row=1, col=1)
    for i in range(k + 1):
        fig.add_annotation(x=i + 0.33, y=ls[i], text=f"<b>{ls[i]:.2f}</b>", showarrow=False, xanchor="left",
                           font=dict(size=16, color=BLUE), row=1, col=1)
    fig.add_scatter(x=list(range(k + 1)), y=ps[:k + 1], mode="lines+markers+text", line=dict(color=BLUE, width=3),
                    marker=dict(size=11), text=[f"{v:.3f}" for v in ps[:k + 1]], textposition="bottom right",
                    textfont=dict(size=16), row=1, col=2)
    ticks = ["start"] + [f"{i + 1}: {z}" for i, z in enumerate(READ)]
    for c in (1, 2):
        fig.update_xaxes(tickvals=list(range(6)), ticktext=ticks, range=[-0.5, 5.6], row=1, col=c, tickangle=-30)
    fig.update_yaxes(title="log odds l", range=[-1, 4.3], row=1, col=1)
    fig.update_yaxes(title="p(open)", range=[0.4, 1.02], row=1, col=2)
    fig.update_layout(template="simple_white", width=1300, height=540, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=70, b=90))
    fig.update_annotations(font_size=21)
    return fig


figs = [frame(k) for k in range(6)]
make_gif(figs, here / "binary_door", fps=2, holds=[3, 3, 3, 3, 3, 8], keys=[2, 5], cols=1, width=950)
