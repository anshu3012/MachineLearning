"""Three ways to draw a loss (section 3). Left: one parameter, L(w) = w^2 / 2 (the loss of section 7), a curve.
Middle: two parameters, the narrow valley L(w1, w2) = (w1^2 + 100 w2^2) / 2 of Figure 1, as a surface. Right: the
same valley seen from above, a contour plot. Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
w = np.linspace(-3, 3, 201)
g1, g2 = np.linspace(-10, 10, 101), np.linspace(-1, 1, 101)
G1, G2 = np.meshgrid(g1, g2)
L = (G1 ** 2 + 100 * G2 ** 2) / 2
assert L.min() == 0 and abs((10 ** 2 + 0) / 2 - L[50, -1]) < 1e-9
fig = make_subplots(rows=1, cols=3, specs=[[{"type": "xy"}, {"type": "scene"}, {"type": "xy"}]],
                    horizontal_spacing=0.06, subplot_titles=("One parameter: a curve", "Two parameters: a surface",
                                                             "The same surface from above: contours"))
fig.add_scatter(x=w, y=w ** 2 / 2, mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False, row=1, col=1)
fig.add_surface(x=g1, y=g2, z=L, colorscale="Viridis", showscale=False, opacity=0.95, row=1, col=2)
fig.add_trace(go.Contour(x=g1, y=g2, z=L, colorscale="Viridis", showscale=False, ncontours=14,
                         contours=dict(coloring="lines"), line=dict(width=2)), row=1, col=3)
fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="star", size=16, color="black"), showlegend=False,
                row=1, col=3)
fig.update_xaxes(title_text="w", row=1, col=1)
fig.update_yaxes(title_text="loss L", row=1, col=1)
fig.update_xaxes(title_text="w₁ (along the valley)", row=1, col=3)
fig.update_yaxes(title_text="w₂ (across)", row=1, col=3)
fig.update_layout(template="simple_white", width=1500, height=520, font=dict(family="Latin Modern Roman", size=18),
                  scene=dict(xaxis_title="w₁", yaxis_title="w₂", zaxis_title="L",
                             camera=dict(eye=dict(x=1.4, y=-1.5, z=0.9))),
                  margin=dict(l=60, r=20, t=60, b=60))
for a in fig.layout.annotations:
    a.font.size = 19
fig.write_image(HERE / "loss_views.png", scale=2)
