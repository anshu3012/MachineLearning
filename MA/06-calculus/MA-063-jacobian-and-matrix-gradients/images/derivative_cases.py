"""The four shapes of a derivative, one small function per panel (Plotly, static).
1 number -> number: f(x) = x^2 at x = 3, slope f'(3) = 6 (1 x 1).
2 vector -> number: f(x, y) = x^2 + y^2 at (2, 3), gradient [4, 6] (1 x 2 row), an arrow on the contour map.
3 number -> vector: g(t) = (t, t^2) at t = 1, derivative (1, 2) (2 x 1 column), the velocity arrow on the path.
4 vector -> vector: polar f(r, theta) = (r cos theta, r sin theta) at (2, pi/6), Jacobian 2 x 2; its two columns are
  where a unit step in r and a unit step in theta land, drawn at the output point.
Run: python derivative_cases.py -> derivative_cases.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#6B6B6B"
J = np.array([[np.cos(np.pi / 6), -2 * np.sin(np.pi / 6)], [np.sin(np.pi / 6), 2 * np.cos(np.pi / 6)]])
assert np.allclose(J, [[0.866, -1], [0.5, 1.732]], atol=1e-3)

fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.12, vertical_spacing=0.2,
                    subplot_titles=("Case 1: number → number<br>f(x) = x²,  f′(3) = 6  (1 × 1)",
                                    "Case 2: vector → number<br>f(x, y) = x² + y²,  ∇f(2, 3) = [4, 6]  (1 × 2)",
                                    "Case 3: number → vector<br>g(t) = (t, t²),  g′(1) = [1, 2]ᵀ  (2 × 1)",
                                    "Case 4: vector → vector<br>polar map at (2, π/6),  J  (2 × 2)"))


def arrow(fig, x0, y0, x1, y1, color, ax, text="", tx=0, ty=0):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref=f"x{ax}", yref=f"y{ax}", axref=f"x{ax}", ayref=f"y{ax}",
                       showarrow=True, arrowhead=3, arrowwidth=4, arrowsize=1, arrowcolor=color, text="")
    if text:
        fig.add_annotation(x=x1 + tx, y=y1 + ty, xref=f"x{ax}", yref=f"y{ax}", text=f"<b>{text}</b>", showarrow=False, bgcolor="rgba(255,255,255,0.9)",
                           font=dict(size=19, color=color))


# 1: curve and tangent line of slope 6
x = np.linspace(0, 4.5, 100)
fig.add_trace(go.Scatter(x=x, y=x ** 2, mode="lines", line=dict(color=BLUE, width=4)), row=1, col=1)
xt = np.array([1.8, 4.2])
fig.add_trace(go.Scatter(x=xt, y=9 + 6 * (xt - 3), mode="lines", line=dict(color=ORANGE, width=4)), row=1, col=1)
fig.add_trace(go.Scatter(x=[3], y=[9], mode="markers", marker=dict(size=14, color="black")), row=1, col=1)
fig.add_annotation(x=1.3, y=14, xref="x", yref="y", text="<b>one number:<br>slope 6</b>", showarrow=False,
                   font=dict(size=19, color=ORANGE))
fig.update_xaxes(title="x", range=[0, 4.5], row=1, col=1)
fig.update_yaxes(title="f", range=[0, 20], row=1, col=1)

# 2: contour map and gradient arrow (drawn at 1/4 length)
g = np.linspace(-1, 5, 120)
GX, GY = np.meshgrid(g, g)
fig.add_trace(go.Contour(x=g, y=g, z=GX ** 2 + GY ** 2, contours=dict(start=2, end=40, size=4, coloring="lines"),
                         line=dict(width=1.5), colorscale=[[0, "#9ecae1"], [1, "#08519c"]], showscale=False),
              row=1, col=2)
fig.add_trace(go.Scatter(x=[2], y=[3], mode="markers", marker=dict(size=14, color="black")), row=1, col=2)
arrow(fig, 2, 3, 3, 4.5, ORANGE, 2, "[4, 6]: one row,<br>one entry per input", tx=-0.6, ty=-2.6)
fig.update_xaxes(title="x", range=[-1, 5], row=1, col=2)
fig.update_yaxes(title="y", range=[-1, 5], scaleanchor="x2", row=1, col=2)

# 3: path and its velocity arrow (drawn at 1/2 length)
t = np.linspace(-0.3, 1.8, 100)
fig.add_trace(go.Scatter(x=t, y=t ** 2, mode="lines", line=dict(color=BLUE, width=4)), row=2, col=1)
fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=14, color="black")), row=2, col=1)
arrow(fig, 1, 1, 1.5, 2, ORANGE, 3, "[1, 2]ᵀ: one column,<br>one entry per output", tx=-1.05, ty=0.35)
fig.update_xaxes(title="first output", range=[-0.3, 1.9], row=2, col=1)
fig.update_yaxes(title="second output", range=[-0.2, 3.2], row=2, col=1)

# 4: polar grid lines through the point, and the two Jacobian columns (drawn at 1/2 length)
th = np.linspace(0, np.pi / 2, 100)
fig.add_trace(go.Scatter(x=2 * np.cos(th), y=2 * np.sin(th), mode="lines", line=dict(color=GREY, width=2, dash="dot")), row=2, col=2)
r = np.linspace(0, 3, 10)
fig.add_trace(go.Scatter(x=r * np.cos(np.pi / 6), y=r * np.sin(np.pi / 6), mode="lines", line=dict(color=GREY, width=2, dash="dot")),
              row=2, col=2)
p = np.array([2 * np.cos(np.pi / 6), 1.0])
fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(size=14, color="black")), row=2, col=2)
c1, c2 = p + 0.5 * J[:, 0], p + 0.5 * J[:, 1]
arrow(fig, *p, *c1, GREEN, 4, "column 1: step in r", tx=0.1, ty=-0.6)
arrow(fig, *p, *c2, PURPLE, 4, "column 2: step in θ", tx=-0.2, ty=0.25)
fig.update_xaxes(title="x", range=[-0.3, 3.2], row=2, col=2)
fig.update_yaxes(title="y", range=[-0.3, 2.6], scaleanchor="x4", row=2, col=2)

fig.update_layout(template="simple_white", width=1150, height=1050, font=FONT, showlegend=False,
                  margin=dict(l=70, r=30, t=90, b=60))
fig.update_annotations(selector=dict(xref="paper"), font_size=21)
fig.write_image(here / "derivative_cases.png", scale=2)
