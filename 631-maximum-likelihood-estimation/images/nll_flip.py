"""The minus sign flips the hill into a valley (Plotly). The log-likelihood of the five mice against mu (sigma = 2) and
its negative, the NLL. NLL(30) = 13.06, NLL(32) = 10.56, NLL(34) = 13.06: the lowest NLL is at the highest
log-likelihood, mu = 32."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([29, 31, 32, 33, 35.0])
ll = lambda m: stats.norm(m, 2).logpdf(X).sum()
assert np.allclose([-ll(30), -ll(32), -ll(34)], [13.06, 10.56, 13.06], atol=0.005)
mu = np.linspace(28.5, 35.5, 300)
L = np.array([ll(m) for m in mu])

fig = go.Figure()
fig.add_hline(y=0, line=dict(color="black", width=1.5))
fig.add_trace(go.Scatter(x=mu, y=L, mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                         name="log-likelihood ℓ(μ): a hill"))
fig.add_trace(go.Scatter(x=mu, y=-L, mode="lines", line=dict(color=BLUE, width=4), name="NLL(μ) = −ℓ(μ): a valley"))
for m in (30, 32, 34):
    fig.add_trace(go.Scatter(x=[m, m], y=[ll(m), -ll(m)], mode="lines", line=dict(color=GREY, width=1, dash="dot"),
                             showlegend=False))
    col = GREEN if m == 32 else ORANGE
    fig.add_trace(go.Scatter(x=[m, m], y=[ll(m), -ll(m)], mode="markers+text", marker=dict(size=13, color=col),
                             text=[f"{ll(m):.2f}".replace("-", "−"), f"{-ll(m):.2f}"],
                             textposition=["bottom center", "top center"], textfont=dict(size=19, color=col),
                             showlegend=False))
fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="mean μ (σ = 2)"), yaxis=dict(title="value", range=[-20, 20]),
                  legend=dict(orientation="h", x=0, y=1.1), margin=dict(l=70, r=20, t=70, b=60))
fig.write_image(HERE / "nll_flip.png", scale=2)
fig.write_image(HERE / "nll_flip.pdf")
