"""Two-dimensional normal components (Plotly: the density surfaces on top, the same surfaces seen from above as contour
maps below, same colours and same marked point). Left: the Note's example, mean (0, 0), variances 1 and 4, no
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
fig = make_subplots(2, 2, horizontal_spacing=0.1, vertical_spacing=0.06,
                    specs=[[{"type": "scene"}, {"type": "scene"}], [{"type": "xy"}, {"type": "xy"}]],
                    subplot_titles=["the surface: variances 1 and 4, covariance 0", "the surface: covariance 1.6",
                                    "from above: ellipses along the axes", "from above: tilted ellipses"])
fig.update_annotations(font_size=21)
gs = g[::4]
Xs, Ys = np.meshgrid(gs, gs)
Ps = np.dstack([Xs, Ys])
LV = dict(show=True, usecolormap=False, color="#2F4B7C", width=3, start=0.01, end=0.13, size=0.02, project=dict(z=True))
for col, S in ((1, S1), (2, S2)):
    fig.add_trace(go.Surface(x=gs, y=gs, z=mvn([0, 0], S).pdf(Ps), colorscale="Blues", cmin=0, cmax=0.14, showscale=False,
                             contours=dict(z=LV), lighting=dict(ambient=1, diffuse=0.1, specular=0)), 1, col)
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[mvn([0, 0], S).pdf([0, 0]) + 0.003], mode="markers", marker=dict(size=5, color="black")), 1, col)
    fig.add_trace(go.Contour(x=g, y=g, z=mvn([0, 0], S).pdf(P), colorscale="Blues", zmin=0, zmax=0.14, showscale=False,
                             contours=dict(coloring="lines", start=0.01, end=0.13, size=0.02), line=dict(width=3)), 2, col)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=12, color="black")), 2, col)
    fig.update_xaxes(title="feature 1", range=[-5, 5], row=2, col=col)
    fig.update_yaxes(title="feature 2" if col == 1 else None, range=[-5, 5], scaleanchor=f"x{col if col > 1 else ''}", row=2, col=col)
fig.add_trace(go.Scatter3d(x=[1], y=[2], z=[0.0293 + 0.003], mode="markers", marker=dict(size=5, color=ORANGE)), 1, 1)
fig.add_trace(go.Scatter(x=[1], y=[2], mode="markers+text", text=["(1, 2): density 0.0293"], textposition="middle right",
                         textfont=dict(size=18, color=ORANGE), marker=dict(size=13, color=ORANGE)), 2, 1)
cam = dict(eye=dict(x=-1.3, y=-1.6, z=0.9), projection=dict(type="orthographic"))
for sc in ("scene", "scene2"):
    fig.update_layout({sc: dict(xaxis=dict(title="feature 1", range=[-5, 5], showbackground=False, tickfont=dict(size=13)),
                                yaxis=dict(title="feature 2", range=[-5, 5], showbackground=False, tickfont=dict(size=13)),
                                zaxis=dict(title="density", range=[0, 0.14], showbackground=False, tickfont=dict(size=13)),
                                camera=cam, aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.6))})
fig.update_layout(template="simple_white", width=1150, height=1100, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "mvn_ellipses.png", scale=2)
