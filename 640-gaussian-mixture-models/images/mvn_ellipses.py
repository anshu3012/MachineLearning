"""Two-dimensional normal components (Plotly contours). Left: the Note's example, mean (0, 0), variances 1 and 4, no
covariance: contour ellipses along the axes, density 0.0293 at (1, 2). Right: the same variances with covariance
1.6: the ellipses tilt."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import multivariate_normal as mvn
from common import FONT, ORANGE

here = Path(__file__).parent
S1, S2 = np.array([[1, 0], [0, 4.0]]), np.array([[1, 1.6], [1.6, 4.0]])
assert round(mvn([0, 0], S1).pdf([1, 2]), 4) == 0.0293
g = np.linspace(-5, 5, 201)
X, Y = np.meshgrid(g, g)
P = np.dstack([X, Y])
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=["variances 1 and 4, covariance 0", "variances 1 and 4, covariance 1.6"])
fig.update_annotations(font_size=21)
for col, S in ((1, S1), (2, S2)):
    fig.add_trace(go.Contour(x=g, y=g, z=mvn([0, 0], S).pdf(P), colorscale="Blues", showscale=False,
                             contours=dict(coloring="lines", start=0.005, end=0.07, size=0.01), line=dict(width=3)), 1, col)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=12, color="black")), 1, col)
    fig.update_xaxes(title="feature 1", range=[-5, 5], row=1, col=col)
    fig.update_yaxes(title="feature 2" if col == 1 else None, range=[-5, 5], scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
fig.add_trace(go.Scatter(x=[1], y=[2], mode="markers+text", text=["(1, 2): density 0.0293"], textposition="middle right",
                         textfont=dict(size=18, color=ORANGE), marker=dict(size=13, color=ORANGE)), 1, 1)
fig.update_layout(template="simple_white", width=1150, height=600, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "mvn_ellipses.png", scale=2)
