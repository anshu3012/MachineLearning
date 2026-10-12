"""The search for the best weight k. Step 1's numbers: prediction 0.5 m with variance
1.01 m², reading 0.82 m with variance 0.16 m². The weight k on the reading slides from 0 to 1. Top: the blended
Gaussian, mean k z + (1 - k) x_pred and variance V(k) = k² R + (1 - k)² p_pred, moves from the prediction to the
reading. Bottom: a dot traces V(k). The last frame returns to the lowest point, k = 0.863, variance 0.138, where the
blend is narrowest. Run: python var_weight_anim.py -> var_weight_anim.gif, var_weight_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE, PURPLE, RED, make_gif
from kfsim import normal

here = Path(__file__).parent
xb, pb, z, r = 0.5, 1.01, 0.82, 0.16
g = np.linspace(-2.5, 3.5, 600)
kk = np.linspace(0, 1, 401)


def V(k):
    return k ** 2 * r + (1 - k) ** 2 * pb


kb = pb / (pb + r)
assert abs(kb - 0.863) < 5e-4 and abs(V(kb) - 0.138) < 5e-4 and abs(V(0) - 1.01) < 1e-9 and abs(V(1) - 0.16) < 1e-9
assert np.argmin(V(kk)) == np.argmin(np.abs(kk - kb))           # the lowest point of the curve is k = 0.863


def frame(k, last=False):
    m, v = k * z + (1 - k) * xb, V(k)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.5, 0.5], vertical_spacing=0.13)
    fig.add_trace(go.Scatter(x=g, y=normal(g, xb, pb), line=dict(color=BLUE, width=4),
                             name="prediction: mean 0.5, variance 1.01"), 1, 1)
    fig.add_trace(go.Scatter(x=g, y=normal(g, z, r), line=dict(color=ORANGE, width=4, dash="dash"),
                             name="reading: 0.82, variance 0.16"), 1, 1)
    fig.add_trace(go.Scatter(x=g, y=normal(g, m, v), line=dict(color=PURPLE, width=5),
                             name=f"blend: mean {m:.3f}, variance {v:.3f}"), 1, 1)
    ks = kk if last else kk[kk <= k + 1e-9]
    fig.add_trace(go.Scatter(x=ks, y=V(ks), mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[k], y=[v], mode="markers", marker=dict(color=RED if last else PURPLE, size=18),
                             showlegend=False), 2, 1)
    fig.add_annotation(x=0, y=pb, text="k = 0: keep the prediction, V = 1.01", showarrow=False, xanchor="left",
                       yanchor="bottom", xshift=16, font=dict(size=18), row=2, col=1)
    if last or k >= 1:
        fig.add_annotation(x=1, y=r, text="k = 1: take the reading, V = 0.16", showarrow=False, xanchor="right",
                           yanchor="top", yshift=-14, font=dict(size=18), row=2, col=1)
    if last:
        fig.add_annotation(x=kb, y=V(kb), text=f"lowest: k = {kb:.3f}, V = {V(kb):.3f}", ax=-160, ay=-110,
                           arrowcolor=RED, font=dict(size=19, color=RED), row=2, col=1)
    title = (f"k = {kb:.3f}: the narrowest blend, variance {V(kb):.3f}" if last
             else f"weight on the reading k = {k:.1f}")
    fig.update_xaxes(title="position (m)", range=[-2.5, 3.5], row=1, col=1)
    fig.update_yaxes(title="density", range=[0, 1.25], row=1, col=1)
    fig.update_xaxes(title="weight k given to the reading", range=[-0.03, 1.03], row=2, col=1)
    fig.update_yaxes(title="variance of the blend V(k) (m²)", range=[0, 1.2], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, margin=dict(l=90, r=30, t=170, b=70),
                      legend=dict(x=0.01, y=1.0, yanchor="bottom", font=dict(size=17)),
                      title=dict(x=0.5, y=0.975, text=title))
    return fig


ks = np.round(np.arange(0, 1.01, 0.1), 1)
figs = [frame(k) for k in ks] + [frame(kb, last=True)]
make_gif(figs, here / "var_weight_anim", fps=1, holds=[3] + [1] * 9 + [2, 10], keys=[0, 5, 10, 11], cols=2,
         width=850)
