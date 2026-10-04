"""The likelihood of a dataset is the product of the heights (Plotly). Same five mice, two curves with sigma = 2.
Left: mean 28; heights 0.176, 0.065, 0.027, 0.009, 0.0004 multiply to 1.18e-9 (the 35-gram mouse is in the tail).
Right: mean 32; the product is 2.59e-5, about 20,000 times larger."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([29, 31, 32, 33, 35.0])
h28, h32 = stats.norm(28, 2).pdf(X), stats.norm(32, 2).pdf(X)
assert np.allclose(h28, [0.176, 0.065, 0.027, 0.009, 0.0004], atol=6e-4)
assert abs(h28.prod() / 1e-9 - 1.18) < 0.01 and abs(h32.prod() / 1e-5 - 2.59) < 0.01

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=(f"mean 28: L = 1.18 × 10⁻⁹", f"mean 32: L = 2.59 × 10⁻⁵"))
x = np.linspace(21, 39, 400)
for c, (mu, h, col) in enumerate(((28, h28, RED), (32, h32, GREEN)), start=1):
    fig.add_trace(go.Scatter(x=x, y=stats.norm(mu, 2).pdf(x), mode="lines", line=dict(color=GREY, width=3)), 1, c)
    for xi, hi in zip(X, h):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[0, hi], mode="lines", line=dict(color=col, width=6)), 1, c)
    fig.add_trace(go.Scatter(x=X, y=h, mode="markers+text", marker=dict(size=10, color=col),
                             text=[f"{v:.4f}".rstrip("0") if v < 0.001 else f"{v:.3f}" for v in h],
                             textposition="top right" if c == 1 else "top center", textfont=dict(size=17, color=col)), 1, c)
    fig.add_trace(go.Scatter(x=X, y=np.zeros(5), mode="markers", marker=dict(size=12, color="black")), 1, c)
fig.add_annotation(x=35, y=0.03, ax=36.5, ay=0.11, xref="x1", yref="y1", axref="x1", ayref="y1", showarrow=True,
                   arrowhead=2, arrowwidth=2, arrowcolor=RED, text="35 g: in the tail", font=dict(size=18, color=RED))
fig.update_xaxes(title_text="mouse weight (grams)")
fig.update_yaxes(title_text="height of the curve", range=[0, 0.245], row=1, col=1)
fig.update_yaxes(range=[0, 0.245], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "heights_product.png", scale=2)
fig.write_image(HERE / "heights_product.pdf")
