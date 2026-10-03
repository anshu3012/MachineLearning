"""Searching for the standard deviation with the mean fixed at 32: curves with sigma = 1, 2, 4 over the five mouse
weights (left) and the likelihood against sigma (right), highest at sigma = 2."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([29, 31, 32, 33, 35.0])
lik = lambda s: stats.norm(32, s).pdf(X).prod()
s_grid = np.linspace(0.8, 5, 400)
L = np.array([lik(s) for s in s_grid]) * 1e5
assert abs(s_grid[L.argmax()] - 2) < 0.02

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("three widths, mean 32", "likelihood against σ"))
x = np.linspace(22, 42, 400)
for s, c in ((1, RED), (2, GREEN), (4, BLUE)):
    fig.add_trace(go.Scatter(x=x, y=stats.norm(32, s).pdf(x), mode="lines", line=dict(color=c, width=4),
                             name=f"σ = {s}: likelihood {lik(s) * 1e5:.2f} × 10⁻⁵"), 1, 1)
    fig.add_trace(go.Scatter(x=[s], y=[lik(s) * 1e5], mode="markers", marker=dict(size=14, color=c),
                             showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=X, y=np.zeros_like(X), mode="markers", marker=dict(size=13, color="black"),
                         showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=s_grid, y=L, mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, 2)
fig.add_vline(x=2, line=dict(color=GREEN, dash="dash", width=2), row=1, col=2)
fig.update_xaxes(title_text="mouse weight (grams)", row=1, col=1)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_xaxes(title_text="standard deviation σ", row=1, col=2)
fig.update_yaxes(title_text="likelihood (× 10⁻⁵)", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(orientation="h", x=0, y=-0.22), margin=dict(l=70, r=20, t=50, b=150))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "sigma_search.png", scale=2)
fig.write_image(HERE / "sigma_search.pdf")
