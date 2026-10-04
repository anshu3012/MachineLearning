"""Section 3.2: the three orthogonal matrices of the Note act on a grid and an L-shaped tile.
V (rotation 45 degrees), U (rotation 71.6 degrees), the reflection [[1, 0], [0, -1]]: squares stay unit squares,
lengths and angles are kept, det is +1 for rotations and -1 for the flip.  Run: python orthogonal_moves.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#BBBBBB"
V = np.array([[1, -1], [1, 1]]) / np.sqrt(2)
U = np.array([[1, -3], [3, 1]]) / np.sqrt(10)
F = np.array([[1, 0], [0, -1]])
MATS = [("V: rotate 45°", V), ("U: rotate 71.6°", U), ("flip across x-axis", F)]
for _, Q in MATS:
    assert np.allclose(Q.T @ Q, np.eye(2))                     # orthonormal columns: Q^T Q = I
assert np.isclose(np.linalg.det(V), 1) and np.isclose(np.linalg.det(U), 1) and np.isclose(np.linalg.det(F), -1)
assert np.isclose(np.degrees(np.arctan2(U[1, 0], U[0, 0])), 71.565, atol=1e-3)
L = np.array([[0, 0], [2, 0], [2, 1], [1, 1], [1, 2], [0, 2], [0, 0]]).T    # an L tile: shows a flip

fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=[f"{n}  (det {np.linalg.det(Q):+.0f})" for n, Q in MATS])
for col, (_, Q) in enumerate(MATS, start=1):
    for s in range(-2, 3):
        for a, b in (([s, s], [-2, 2]), ([-2, 2], [s, s])):
            p = Q @ np.array([a, b])
            fig.add_trace(go.Scatter(x=p[0], y=p[1], mode="lines", line=dict(color=GREY, width=1)), 1, col)
    fig.add_trace(go.Scatter(x=L[0], y=L[1], mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, col)
    P = Q @ L
    fig.add_trace(go.Scatter(x=P[0], y=P[1], fill="toself", mode="lines", line=dict(color=ORANGE, width=3),
                             fillcolor="rgba(245,133,24,0.35)"), 1, col)
    for v, c in ((Q[:, 0], BLUE), (Q[:, 1], GREEN)):
        fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref=f"x{col}", yref=f"y{col}", axref=f"x{col}",
                           ayref=f"y{col}", showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=c, text="")
    fig.update_xaxes(range=[-2.6, 2.6], visible=False, row=1, col=col)
    fig.update_yaxes(range=[-2.6, 2.6], visible=False, scaleanchor=f"x{col}", row=1, col=col)
fig.update_layout(template="simple_white", width=1350, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=22), margin=dict(l=20, r=20, t=70, b=20))
fig.update_annotations(font_size=24)
fig.write_image(HERE / "orthogonal_moves.png", scale=2)
