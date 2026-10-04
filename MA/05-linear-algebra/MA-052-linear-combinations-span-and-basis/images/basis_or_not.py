"""Basis or not, for the target [3, -2]. Left: v = [1, 1], w = [1, -1] is a basis: one way only, 0.5 v + 2.5 w.
Middle: [1, 2] and [2, 4] lie on one line, so no combination reaches [3, -2]. Right: three vectors [1, 0], [0, 1],
[1, 1] reach it in many ways, e.g. 3, -2, 0 and 2, -3, 1: a spare vector makes coordinates non-unique."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
t = np.array([3, -2.0])
v, w = np.array([1, 1.0]), np.array([1, -1.0])
assert np.allclose(np.linalg.solve(np.c_[v, w], t), [0.5, 2.5])
assert np.linalg.matrix_rank(np.c_[[1, 2], [2, 4]]) == 1
e1, e2, e3 = np.array([1, 0.0]), np.array([0, 1.0]), np.array([1, 1.0])
assert np.allclose(3 * e1 - 2 * e2, t) and np.allclose(2 * e1 - 3 * e2 + e3, t)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06, subplot_titles=[
    "basis: one way, 0.5v + 2.5w", "not a basis: the span is a line", "spare vector: many ways"])


def arrow(c, start, end, col, width=4):
    fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1], xref=f"x{c}", yref=f"y{c}", axref=f"x{c}",
                       ayref=f"y{c}", arrowhead=3, arrowwidth=width, arrowcolor=col, showarrow=True)


for c in (1, 2, 3):
    fig.add_scatter(x=[3], y=[-2], mode="markers+text", text=["[3, −2]"], textposition="bottom right",
                    marker=dict(size=13, color="black"), textfont=dict(size=17), row=1, col=c)
arrow(1, (0, 0), 0.5 * v, "#4C78A8"); arrow(1, 0.5 * v, t, "#F58518")
fig.add_scatter(x=[-3, 3], y=[-6, 6], mode="lines", line=dict(color="#E45756", width=3), row=1, col=2)
arrow(2, (0, 0), (1, 2), "#4C78A8"); arrow(2, (0, 0), (2, 4), "#F58518", 2)
arrow(3, (0, 0), (3, 0), "#4C78A8"); arrow(3, (3, 0), t, "#F58518")
arrow(3, (0, 0), (2, 0), "#9a9a9a", 2); arrow(3, (2, 0), (2, -3), "#9a9a9a", 2); arrow(3, (2, -3), t, "#54A24B", 2)
for c in (1, 2, 3):
    fig.update_xaxes(range=[-1, 4.5], zeroline=True, row=1, col=c)
    fig.update_yaxes(range=[-3.5, 4.5], zeroline=True, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
for a in fig.layout.annotations[:3]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1500, height=600, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=40, r=20, t=60, b=40))
fig.write_image(here / "basis_or_not.png", scale=2)
fig.write_image(here / "basis_or_not.pdf")
