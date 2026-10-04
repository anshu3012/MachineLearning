"""Covariance depends on the scale, correlation does not: x with x, x with y, and 2x with 2y."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(42)
x = rng.uniform(0, 120, 40)
y = x + rng.normal(0, 45, 40)
pairs = [("x against x", x, x), ("x against y", x, y), ("2x against 2y", 2 * x, 2 * y)]
titles = [f"{t}<br>cov = {np.cov(a, b)[0, 1]:.0f},  r = {np.corrcoef(a, b)[0, 1]:.2f}" for t, a, b in pairs]
fig = make_subplots(rows=1, cols=3, subplot_titles=titles, horizontal_spacing=0.07)
for i, (_, a, b) in enumerate(pairs, start=1):
    fig.add_scatter(x=a, y=b, mode="markers", marker=dict(size=8, color="#4C78A8"), row=1, col=i)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1400, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=40, r=20, t=90, b=40))
fig.write_image(here / "scale.png", scale=2)
fig.write_image(here / "scale.pdf")
