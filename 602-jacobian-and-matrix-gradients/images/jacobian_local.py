"""The Jacobian as the local linear map (Plotly). Polar coordinates f(r, theta) = [r cos theta, r sin theta] bend a
straight grid (left) into circles and rays (right). A small cell at (r, theta) = (2, pi/6) (orange) lands on a
curved cell that is almost the parallelogram spanned by the Jacobian's columns times the cell's sides (green).
det J = r = 2: the cell's area is doubled."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
P = lambda r, t: (r * np.cos(t), r * np.sin(t))
R0, T0, DR, DT = 2.0, np.pi / 6, 0.4, 0.2
J = np.array([[np.cos(T0), -R0 * np.sin(T0)], [np.sin(T0), R0 * np.cos(T0)]])
assert abs(np.linalg.det(J) - R0) < 1e-12
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=("input: (r, θ)", "output: (x, y) = f(r, θ)"))
line = dict(color="#BBBBBB", width=1.2)
rs, ts = np.arange(1.0, 3.01, 0.2), np.arange(0, np.pi / 2 + 1e-9, 0.1)
s = np.linspace(0, 1, 60)
for r in rs:
    fig.add_trace(go.Scatter(x=[r, r], y=[0, ts[-1]], mode="lines", line=line), 1, 1)
    x, y = P(r, ts[0] + s * (ts[-1] - ts[0]))
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=line), 1, 2)
for t in ts:
    fig.add_trace(go.Scatter(x=[1, 3], y=[t, t], mode="lines", line=line), 1, 1)
    x, y = P(1 + 2 * s, t)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=line), 1, 2)
# the small cell, before and after
cr = np.r_[R0 + DR * s, np.full(60, R0 + DR), R0 + DR * s[::-1], np.full(60, R0)]
ct = np.r_[np.full(60, T0), T0 + DT * s, np.full(60, T0 + DT), T0 + DT * s[::-1]]
fig.add_trace(go.Scatter(x=cr, y=ct, fill="toself", mode="lines", line=dict(color=ORANGE, width=3),
                         fillcolor="rgba(245,133,24,0.35)"), 1, 1)
x, y = P(cr, ct)
fig.add_trace(go.Scatter(x=x, y=y, fill="toself", mode="lines", line=dict(color=ORANGE, width=3),
                         fillcolor="rgba(245,133,24,0.35)"), 1, 2)
o = np.array(P(R0, T0))
c1, c2 = J[:, 0] * DR, J[:, 1] * DT
par = np.array([o, o + c1, o + c1 + c2, o + c2, o])
fig.add_trace(go.Scatter(x=par[:, 0], y=par[:, 1], mode="lines", line=dict(color=GREEN, width=3, dash="dash")), 1, 2)
for vec, lab, xs, ys in ((c1, "column 1 of J \u00d7 \u0394r", 10, -12), (c2, "column 2 of J \u00d7 \u0394\u03b8", -6, 12)):
    fig.add_annotation(x=o[0] + vec[0], y=o[1] + vec[1], ax=o[0], ay=o[1], xref="x2", yref="y2", axref="x2", ayref="y2",
                       showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor=GREEN, text="")
    fig.add_annotation(x=o[0] + vec[0], y=o[1] + vec[1], xref="x2", yref="y2", text=lab, showarrow=False,
                       font=dict(color=GREEN, size=16), xanchor="left" if xs > 0 else "right", xshift=xs, yshift=ys,
                       bgcolor="white")
fig.add_trace(go.Scatter(x=[R0], y=[T0], mode="markers", marker=dict(size=9, color="black")), 1, 1)
fig.add_trace(go.Scatter(x=[o[0]], y=[o[1]], mode="markers", marker=dict(size=9, color="black")), 1, 2)
fig.update_xaxes(title="r", range=[0.9, 3.1], row=1, col=1)
fig.update_yaxes(title="θ (radians)", range=[-0.05, 1.65], row=1, col=1)
fig.update_xaxes(title="x", range=[-0.1, 3.1], row=1, col=2)
fig.update_yaxes(title="y", range=[-0.1, 3.1], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(selector=dict(xref="paper"), font_size=18)
fig.write_image(here / "jacobian_local.png", scale=2)
fig.write_image(here / "jacobian_local.pdf")
