"""The 3 x 2 matrix B = [[1, 1], [0, 1], [1, 0]] (Plotly 3-D). Every output B x is a mix of B's two columns
[1, 0, 1] and [1, 1, 0], so the outputs fill a flat sheet (a plane through the origin, blue). u1 = [2, 1, 1]/sqrt 6 and
u2 = [0, -1, 1]/sqrt 2 lie in the sheet; u3 = [1, -1, -1]/sqrt 3 sticks out of it at a right angle and is never reached.
Run: python tall_matrix.py -> tall_matrix.png, tall_matrix.pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
B = np.array([[1, 1], [0, 1], [1, 0]])
c1, c2 = B[:, 0], B[:, 1]
u1, u2, u3 = np.array([2, 1, 1]) / 6 ** 0.5, np.array([0, -1, 1]) / 2 ** 0.5, np.array([1, -1, -1]) / 3 ** 0.5
assert abs(u3 @ c1) < 1e-12 and abs(u3 @ c2) < 1e-12
U, s, Vt = np.linalg.svd(B)
assert np.allclose(s, [3 ** 0.5, 1])

a, b = np.meshgrid(np.linspace(-1.1, 1.1, 2), np.linspace(-1.1, 1.1, 2))
P = a[..., None] * u1 + b[..., None] * u2
fig = go.Figure(go.Surface(x=P[..., 0], y=P[..., 1], z=P[..., 2], opacity=0.35, showscale=False,
                           colorscale=[[0, BLUE], [1, BLUE]]))
for vec, col, lab in [(c1, "grey", "column 1"), (c2, "grey", "column 2"), (u1, ORANGE, "u<sub>1</sub>"),
                      (u2, GREEN, "u<sub>2</sub>"), (u3, RED, "u<sub>3</sub> (never reached)")]:
    fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]], mode="lines",
                               line=dict(color=col, width=9 if col != "grey" else 5, dash="solid")))
    fig.add_trace(go.Cone(x=[vec[0]], y=[vec[1]], z=[vec[2]], u=[vec[0]], v=[vec[1]], w=[vec[2]], sizemode="absolute",
                          sizeref=0.18, anchor="tip", showscale=False, colorscale=[[0, col], [1, col]]))
    off = np.array([0.55, 0.55, -0.2]) if col == RED else 0.15 * vec
    fig.add_trace(go.Scatter3d(x=[vec[0] + off[0]], y=[vec[1] + off[1]], z=[vec[2] + off[2]], mode="text", text=[lab],
                               textfont=dict(size=22, color=col if col != "grey" else "#444")))
fig.update_layout(template="simple_white", width=900, height=640, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=0, r=0, t=40, b=0),
                  title=dict(text="outputs of B fill a plane in 3-D", x=0.5, font=dict(size=26)),
                  scene=dict(xaxis_title="", yaxis_title="", zaxis_title="", aspectmode="cube",
                             xaxis=dict(range=[-1.6, 1.6], visible=False), yaxis=dict(range=[-1.6, 1.6], visible=False),
                             zaxis=dict(range=[-1.6, 1.6], visible=False), camera=dict(eye=dict(x=0.8, y=-0.8, z=0.55))))
fig.write_image(HERE / "tall_matrix.png", scale=2)
fig.write_image(HERE / "tall_matrix.pdf")
