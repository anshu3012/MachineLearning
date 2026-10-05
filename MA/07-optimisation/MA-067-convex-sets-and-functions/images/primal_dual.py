"""The convex problem of the Lagrange multipliers Note (Plotly). Left: the surface of f = x^2 + 2y^2 (a bowl) with the
feasible line lifted onto it; middle: contours of x^2 + 2y^2 and the feasible half-plane
x + y >= 3; the lowest feasible point is (2, 1) with value 6. Right: the dual function D(lambda) = 3 lambda - 3 lambda^2/8
peaks at lambda = 4 with D(4) = 6, the same height: strong duality.
Middle (same colours and star as the surface): contour map; right: the dual."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import optimize

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda x, y: x ** 2 + 2 * y ** 2
D = lambda l: 3 * l - 3 * l ** 2 / 8
res = optimize.minimize(lambda p: f(*p), [3, 3], constraints=[{"type": "ineq", "fun": lambda p: p[0] + p[1] - 3}])
assert np.allclose(res.x, [2, 1], atol=1e-4) and abs(res.fun - 6) < 1e-6 and D(4) == 6
lam = np.linspace(0, 8, 400)
assert abs(lam[D(lam).argmax()] - 4) < 0.02

fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.09, column_widths=[0.3, 0.37, 0.33],
                    specs=[[{"type": "scene"}, {"type": "xy"}, {"type": "xy"}]],
                    subplot_titles=("the surface of x² + 2y²", "from above: x + y ≥ 3 (green)", "dual: max D(λ)"))
gs = np.linspace(-1, 4, 60)
XS, YS = np.meshgrid(gs, gs)
fig.add_trace(go.Surface(x=gs, y=gs, z=f(XS, YS), colorscale="Blues", reversescale=True, cmin=0, cmax=40, showscale=False,
                         contours=dict(z=dict(show=True, usecolormap=False, color="#2F4B7C", width=2, start=2.5, end=37.5, size=2.5,
                                              project=dict(z=True))), lighting=dict(ambient=1, diffuse=0.1, specular=0)), 1, 1)
tt = np.linspace(0.3, 3.7, 60)
fig.add_trace(go.Scatter3d(x=tt, y=3 - tt, z=f(tt, 3 - tt) + 0.3, mode="lines", line=dict(color=GREEN, width=8)), 1, 1)
fig.add_trace(go.Scatter3d(x=[2], y=[1], z=[6.5], mode="markers", marker=dict(size=7, color=RED)), 1, 1)
fig.update_layout(scene=dict(xaxis=dict(title="x", showbackground=False, tickfont=dict(size=12)),
                             yaxis=dict(title="y", showbackground=False, tickfont=dict(size=12)),
                             zaxis=dict(title="f", range=[0, 40], showbackground=False, tickfont=dict(size=12)),
                             camera=dict(eye=dict(x=-1.3, y=-1.6, z=1.0), projection=dict(type="orthographic")),
                             aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.7)))
g = np.linspace(-1, 4, 200)
X, Y = np.meshgrid(g, g)
fig.add_trace(go.Contour(x=g, y=g, z=f(X, Y), showscale=False, colorscale="Blues", reversescale=True, zmin=0, zmax=40,
                         contours=dict(start=2.5, end=37.5, size=2.5), line=dict(width=1, color="#2F4B7C")), 1, 2)
fig.add_trace(go.Scatter(x=[3 - 4, 4, 4, -1], y=[4, -1, 4, 4], fill="toself", mode="none",
                         fillcolor="rgba(84,162,75,0.18)"), 1, 2)
fig.add_trace(go.Scatter(x=[-1, 4], y=[4, -1], mode="lines", line=dict(color=GREEN, width=3)), 1, 2)
fig.add_trace(go.Contour(x=g, y=g, z=f(X, Y), showscale=False, contours=dict(start=6, end=6, size=1, coloring="none"),
                         line=dict(color=BLUE, width=3, dash="dash")), 1, 2)
fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers+text", text=["(2, 1): value 6"], textposition="middle right",
                         textfont=dict(size=21, color=RED), marker=dict(symbol="star", size=20, color=RED)), 1, 2)
fig.add_annotation(x=3.1, y=3.4, text="feasible", showarrow=False, font=dict(color=GREEN, size=20), row=1, col=2)
fig.add_trace(go.Scatter(x=lam, y=D(lam), mode="lines", line=dict(color=ORANGE, width=4)), 1, 3)
fig.add_trace(go.Scatter(x=[0, 8], y=[6, 6], mode="lines", line=dict(color=RED, width=2, dash="dash")), 1, 3)
fig.add_trace(go.Scatter(x=[4], y=[6], mode="markers", marker=dict(symbol="star", size=20, color=RED)), 1, 3)
fig.add_annotation(x=4, y=6, text="D(4) = 6 = primal minimum", yshift=22, showarrow=False, font=dict(color=RED, size=19),
                   row=1, col=3)
fig.update_xaxes(title_text="x", range=[-1, 4], row=1, col=2)
fig.update_yaxes(title_text="y", range=[-1, 4], scaleanchor="x", row=1, col=2)
fig.update_xaxes(title_text="λ", row=1, col=3)
fig.update_yaxes(title_text="D(λ)", range=[0, 7.5], row=1, col=3)
fig.update_layout(template="simple_white", width=1500, height=540, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "primal_dual.png", scale=2)
fig.write_image(HERE / "primal_dual.pdf")
