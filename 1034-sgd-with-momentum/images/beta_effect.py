"""Effect of beta on L(w) = w^2/2 from w = -10, learning rate 0.1: the weight over 100 steps (Plotly).
beta = 0 is plain gradient descent; beta = 0.9 overshoots and settles; beta = 1 never settles (no friction)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, GREEN, ORANGE, RED, FONT

here = Path(__file__).parent


def run(beta, eta=0.1, steps=100):
    w, v, P = -10.0, 0.0, [-10.0]
    for _ in range(steps):
        v = beta * v + eta * w                    # gradient of w^2/2 is w
        w = w - v
        P.append(w)
    return P


fig = go.Figure()
for beta, c in ((0.0, BLUE), (0.5, GREEN), (0.9, ORANGE), (1.0, RED)):
    name = f"β = {beta:g}" + (" (plain gradient descent)" if beta == 0 else " (no decay)" if beta == 1 else "")
    fig.add_trace(go.Scatter(x=list(range(101)), y=run(beta), name=name, line=dict(color=c, width=3)))
fig.add_hline(y=0, line=dict(color="black", width=1, dash="dot"))
fig.update_layout(template="simple_white", width=950, height=460, font=FONT,
                  xaxis=dict(title="step"), yaxis=dict(title="weight w (minimum at 0)", range=[-11, 11]),
                  legend=dict(orientation="h", x=0, y=1.16), margin=dict(l=70, r=20, t=70, b=60))
fig.write_image(here / "beta_effect.png", scale=2)
fig.write_image(here / "beta_effect.pdf")
