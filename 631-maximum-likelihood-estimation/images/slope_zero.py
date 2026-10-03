"""Log-likelihood of the Poisson rate lambda for the call counts 2, 1, 3, 2, 2, with tangent lines at
lambda = 1, 2 and 3.5: the slope is positive before the peak, zero at the peak (lambda = 2) and negative after it."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
C = np.array([2, 1, 3, 2, 2])
lam = np.linspace(0.5, 5, 400)
ll = lambda l: stats.poisson(l).logpmf(C).sum()
slope = lambda l: C.sum() / l - len(C)                     # derivative of the log-likelihood
assert abs(lam[np.argmax([ll(l) for l in lam])] - 2) < 0.02 and slope(2) == 0

fig = go.Figure(go.Scatter(x=lam, y=[ll(l) for l in lam], mode="lines", line=dict(color=BLUE, width=4),
                           name="log-likelihood ℓ(λ)"))
for l0, c, pos in ((1, ORANGE, "bottom right"), (2, GREEN, "top center"), (3.5, RED, "top right")):
    t = np.array([l0 - 0.6, l0 + 0.6])
    fig.add_trace(go.Scatter(x=t, y=ll(l0) + slope(l0) * (t - l0), mode="lines", line=dict(color=c, width=3, dash="dash"),
                             showlegend=False))
    fig.add_trace(go.Scatter(x=[l0], y=[ll(l0)], mode="markers+text", marker=dict(size=13, color=c),
                             text=[f"slope {slope(l0):+.2f}"], textposition=pos, textfont=dict(color=c, size=20),
                             showlegend=False))
fig.update_layout(template="simple_white", width=900, height=520, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="rate λ (calls per minute)", range=[0.5, 5]),
                  yaxis=dict(title="log-likelihood", range=[-13, -5.5]), showlegend=False,
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(HERE / "slope_zero.png", scale=2)
fig.write_image(HERE / "slope_zero.pdf")
