"""What failed assumptions look like (made-up data, fixed seed): a curve, a funnel, and residuals that follow each other."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
rng = np.random.default_rng(3)
x = np.sort(rng.uniform(0, 10, 120))
curve = 0.3 * (x - 5) ** 2 + rng.normal(0, 1, x.size); curve -= curve.mean()  # residuals of a fit with an intercept average 0
funnel = rng.normal(0, 0.15 + 0.5 * x, x.size)
walk = np.cumsum(rng.normal(0, 1, 120)); walk -= walk.mean()
fig = make_subplots(1, 3, horizontal_spacing=0.07, subplot_titles=(
    "Not linear: curved pattern", "Heteroscedastic: funnel", "Autocorrelated: residuals follow each other"))
fig.add_trace(go.Scatter(x=x, y=curve, mode="markers", marker=dict(size=5, color=RED)), 1, 1)
fig.add_trace(go.Scatter(x=x, y=funnel, mode="markers", marker=dict(size=5, color=RED)), 1, 2)
fig.add_trace(go.Scatter(x=np.arange(120), y=walk, mode="lines+markers", line=dict(color=RED, width=1.5),
                         marker=dict(size=4)), 1, 3)
for c in (1, 2, 3):
    fig.add_trace(go.Scatter(x=[0, 10 if c < 3 else 119], y=[0, 0], mode="lines",
                             line=dict(color=GREY, dash="dash")), 1, c)
fig.update_xaxes(title="predicted value", row=1, col=1); fig.update_xaxes(title="predicted value", row=1, col=2)
fig.update_xaxes(title="row order", row=1, col=3); fig.update_yaxes(title="residual", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=380, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
fig.write_image(here / "violations.png", scale=2)
fig.write_image(here / "violations.pdf")
