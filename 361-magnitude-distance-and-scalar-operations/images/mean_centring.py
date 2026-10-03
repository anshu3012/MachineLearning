"""Mean centring as a scalar subtraction: 100 random 2D vectors before and after subtracting each column's mean."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(0)
data = rng.multivariate_normal([6, 4], [[2, 1.2], [1.2, 1.5]], size=100)    # 100 example 2D vectors
centred = data - data.mean(axis=0)                                          # x1 - mean(x1), x2 - mean(x2)

fig = make_subplots(1, 2, subplot_titles=["original vectors", "mean-centred vectors"], horizontal_spacing=0.1)
for c, (pts, col) in enumerate([(data, "#4C78A8"), (centred, "#F58518")], start=1):
    fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", marker=dict(size=7, color=col, opacity=0.75),
                             showlegend=False), 1, c)
    m = pts.mean(axis=0)
    fig.add_trace(go.Scatter(x=[m[0]], y=[m[1]], mode="markers", marker=dict(size=14, color="#E45756", symbol="x"),
                             showlegend=False), 1, c)
    fig.update_xaxes(range=[-5, 11], zeroline=True, zerolinecolor="black", zerolinewidth=2, title_text="x1",
                     showgrid=True, gridcolor="#eeeeee", row=1, col=c)
    fig.update_yaxes(range=[-5, 9], zeroline=True, zerolinecolor="black", zerolinewidth=2, title_text="x2",
                     showgrid=True, gridcolor="#eeeeee", scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="Same shape, moved so the mean (red x) sits at the origin", x=0.5),
                  margin=dict(l=40, r=20, t=90, b=40))
fig.write_image(here / "mean_centring.png", scale=2)
fig.write_image(here / "mean_centring.pdf")
print(data.mean(axis=0).round(2), centred.mean(axis=0).round(10))
