"""Three quadratic surfaces f = (1/2) d^T H d and the signs of the Hessian's eigenvalues (Plotly 3D):
both positive -> bowl (a minimum), opposite signs -> saddle, both negative -> cap (a maximum)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
cases = (("bowl: H = [[2, 0], [0, 1]]<br>eigenvalues 2, 1", np.array([[2, 0], [0, 1.0]]), BLUE),
         ("saddle: H = [[2, 0], [0, -1]]<br>eigenvalues 2, -1", np.array([[2, 0], [0, -1.0]]), ORANGE),
         ("cap: H = [[-2, 0], [0, -1]]<br>eigenvalues -2, -1", np.array([[-2, 0], [0, -1.0]]), RED))
g = np.linspace(-1.5, 1.5, 40)
X, Y = np.meshgrid(g, g)
fig = make_subplots(1, 3, specs=[[{"type": "scene"}] * 3], horizontal_spacing=0.0,
                    subplot_titles=[c[0] for c in cases])
for col, (_, H, c) in enumerate(cases, start=1):
    Z = 0.5 * (H[0, 0] * X ** 2 + 2 * H[0, 1] * X * Y + H[1, 1] * Y ** 2)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, c], [1, c]], showscale=False, opacity=0.8,
                             contours=dict(z=dict(show=True, color=GREY, width=1))), 1, col)
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=5, color="black")), 1, col)
fig.update_scenes(xaxis_title="x", yaxis_title="y", zaxis_title="f", zaxis=dict(range=[-3.6, 3.6], nticks=4),
                  xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False), camera=dict(eye=dict(x=1.6, y=-1.6, z=0.9)))
fig.update_layout(template="simple_white", width=1200, height=470, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=0, r=0, t=70, b=0))
fig.update_annotations(font_size=24)
fig.write_image(here / "hessian_shapes.png", scale=2)
fig.write_image(here / "hessian_shapes.pdf")
