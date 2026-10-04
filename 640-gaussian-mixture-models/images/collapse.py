"""Maximum likelihood breaks (Plotly), on the seven points with component 1 placed on x = -3, components 2 and 3 fixed
at N(0, 1) and N(4, 1), equal weights (as in the Notebook, Section 5). Left: the mixture density for sigma1 = 0.1:
a tall spike on one point. Right: the log-likelihood against sigma1 (log scale): -17.25, -14.95, -12.65 at 0.1, 0.01,
0.001, rising by log 10 = 2.30 per tenfold shrink without limit."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from common import BLUE, FONT, ORANGE, RED

here = Path(__file__).parent
x = np.array([-3, -2.5, -1, 0, 2, 4, 5.0])


def loglik(s1):
    mu, sd = np.array([-3, 0, 4.0]), np.array([s1, 1, 1])
    return np.log((norm.pdf(x[:, None], mu, sd) / 3).sum(1)).sum()


assert [round(loglik(s), 2) for s in (0.1, 0.01, 0.001)] == [-17.25, -14.95, -12.65]
fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=["mixture with σ₁ = 0.1: a spike on one point",
                                                                   "log-likelihood as σ₁ shrinks"])
fig.update_annotations(font_size=21)
g = np.linspace(-6, 7, 4001)
dens = (norm.pdf(g[:, None], [-3, 0, 4], [0.1, 1, 1]) / 3).sum(1)
fig.add_trace(go.Scatter(x=g, y=dens, mode="lines", line=dict(color=BLUE, width=3)), 1, 1)
fig.add_trace(go.Scatter(x=x, y=np.zeros_like(x), mode="markers", marker=dict(size=11, color="black")), 1, 1)
s = np.logspace(-4, -1, 60)
fig.add_trace(go.Scatter(x=s, y=[loglik(v) for v in s], mode="lines", line=dict(color=RED, width=4)), 1, 2)
for v in (0.1, 0.01, 0.001):
    fig.add_trace(go.Scatter(x=[v], y=[loglik(v)], mode="markers+text", text=[f"{loglik(v):.2f}"], textposition="top right",
                             textfont=dict(size=18, color=ORANGE), marker=dict(size=11, color=ORANGE)), 1, 2)
fig.update_xaxes(title="x", row=1, col=1)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_xaxes(title="σ₁ (log scale)", type="log", exponentformat="power", autorange="reversed", row=1, col=2)
fig.update_yaxes(title="log-likelihood ℓ", row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "collapse.png", scale=2)
