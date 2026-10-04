"""The likelihood and the log-likelihood of the five mouse weights (sigma = 2) against the mean: different shapes,
same peak at mu = 32. The log turns the tall narrow bump into a smooth upside-down parabola."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([29, 31, 32, 33, 35.0])
mu = np.linspace(26, 38, 400)
logL = np.array([stats.norm(m, 2).logpdf(X).sum() for m in mu])
assert abs(mu[logL.argmax()] - 32) < 0.05

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("likelihood (product)", "log-likelihood (sum of logs)"))
fig.add_trace(go.Scatter(x=mu, y=np.exp(logL) * 1e5, mode="lines", line=dict(color=GREEN, width=4)), 1, 1)
fig.add_trace(go.Scatter(x=mu, y=logL, mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
for col in (1, 2):
    fig.add_vline(x=32, line=dict(color=RED, dash="dash", width=2), row=1, col=col)
fig.add_annotation(x=32, y=2.75, text="peak at μ = 32", showarrow=False, xanchor="left", xshift=8, row=1, col=1)
fig.add_annotation(x=32, y=-22, text="peak at μ = 32", showarrow=False, xanchor="left", xshift=8, row=1, col=2)
fig.update_xaxes(title_text="mean μ")
fig.update_yaxes(title_text="likelihood (× 10⁻⁵)", range=[0, 2.9], row=1, col=1)
fig.update_yaxes(title_text="log-likelihood", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "log_same_peak.png", scale=2)
fig.write_image(HERE / "log_same_peak.pdf")
