"""Why squares: the absolute distance |d| has a sharp corner at 0, where its slope jumps from -1 to +1; the square d^2
is smooth everywhere, with slope 2d passing through 0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
d = np.linspace(-2, 2, 401)
assert np.isclose(np.gradient(d ** 2, d)[200], 0, atol=0.02)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, subplot_titles=["|d|: a corner at 0, slope jumps −1 → +1",
                                                                            "d²: smooth, slope 2d passes through 0"])
fig.add_scatter(x=d, y=np.abs(d), mode="lines", line=dict(color="#E45756", width=4), row=1, col=1)
fig.add_scatter(x=d, y=d ** 2, mode="lines", line=dict(color="#4C78A8", width=4), row=1, col=2)
fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(size=14, color="black", symbol="circle-open", line=dict(width=3)), row=1, col=1)
for c in (1, 2):
    fig.update_xaxes(title_text="distance d from the mean", row=1, col=c)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1200, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=50, r=20, t=60, b=60))
fig.write_image(here / "square_vs_abs.png", scale=2)
fig.write_image(here / "square_vs_abs.pdf")
