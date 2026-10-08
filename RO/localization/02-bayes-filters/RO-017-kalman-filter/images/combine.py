"""Multiplying the prediction curve by the reading curve gives the updated belief. Prediction N(0.5, 1.01) and
reading 0.82 from the first step; the reading's variance R runs from 4 down to 0.01. A vague reading barely moves
the prediction (small gain K); a sharp one pulls the estimate onto it (K near 1). Frame R = 0.16 is the real beacon.
Run: python combine.py -> combine.gif, combine_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, PURPLE, make_gif
from kfsim import normal

here = Path(__file__).parent
xb, pb, z = 0.5, 1.01, 0.82
g = np.linspace(-2.5, 3.5, 600)
Rs = [4.0, 1.0, 0.4, 0.16, 0.04, 0.01]


def frame(r):
    k = pb / (pb + r)
    m, v = xb + k * (z - xb), (1 - k) * pb
    prod = normal(g, xb, pb) * normal(g, z, r)
    assert np.allclose(prod / np.trapezoid(prod, g), normal(g, m, v), atol=1e-3)   # product = normal(m, v)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=g, y=normal(g, xb, pb), line=dict(color=BLUE, width=4), name="prediction: mean 0.5, variance 1.01"))
    fig.add_trace(go.Scatter(x=g, y=normal(g, z, r), line=dict(color=ORANGE, width=4, dash="dash"),
                             name=f"reading: 0.82, variance R = {r}"))
    fig.add_trace(go.Scatter(x=g, y=normal(g, m, v), line=dict(color=PURPLE, width=5),
                             name=f"product (updated belief): mean {m:.3f}, variance {v:.3f}"))
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=600, margin=dict(l=80, r=30, t=150, b=70),
                      legend=dict(x=0.01, y=0.99, font=dict(size=17)),
                      title=dict(x=0.5, y=0.96, text=f"R = {r}:  gain K = 1.01 / (1.01 + {r}) = {k:.3f}"
                                 + ("  (the real beacon)" if r == 0.16 else "")),
                      xaxis=dict(title="position (m)", range=[-2.5, 3.5]), yaxis=dict(title="density", range=[0, 4.3]))
    return fig


figs = [frame(r) for r in Rs]
make_gif(figs, here / "combine", fps=1, holds=[2, 2, 2, 4, 2, 4], keys=[0, 3, 5], cols=1, width=850)
