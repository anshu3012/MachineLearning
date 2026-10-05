"""Where each Taylor approximation is good (Plotly heatmaps), for f(x, y) = x^3 + xy + y^2 around (1, 1): the size
of the error |f - T1| of the tangent plane (left) and |f - T2| of the second-order polynomial (right), on the same
colour scale. Top row: each error drawn as a surface; bottom row: the same seen from above as a heat map.\nThe contour line 0.05 marks the region where the error stays below 0.05; it is much larger for T2."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT

here = Path(__file__).parent
f = lambda x, y: x ** 3 + x * y + y ** 2
T1 = lambda x, y: 3 + 4 * (x - 1) + 3 * (y - 1)
T2 = lambda x, y: T1(x, y) + 3 * (x - 1) ** 2 + (x - 1) * (y - 1) + (y - 1) ** 2
assert abs(T1(1.1, 0.9) - 3.1) < 1e-12 and abs(T2(1.1, 0.9) - 3.13) < 1e-12 and abs(f(1.1, 0.9) - 3.131) < 1e-12
g = np.linspace(0.4, 1.6, 241)
X, Y = np.meshgrid(g, g)
e1, e2 = np.abs(f(X, Y) - T1(X, Y)), np.abs(f(X, Y) - T2(X, Y))
area = lambda e: (e < 0.05).mean()
assert 9 <= area(e2) / area(e1) < 10, (area(e1), area(e2))
fig = make_subplots(2, 2, horizontal_spacing=0.08, vertical_spacing=0.08, row_heights=[0.45, 0.55],
                    specs=[[{"type": "scene"}, {"type": "scene"}], [{"type": "xy"}, {"type": "xy"}]],
                    subplot_titles=["error of the tangent plane |f − T₁|", "error of the second-order polynomial |f − T₂|",
                                    "seen from above", "seen from above"])
# top row: each error as a surface (height = error), same colours; the black ring is the 0.05 line of the map below
sg = np.linspace(0.4, 1.6, 161)
SX, SY = np.meshgrid(sg, sg)
for col, T in ((1, T1), (2, T2)):
    es = np.abs(f(SX, SY) - T(SX, SY))
    fig.add_trace(go.Surface(x=sg, y=sg, z=np.where(es <= 1.2, es, np.nan), colorscale="Reds", cmin=0, cmax=1,
                             showscale=False, lighting=dict(ambient=0.9, diffuse=0.3, specular=0.05),
                             contours_z=dict(show=True, start=0.05, end=0.05, size=1, color="black", width=4)),
                  1, col)
    fig.add_trace(go.Scatter3d(x=[1], y=[1], z=[0], mode="markers", marker=dict(size=5, color="black")), 1, col)
fig.update_scenes(xaxis=dict(title="x", tickvals=[0.5, 1, 1.5], tickfont=dict(size=13)),
                  yaxis=dict(title="y", tickvals=[0.5, 1, 1.5], tickfont=dict(size=13)),
                  zaxis=dict(title="error", range=[0, 1.2], tickvals=[0, 0.5, 1], tickfont=dict(size=13)),
                  aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.6), camera=dict(eye=dict(x=1.4, y=-1.4, z=0.9)))
fig.update_annotations(font_size=21)
for col, e in ((1, e1), (2, e2)):
    fig.add_trace(go.Heatmap(x=g, y=g, z=e, colorscale="Reds", zmin=0, zmax=1, showscale=col == 2,
                             colorbar=dict(title="error", len=0.5, y=0.27)), 2, col)
    fig.add_trace(go.Contour(x=g, y=g, z=e, contours=dict(start=0.05, end=0.05, coloring="lines"),
                             colorscale=[[0, "black"], [1, "black"]], showscale=False, line=dict(width=3)), 2, col)
    fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=12, color="black")), 2, col)
    fig.update_xaxes(title="x", row=2, col=col)
    fig.update_yaxes(title="y" if col == 1 else None, scaleanchor=f"x{col if col > 1 else ''}", row=2, col=col)
fig.update_layout(template="simple_white", width=1250, height=1150, font=FONT, showlegend=False,
                  margin=dict(l=70, r=30, t=60, b=70))
fig.write_image(here / "approx_error.png", scale=2)
