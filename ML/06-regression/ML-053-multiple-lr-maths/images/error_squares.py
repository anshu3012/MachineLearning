"""Section 3 of Note ML-053: the error vector e = y - X beta and the sum of squared errors e^T e, drawn on the four
students of the worked example (Section 6.1) with their best line beta = (-0.81, 0.57). Each residual is a
vertical segment; its square is drawn as a real square, and E is the total area. Plotly.
Run: python error_squares.py -> error_squares.png, error_squares.pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
cgpa = np.array([6.89, 5.12, 7.82, 7.42])
y = np.array([3.26, 1.98, 3.25, 3.67])
X = np.column_stack([np.ones(4), cgpa])
beta = np.linalg.solve(X.T @ X, X.T @ y)
e = y - X @ beta
E = e @ e
assert np.allclose(beta.round(2), [-0.81, 0.57]) and np.isclose(E, (e ** 2).sum())
print("e =", e.round(2), " E =", round(E, 3))

fig = go.Figure()
xs = np.array([4.9, 8.1])
fig.add_trace(go.Scatter(x=xs, y=beta[0] + beta[1] * xs, mode="lines", line=dict(color=BLUE, width=3)))
for xi, yi, ei in zip(cgpa, y, e):
    yh = yi - ei
    side = abs(ei)
    x0 = xi if ei < 0 or xi < 7.6 else xi - side          # put the square on the side with room
    fig.add_shape(type="rect", x0=x0, x1=x0 + side if x0 == xi else xi, y0=min(yi, yh), y1=max(yi, yh),
                  fillcolor=ORANGE, opacity=0.35, line=dict(color=ORANGE, width=1))
    fig.add_shape(type="line", x0=xi, x1=xi, y0=yh, y1=yi, line=dict(color=RED, width=4), opacity=1)
    up = ei > 0
    fig.add_annotation(x=xi, y=max(yi, yh) if up else min(yi, yh), yshift=8 if up else -8,
                       yanchor="bottom" if up else "top", showarrow=False,
                       text=f"e = {ei:+.2f}<br>e² = {ei ** 2:.3f}", font=dict(color=RED, size=18))
fig.add_trace(go.Scatter(x=cgpa, y=y, mode="markers", marker=dict(color="black", size=12)))
fig.add_annotation(x=0.02, y=0.97, xref="paper", yref="paper", xanchor="left", yanchor="top", showarrow=False,
                   align="left", font=dict(size=22),
                   text=f"E = e<sup>T</sup>e = sum of the orange areas = {E:.3f}")
fig.update_layout(template="simple_white", width=1000, height=640, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=30, t=30, b=70))
fig.update_xaxes(title="cgpa", range=[4.9, 8.1], dtick=0.5)
fig.update_yaxes(title="package", range=[1.5, 4.3], scaleanchor="x", scaleratio=1)
fig.write_image(HERE / "error_squares.png", scale=2)
fig.write_image(HERE / "error_squares.pdf")
