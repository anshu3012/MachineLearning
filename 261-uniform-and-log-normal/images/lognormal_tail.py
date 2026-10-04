"""The comment-length log-normal, mu = 3, sigma = 1: the area above 100 words (0.054), the median e^3 = 20.1 and the
mean e^3.5 = 33.1, pulled right by the long tail."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
ln = stats.lognorm(s=1, scale=np.exp(3))
assert round(ln.sf(100), 3) == 0.054 and round(ln.median(), 1) == 20.1 and round(ln.mean(), 1) == 33.1
assert round(ln.pdf(20), 4) == 0.0199
x = np.linspace(0.1, 160, 600)
y = ln.pdf(x)
fig = go.Figure()
fig.add_scatter(x=x, y=y, mode="lines", line=dict(color="#4C78A8", width=4))
m = x >= 100
fig.add_scatter(x=np.r_[100, x[m], x[m][-1]], y=np.r_[0, y[m], 0], fill="toself", fillcolor="rgba(228,87,86,0.5)",
                line=dict(width=0), mode="lines")
for v, name, c, yy in ((ln.median(), "median 20.1", "#F58518", 0.031), (ln.mean(), "mean 33.1", "#E45756", 0.025)):
    fig.add_vline(x=v, line=dict(color=c, width=3, dash="dash"))
    fig.add_annotation(x=v, y=yy, text=name, showarrow=False, xanchor="left", xshift=6, font=dict(size=20, color=c))
fig.add_annotation(x=118, y=0.006, text="P(X > 100) = 0.054", showarrow=True, ax=40, ay=-60, font=dict(size=20, color="#E45756"))
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=19),
                  showlegend=False, title=dict(text="Comment lengths, Lognormal(μ = 3, σ = 1)", x=0.5),
                  xaxis=dict(title="comment length (words)", range=[0, 160]), yaxis=dict(title="density", range=[0, 0.034]),
                  margin=dict(l=90, r=30, t=70, b=70))
fig.write_image(here / "lognormal_tail.png", scale=2)
fig.write_image(here / "lognormal_tail.pdf")
