"""Plotly figures for the linear and quadratic programming Note.
lp_region: maximise 3 x1 + 2 x2 subject to x1 + x2 <= 4, x1 + 3 x2 <= 9, x1 <= 3, x1, x2 >= 0.
  Feasible polygon with corners (0,0), (3,0), (3,1), (1.5,2.5), (0,3); profit lines 6, 9, 11; best corner (3, 1), profit 11.
qp_region: minimise 1/2 x^T Q x + c^T x with Q = [[2,1],[1,2]], c = (-8,-7), subject to x1 + x2 <= 2, x1, x2 >= 0.
  Unconstrained minimum (3, 2); constrained minimum (1.5, 0.5), value -12.25, multiplier 4.5."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import linprog, minimize, LinearConstraint

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=17)
star = dict(symbol="star", size=22, color=GREEN, line=dict(color="black", width=1))

# ---------- checks
r = linprog([-3, -2], A_ub=[[1, 1], [1, 3], [1, 0]], b_ub=[4, 9, 3], bounds=[(0, None)] * 2)
assert np.allclose(r.x, [3, 1]) and abs(r.fun + 11) < 1e-9
Q, c = np.array([[2, 1], [1, 2]]), np.array([-8, -7])
q = minimize(lambda x: 0.5 * x @ Q @ x + c @ x, [0, 0], method="trust-constr",
             constraints=[LinearConstraint([[1, 1]], -np.inf, 2)], bounds=[(0, None)] * 2)
assert np.allclose(q.x, [1.5, 0.5], atol=1e-3) and abs(q.fun + 12.25) < 1e-3

# ---------- LP
corners = np.array([[0, 0], [3, 0], [3, 1], [1.5, 2.5], [0, 3], [0, 0]])
fig = go.Figure(layout=dict(showlegend=False))
fig.add_trace(go.Scatter(x=corners[:, 0], y=corners[:, 1], mode="lines", fill="toself", showlegend=False,
                         fillcolor="rgba(76,120,168,0.18)", line=dict(color=BLUE, width=2.5)))
for p, dash in ((6, "dot"), (9, "dash"), (11, "solid")):
    x1 = np.array([0, 4.5])
    fig.add_trace(go.Scatter(x=x1, y=(p - 3 * x1) / 2, mode="lines", line=dict(color=ORANGE, width=2.5, dash=dash),
                             name=f"profit 3x1 + 2x2 = {p}", showlegend=True))
fig.add_trace(go.Scatter(x=corners[:5, 0], y=corners[:5, 1], mode="markers", marker=dict(size=9, color="black"), showlegend=False))
fig.add_trace(go.Scatter(x=[3], y=[1], mode="markers", marker=star, showlegend=False))
for (x, y, t, xs, ys) in ((3, 1, "best corner (3, 1)", 85, -14), (1.5, 2.5, "(1.5, 2.5): 9.5", 70, 12),
                          (3, 0, "(3, 0): 9", -45, 16), (0, 3, "(0, 3): 6", 45, 14)):
    fig.add_annotation(x=x, y=y, text=t, showarrow=False, xshift=xs, yshift=ys, font=dict(size=16), bgcolor="white")
fig.add_annotation(x=1.2, y=1.0, text="feasible", showarrow=False, font=dict(color=BLUE, size=18))
fig.update_xaxes(title="x1 (product A)", range=[-0.2, 4.6], constrain="domain")
fig.update_yaxes(title="x2 (product B)", range=[-0.2, 4.2], scaleanchor="x")
fig.update_layout(template="simple_white", width=680, height=600, font=FONT, showlegend=True,
                  legend=dict(x=0.98, y=0.98, xanchor="right", bgcolor="white", font=dict(size=15)),
                  margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(here / "lp_region.png", scale=2)
fig.write_image(here / "lp_region.pdf")

# ---------- QP
g = np.linspace(-0.5, 4, 200)
X1, X2 = np.meshgrid(g, g)
F = X1 ** 2 + X1 * X2 + X2 ** 2 - 8 * X1 - 7 * X2
fig = go.Figure(go.Contour(x=g, y=g, z=F, colorscale="Blues", reversescale=True, zmin=-20, zmax=12, showscale=False, opacity=1,
                           contours=dict(start=-18, end=6, size=3), line=dict(width=1)))
fig.add_trace(go.Scatter(x=[0, 2, 0, 0], y=[0, 0, 2, 0], mode="lines", fill="toself",
                         fillcolor="rgba(245,133,24,0.25)", line=dict(color=ORANGE, width=3)))
fig.add_trace(go.Scatter(x=[3], y=[2], mode="markers", marker=dict(size=12, color="black")))
fig.add_trace(go.Scatter(x=[1.5], y=[0.5], mode="markers", marker=star))
for (x, y, t, xs, ys, col) in ((3, 2, "unconstrained minimum (3, 2)", 0, 18, "black"),
                               (1.5, 0.5, "constrained minimum (1.5, 0.5)", 95, 22, GREEN),
                               (0.55, 0.45, "feasible", 0, 0, ORANGE)):
    fig.add_annotation(x=x, y=y, text=t, showarrow=False, xshift=xs, yshift=ys, font=dict(size=16, color=col),
                       bgcolor="white")
fig.update_xaxes(title="x1", range=[-0.5, 4], constrain="domain")
fig.update_yaxes(title="x2", range=[-0.5, 4], scaleanchor="x")
fig.update_layout(template="simple_white", width=640, height=600, showlegend=False, font=FONT,
                  margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(here / "qp_region.png", scale=2)
fig.write_image(here / "qp_region.pdf")
