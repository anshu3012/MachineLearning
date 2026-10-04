"""Momentum and NAG on L(w) = w^2/2 from w = -10, learning rate 0.1, beta = 0.9: the weight over 60 steps (left),
and on L(w) = (w^2 - 4)^2/8 - 0.6 w from w = -3, learning rate 0.05, beta = 0.9 (right) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import ORANGE, PURPLE, GREY, FONT

here = Path(__file__).parent


def run(grad, w0, eta, beta, nag, steps):
    w, v, P = w0, 0.0, [w0]
    for _ in range(steps):
        g = grad(w - beta * v) if nag else grad(w)
        v = beta * v + eta * g
        w = w - v
        P.append(w)
    return P


fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.11,
                    subplot_titles=("bowl L = w²/2: overshooting", "curve with a local minimum"))
df = lambda w: w * (w ** 2 - 4) / 2 - 0.6
for nag, name, c in ((False, "momentum", ORANGE), (True, "NAG", PURPLE)):
    fig.add_trace(go.Scatter(y=run(lambda w: w, -10.0, 0.1, 0.9, nag, 60), name=name, line=dict(color=c, width=3)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=run(df, -3.0, 0.05, 0.9, nag, 120), showlegend=False, line=dict(color=c, width=3)),
                  row=1, col=2)
fig.add_hline(y=0, line=dict(color=GREY, dash="dot", width=1.5), row=1, col=1)
for y, text in ((-1.83, "local minimum"), (2.14, "global minimum")):
    fig.add_hline(y=y, line=dict(color=GREY, dash="dot", width=1.5), row=1, col=2)
    fig.add_annotation(x=118, y=y, yshift=12, xanchor="right", text=text, showarrow=False, font=dict(color=GREY),
                       row=1, col=2)
fig.update_xaxes(title_text="step")
fig.update_yaxes(title_text="weight w", col=1)
fig.update_layout(template="simple_white", width=1050, height=430, font=FONT,
                  legend=dict(x=0.3, y=0.05, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=70, r=20, t=40, b=60))
fig.write_image(here / "overshoot.png", scale=2)
fig.write_image(here / "overshoot.pdf")
