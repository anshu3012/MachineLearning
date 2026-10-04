"""Section 6's example: dividing every value by c divides the spread by c and the variance by c^2.
10, 20, ..., 70 (variance 400) become 1, 2, ..., 7 (variance 4). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, BLUE, FONT

here = Path(__file__).parent
x = np.arange(10, 71, 10)
assert x.mean() == 40 and x.var() == 400 and (x / 10).var() == 4
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.32,
                    subplot_titles=("10, 20, ..., 70: mean 40, variance 400", "divided by 10: mean 4, variance 400 / 10² = 4"))
for r, v, col in ((1, x, RED), (2, x / 10, BLUE)):
    fig.add_scatter(x=v, y=[0] * 7, mode="markers+text", text=[f"{t:g}" for t in v], textposition="top center",
                    marker=dict(size=16, color=col), showlegend=False, row=r, col=1)
    fig.add_vline(x=v.mean(), line=dict(color="black", dash="dot", width=2), row=r, col=1)
fig.update_xaxes(range=[0, 75], row=1, col=1)
fig.update_xaxes(range=[0, 7.5], row=2, col=1)
fig.update_yaxes(visible=False, range=[-0.6, 1.2])
fig.update_layout(template="simple_white", width=1000, height=380, font=dict(FONT, size=20), margin=dict(l=30, r=20, t=50, b=40))
fig.write_image(here / "variance_scale.png", scale=2)
fig.write_image(here / "variance_scale.pdf")
