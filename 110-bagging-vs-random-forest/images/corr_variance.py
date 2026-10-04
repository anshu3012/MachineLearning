"""Section 3.3 Extra: variance of the average of n trees, rho*sigma^2 + (1 - rho)/n * sigma^2 (ESL eq. 15.1), with
sigma^2 = 1, for tree correlation rho = 0.6 and rho = 0.3. More trees only shrink the second term; the floor rho*sigma^2
stays. Checked by simulating correlated trees. (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
n = np.arange(1, 101)
var = lambda rho, n: rho + (1 - rho) / n
assert round(var(0.6, 100), 3) == 0.604 and round(var(0.3, 100), 3) == 0.307      # the Note's example
# simulation: trees = shared part (variance rho) + own part (variance 1 - rho), so corr = rho and variance 1
rng = np.random.default_rng(0)
for rho in (0.6, 0.3):
    shared = rng.normal(0, np.sqrt(rho), (20000, 1))
    trees = shared + rng.normal(0, np.sqrt(1 - rho), (20000, 100))
    assert abs(trees.mean(1).var() - var(rho, 100)) < 0.02
fig = go.Figure()
for rho, c in [(0.6, "#4C78A8"), (0.3, "#F58518")]:
    fig.add_trace(go.Scatter(x=n, y=var(rho, n), mode="lines", line=dict(color=c, width=4),
                             name=f"trees correlated by ρ = {rho}"))
    fig.add_hline(y=rho, line=dict(color=c, width=2, dash="dash"))
    fig.add_annotation(x=100, y=rho, text=f"floor ρσ² = {rho}: 100 trees give {var(rho, 100):.3f}", xanchor="right",
                       yanchor="bottom", showarrow=False, font=dict(size=20, color=c))
fig.update_xaxes(title="number of trees n", range=[0, 101])
fig.update_yaxes(title="variance of the average (σ² = 1)", range=[0, 1.05])
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=20, b=70), legend=dict(x=0.45, y=0.95))
fig.write_image(HERE / "corr_variance.png", scale=2)
fig.write_image(HERE / "corr_variance.pdf")
