"""Log-likelihood of a normal distribution for the five mouse weights 29, 31, 32, 33, 35 as a contour map over
(mu, sigma). The single peak is at (32, 2): the mean and the standard deviation (dividing by n) of the data.
Dashed lines: the two one-parameter searches of the maximum likelihood Note."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([29, 31, 32, 33, 35.0])
mu = np.linspace(28, 36, 201)
sg = np.linspace(0.8, 5, 211)
M, S = np.meshgrid(mu, sg)
LL = stats.norm(M[..., None], S[..., None]).logpdf(X).sum(axis=-1)
i, j = np.unravel_index(LL.argmax(), LL.shape)
assert abs(M[i, j] - 32) < 0.05 and abs(S[i, j] - 2) < 0.03

fig = go.Figure(go.Contour(x=mu, y=sg, z=LL, colorscale="Blues", contours=dict(start=-22, end=-10.75, size=0.75),
                           line=dict(width=0.8), colorbar=dict(title=dict(text="log-likelihood", side="right"))))
fig.add_trace(go.Scatter(x=[28, 36], y=[2, 2], mode="lines", line=dict(color=ORANGE, dash="dash", width=3),
                         name="σ fixed at 2, μ varies"))
fig.add_trace(go.Scatter(x=[32, 32], y=[0.8, 5], mode="lines", line=dict(color=GREEN, dash="dash", width=3),
                         name="μ fixed at 32, σ varies"))
fig.add_trace(go.Scatter(x=[32], y=[2], mode="markers", marker=dict(symbol="star", size=20, color=RED),
                         showlegend=False))
fig.add_annotation(x=32, y=2, text="peak (32, 2): ℓ = −10.56", showarrow=True, ax=120, ay=-60, bgcolor="white",
                   font=dict(size=20))
fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="mean μ"), yaxis=dict(title="standard deviation σ"),
                  legend=dict(orientation="h", x=0, y=1.1), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(HERE / "normal_surface.png", scale=2)
fig.write_image(HERE / "normal_surface.pdf")
