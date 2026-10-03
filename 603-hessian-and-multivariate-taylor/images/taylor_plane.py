"""f(x, y) = x^3 + x y + y^2 (blue) and its Taylor approximations at (1, 1) (Plotly 3D).
Left: first order, the tangent plane 3 + 4(x-1) + 3(y-1). Right: second order, adding (1/2) d^T H d with
H = [[6, 1], [1, 2]]: a curved surface that hugs f over a wider area."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda x, y: x ** 3 + x * y + y ** 2
T1 = lambda x, y: 3 + 4 * (x - 1) + 3 * (y - 1)
T2 = lambda x, y: T1(x, y) + 3 * (x - 1) ** 2 + (x - 1) * (y - 1) + (y - 1) ** 2
assert abs(T2(1.1, 0.9) - 3.13) < 1e-12
g = np.linspace(0, 2, 40)
X, Y = np.meshgrid(g, g)
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "scene"}]], horizontal_spacing=0.0,
                    subplot_titles=("first order: tangent plane", "second order: adds the Hessian term"))
for col, T, c in ((1, T1, ORANGE), (2, T2, GREEN)):
    fig.add_trace(go.Surface(x=X, y=Y, z=f(X, Y), colorscale=[[0, BLUE], [1, BLUE]], showscale=False, opacity=0.55), 1, col)
    fig.add_trace(go.Surface(x=X, y=Y, z=T(X, Y), colorscale=[[0, c], [1, c]], showscale=False, opacity=0.6), 1, col)
    fig.add_trace(go.Scatter3d(x=[1], y=[1], z=[3], mode="markers", marker=dict(size=6, color="black")), 1, col)
fig.update_scenes(xaxis_title="x", yaxis_title="y", zaxis_title="f", zaxis=dict(range=[-2, 14], nticks=5),
                  xaxis=dict(tickvals=[0, 1]), yaxis=dict(tickvals=[0, 1, 2]),
                  camera=dict(eye=dict(x=1.25, y=-1.35, z=0.55), center=dict(x=0, y=0, z=-0.1)))
fig.update_layout(template="simple_white", width=1150, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=0, r=0, t=40, b=0))
fig.update_annotations(font_size=26)
fig.write_image(here / "taylor_plane.png", scale=2)
fig.write_image(here / "taylor_plane.pdf")
