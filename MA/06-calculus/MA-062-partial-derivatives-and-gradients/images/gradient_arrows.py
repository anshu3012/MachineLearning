"""Contour map of f(x1, x2) = x1^2 + x1 x2 + 2 x2^2 with gradient arrows (Plotly). Each arrow is the gradient
[2 x1 + x2, x1 + 4 x2], scaled down to fit; it crosses the contour lines at right angles and points uphill.
At (1, 1) the gradient is [3, 5] (orange) and the negative gradient (green) is the steepest way down."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
grad = lambda a, b: np.array([2 * a + b, a + 4 * b])
g = np.linspace(-2.2, 2.2, 200)
A, B = np.meshgrid(g, g)
fig = go.Figure(go.Contour(x=g, y=g, z=f(A, B), colorscale="Blues", reversescale=True, showscale=False, opacity=0.55,
                           contours=dict(start=0.5, end=14, size=1.5), line=dict(width=1)))
S = 0.06                                       # arrow length = S * gradient
for a in np.arange(-1.6, 1.61, 0.8):
    for b in np.arange(-1.6, 1.61, 0.8):
        if abs(a - 1) < 0.3 and abs(b - 1) < 0.3 or (a, b) == (0, 0):
            continue
        d = S * grad(a, b)
        fig.add_annotation(x=a + d[0], y=b + d[1], ax=a, ay=b, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="black", text="")
d = 0.12 * grad(1, 1)
for sign, col, lab, shift in ((1, ORANGE, "gradient [3, 5]", (-14, 4)), (-1, GREEN, "minus gradient", (-8, -6))):
    tip = (1 + sign * d[0], 1 + sign * d[1])
    fig.add_annotation(x=tip[0], y=tip[1], ax=1, ay=1, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.2, arrowwidth=3.5, arrowcolor=col, text="")
    fig.add_annotation(x=tip[0], y=tip[1], text=lab, showarrow=False, font=dict(color=col, size=17),
                       xanchor="right", xshift=shift[0], yshift=shift[1], bgcolor="white")
fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=10, color="black")))
fig.update_xaxes(title="x1", range=[-2.3, 2.3], constrain="domain")
fig.update_yaxes(title="x2", range=[-2.3, 2.3], scaleanchor="x")
fig.update_layout(template="simple_white", width=640, height=600, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(here / "gradient_arrows.png", scale=2)
fig.write_image(here / "gradient_arrows.pdf")
