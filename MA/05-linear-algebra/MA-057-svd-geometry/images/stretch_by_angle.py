"""Sections 4 and 5.2: how far A = [[3, 0], [4, 5]] stretches each unit vector, by its angle.
The top is sigma1 = 6.71 at 45 degrees (v1), the bottom sigma2 = 2.24 at 135 degrees (v2); i-hat and j-hat both reach 5.
Also: area of the unit circle through V^T, Sigma, U: only Sigma changes it, by sigma1 sigma2 = |det A| = 15.
Run: python stretch_by_angle.py -> stretch_by_angle.png, area_through_svd.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREEN, GREY = "#4C78A8", "#F58518", "#E45756", "#54A24B", "#6B6B6B"
A = np.array([[3.0, 0.0], [4.0, 5.0]])
U, s, Vt = np.linalg.svd(A)
deg = np.arange(0, 180.01, 0.5)
x = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
L = np.linalg.norm(A @ x, axis=0)
assert np.isclose(L.max(), s[0]) and deg[L.argmax()] == 45      # longest stretch: sigma1 at v1
assert np.isclose(L.min(), s[1]) and deg[L.argmin()] == 135     # shortest: sigma2 at v2
assert np.allclose(s, [6.708, 2.236], atol=1e-3)
assert L[deg == 0][0] == 5 and np.isclose(L[deg == 90][0], 5)   # i-hat -> [3, 4], j-hat -> [0, 5]

fig = go.Figure(go.Scatter(x=deg, y=L, mode="lines", line=dict(color=BLUE, width=4), showlegend=False))
for d, lab, c, pos in ((45, "v₁: σ₁ = 6.71", RED, "top center"), (135, "v₂: σ₂ = 2.24", RED, "bottom center"),
                       (0, "î: 5", GREY, "bottom right"), (90, "ĵ: 5", GREY, "top right")):
    fig.add_trace(go.Scatter(x=[d], y=[L[deg == d][0]], mode="markers+text", text=[lab], textposition=pos,
                             marker=dict(size=14, color=c), textfont=dict(color=c, size=24), showlegend=False))
fig.add_hline(y=s[0], line=dict(color=RED, dash="dot", width=1.5))
fig.add_hline(y=s[1], line=dict(color=RED, dash="dot", width=1.5))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="angle of the unit vector x (degrees)", tickvals=[0, 45, 90, 135, 180]),
                  yaxis=dict(title="length of A x", range=[0, 7.8]), margin=dict(l=70, r=30, t=30, b=70))
fig.write_image(HERE / "stretch_by_angle.png", scale=2)

# Area through the three factors
t = np.linspace(0, 2 * np.pi, 300)
c = np.array([np.cos(t), np.sin(t)])
steps = [("unit circle", c), ("after Vᵀ (rotate)", Vt @ c), ("after Σ (stretch)", np.diag(s) @ Vt @ c),
         ("after U (rotate)", U @ np.diag(s) @ Vt @ c)]
area = lambda p: 0.5 * abs(np.dot(p[0], np.roll(p[1], 1)) - np.dot(p[1], np.roll(p[0], 1)))
areas = [area(p) for _, p in steps]
assert np.allclose(areas[:2], np.pi, rtol=1e-3) and np.allclose(areas[2:], 15 * np.pi, rtol=1e-3)
assert np.isclose(s[0] * s[1], abs(np.linalg.det(A)))           # sigma1 sigma2 = |det A| = 15
fig = make_subplots(1, 4, horizontal_spacing=0.03, subplot_titles=[f"{n}<br>area {round(a / np.pi)}π".replace(" 1π", " π") for (n, _), a in zip(steps, areas)])
for k, (_, p) in enumerate(steps, start=1):
    fig.add_trace(go.Scatter(x=p[0], y=p[1], fill="toself", mode="lines", line=dict(color=ORANGE, width=3),
                             fillcolor="rgba(245,133,24,0.35)", showlegend=False), 1, k)
    fig.update_xaxes(range=[-7, 7], visible=False, row=1, col=k)
    fig.update_yaxes(range=[-7, 7], visible=False, scaleanchor=f"x{k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1400, height=470, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=10, r=10, t=100, b=10))
fig.update_annotations(font_size=24)
fig.write_image(HERE / "area_through_svd.png", scale=2)
