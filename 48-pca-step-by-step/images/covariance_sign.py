"""Same variances, opposite covariance: variance alone cannot tell these two datasets apart (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
sets = {"Data A": np.array([[-1, -1], [0, 0], [1, 1]]), "Data B": np.array([[-1, 1], [0, 0], [1, -1]])}
cov = lambda d: float(np.mean((d[:, 0] - d[:, 0].mean()) * (d[:, 1] - d[:, 1].mean())))
titles = [f"{k}: var(x) = {d[:, 0].var():.2f}, var(y) = {d[:, 1].var():.2f}<br><b>cov(x, y) = {cov(d):+.2f}</b>"
          for k, d in sets.items()]
fig = make_subplots(1, 2, subplot_titles=titles, horizontal_spacing=0.12)
for c, (k, d) in enumerate(sets.items(), start=1):
    colour = BLUE if cov(d) > 0 else RED
    fig.add_trace(go.Scatter(x=d[:, 0], y=d[:, 1], mode="markers+text", marker=dict(size=18, color=colour),
                             text=[f"({x}, {y})" for x, y in d], textposition="top left", textfont=dict(size=16)), 1, c)
    fig.update_xaxes(range=[-1.8, 1.8], zeroline=True, zerolinecolor="#BBBBBB", title="x", row=1, col=c)
    fig.update_yaxes(range=[-1.8, 1.8], zeroline=True, zerolinecolor="#BBBBBB", title="y",
                     scaleanchor=f"x{'' if c == 1 else 2}", row=1, col=c)
fig.add_annotation(x=0.2, y=-1.45, xref="x", yref="y", text="x up, y up", showarrow=False, font=dict(color=BLUE, size=17))
fig.add_annotation(x=0.2, y=-1.45, xref="x2", yref="y2", text="x up, y down", showarrow=False, font=dict(color=RED, size=17))
fig.update_layout(template="simple_white", width=950, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=90, b=50))
fig.update_annotations(font_size=17, selector=dict(xref="paper"))
fig.write_image(here / "covariance_sign.png", scale=2)
fig.write_image(here / "covariance_sign.pdf")
