"""Projection, one of the dot product's jobs: how far a = [3, 4] reaches along b = [7, 1]. The length of the shadow
is a . b / |b| = 24 / 5 = 4.8."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
a, b = np.array([3, 4.0]), np.array([7, 1.0])
u = b / np.linalg.norm(b)
p = (a @ u) * u
proj = a @ u
assert a @ b == 25 and round(proj, 2) == 3.54
fig = go.Figure()
fig.add_scatter(x=[0, 8.4], y=[0, 1.2], mode="lines", line=dict(color="#dddddd", dash="dot", width=2))
fig.add_scatter(x=[a[0], p[0]], y=[a[1], p[1]], mode="lines", line=dict(color="#9a9a9a", dash="dash", width=2))
for w, c, name, sh in ((a, "#4C78A8", "a = [3, 4]", (0, 18)), (b, "#F58518", "b = [7, 1]", (20, -18)),
                       (p, "#54A24B", "shadow of a on b:<br>a · b / ‖b‖ = 25 / 7.07 = 3.54", (30, -60))):
    fig.add_annotation(x=w[0], y=w[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                       arrowwidth=6 if c == "#54A24B" else 4, arrowcolor=c, opacity=0.9)
    fig.add_annotation(x=w[0], y=w[1], text=name, showarrow=False, xshift=sh[0], yshift=sh[1], font=dict(size=19, color=c),
                       xanchor="left" if sh[0] > 0 else "center")
fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=18),
                  showlegend=False, title=dict(text="Projection: a · b / ‖b‖ is how far a reaches along b", x=0.5),
                  xaxis=dict(range=[-0.5, 8.5], zeroline=True), yaxis=dict(range=[-1.2, 5.2], zeroline=True, scaleanchor="x"),
                  margin=dict(l=40, r=20, t=70, b=40))
fig.write_image(here / "projection.png", scale=2)
fig.write_image(here / "projection.pdf")
