"""Where each Taylor approximation is good (Plotly heatmaps), for f(x, y) = x^3 + xy + y^2 around (1, 1): the size
of the error |f - T1| of the tangent plane (left) and |f - T2| of the second-order polynomial (right), on the same
colour scale. The contour line 0.05 marks the region where the error stays below 0.05; it is much larger for T2."""
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
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["error of the tangent plane |f − T₁|",
                                                                   "error of the second-order polynomial |f − T₂|"])
fig.update_annotations(font_size=21)
for col, e in ((1, e1), (2, e2)):
    fig.add_trace(go.Heatmap(x=g, y=g, z=e, colorscale="Reds", zmin=0, zmax=1, showscale=col == 2,
                             colorbar=dict(title="error")), 1, col)
    fig.add_trace(go.Contour(x=g, y=g, z=e, contours=dict(start=0.05, end=0.05, coloring="lines"),
                             colorscale=[[0, "black"], [1, "black"]], showscale=False, line=dict(width=3)), 1, col)
    fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=12, color="black")), 1, col)
    fig.update_xaxes(title="x", row=1, col=col)
    fig.update_yaxes(title="y" if col == 1 else None, scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
fig.update_layout(template="simple_white", width=1250, height=600, font=FONT, showlegend=False,
                  margin=dict(l=70, r=30, t=60, b=70))
fig.write_image(here / "approx_error.png", scale=2)
