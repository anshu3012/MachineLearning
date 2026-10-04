"""Where the zigzag is, on the valley L = (w1^2 + 100 w2^2)/2 from (-10, 0.4), first 60 steps (Plotly).
Top: w2, the position across the valley. Bottom: w1, the position along it.
Gradient descent at eta = 0.01 (1 - 100 eta = 0: w2 jumps to 0), gradient descent at eta = 0.019
(1 - 100 eta = -0.9: w2 flips sign every step) and momentum, eta = 0.01, beta = 0.9."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, ORANGE, FONT

here = Path(__file__).parent
K, STEPS = 100, 60


def run(eta, beta):
    w, v, P = np.array([-10.0, 0.4]), np.zeros(2), [np.array([-10.0, 0.4])]
    for _ in range(STEPS):
        v = beta * v + eta * np.array([w[0], K * w[1]])     # beta = 0 is plain gradient descent
        w = w - v
        P.append(w.copy())
    return np.array(P)


runs = [("gradient descent, η = 0.01", run(0.01, 0.0), GREEN),
        ("gradient descent, η = 0.019", run(0.019, 0.0), BLUE),
        ("momentum, η = 0.01, β = 0.9", run(0.01, 0.9), ORANGE)]
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
for name, P, c in runs:
    for row, col in ((1, 1), (2, 0)):
        fig.add_trace(go.Scatter(x=list(range(STEPS + 1)), y=P[:, col], name=name, showlegend=row == 1,
                                 mode="lines+markers", line=dict(color=c, width=2), marker=dict(size=4, color=c)),
                      row=row, col=1)
for row in (1, 2):
    fig.add_hline(y=0, line=dict(color="black", width=1, dash="dot"), row=row, col=1)
fig.update_yaxes(title_text="w₂ (across)", row=1, col=1)
fig.update_yaxes(title_text="w₁ (along)", row=2, col=1)
fig.update_xaxes(title_text="step", row=2, col=1)
fig.update_layout(template="simple_white", width=950, height=620, font=FONT,
                  legend=dict(orientation="h", x=0, y=1.1), margin=dict(l=80, r=20, t=60, b=60))
fig.write_image(here / "momentum_zigzag.png", scale=2)
fig.write_image(here / "momentum_zigzag.pdf")
