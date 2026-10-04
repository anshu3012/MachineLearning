"""Parametric density estimation: 1000 values, a density histogram, the fitted normal and a badly chosen normal.
Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
rng = np.random.default_rng(42)                     # same draws as the Notebook
sample = rng.normal(50, 5, 1000)
mu, sigma = sample.mean(), sample.std()
assert round(mu, 2) == 49.86 and round(sigma, 2) == 4.94
x = np.linspace(sample.min(), sample.max(), 100)
dens, edges = np.histogram(sample, bins=10, density=True)
fig = go.Figure(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=dens, width=np.diff(edges), name="density histogram",
                       marker=dict(color="#4C78A8", opacity=0.4, line=dict(color="white", width=1))))
fig.add_scatter(x=x, y=stats.norm(mu, sigma).pdf(x), mode="lines", line=dict(color="#F58518", width=4),
                name=f"fitted: μ = {mu:.2f}, σ = {sigma:.2f}")
fig.add_scatter(x=x, y=stats.norm(60, 12).pdf(x), mode="lines", line=dict(color="#E45756", width=4),
                name="badly chosen: μ = 60, σ = 12")
fig.update_layout(template="simple_white", width=950, height=500, bargap=0,
                  font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="1000 values: density histogram and two normal PDFs", x=0.5),
                  xaxis_title="value", yaxis_title="density", legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.7)"),
                  margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "parametric_fit.png", scale=2)
fig.write_image(here / "parametric_fit.pdf")
