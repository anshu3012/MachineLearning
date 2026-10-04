"""Linearly separable data (a straight line splits the classes) vs data that no straight line can split (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles

here = Path(__file__).parent
rng = np.random.default_rng(3)
n = 40
placed = np.c_[rng.normal(8.0, 0.45, n), rng.normal(118, 6, n)]
not_placed = np.c_[rng.normal(6.0, 0.45, n), rng.normal(92, 6, n)]
Xc, yc = make_circles(n_samples=160, noise=0.06, factor=0.45, random_state=1)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Linearly separable: a straight line works", "Not linearly separable: no straight line works"))
fig.add_trace(go.Scatter(x=placed[:, 0], y=placed[:, 1], mode="markers", marker=dict(color="#54A24B", size=9), name="placed"), 1, 1)
fig.add_trace(go.Scatter(x=not_placed[:, 0], y=not_placed[:, 1], mode="markers", marker=dict(color="#4C78A8", size=9), name="not placed"), 1, 1)
xs = np.array([5.0, 9.0])
fig.add_trace(go.Scatter(x=xs, y=105 - 13 * (xs - 7), mode="lines", line=dict(color="black", width=3), showlegend=False), 1, 1)
for k, c in ((1, "#54A24B"), (0, "#4C78A8")):
    fig.add_trace(go.Scatter(x=Xc[yc == k, 0], y=Xc[yc == k, 1], mode="markers", marker=dict(color=c, size=8), showlegend=False), 1, 2)
fig.update_xaxes(title="CGPA", row=1, col=1); fig.update_yaxes(title="IQ", range=[65, 145], row=1, col=1)
fig.update_xaxes(title="x₁", row=1, col=2); fig.update_yaxes(title="x₂", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "separable.png", scale=2); fig.write_image(here / "separable.pdf")
