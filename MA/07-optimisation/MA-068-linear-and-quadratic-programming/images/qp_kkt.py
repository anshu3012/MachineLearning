"""The KKT condition of the quadratic program at its answer (Plotly). Contours of x1^2 + x1 x2 + x2^2 - 8x1 - 7x2 and
the triangle x1 + x2 <= 2, x1, x2 >= 0. At (1.5, 0.5) the downhill direction -grad f = [4.5, 4.5] points straight out
of the edge x1 + x2 = 2: it is lambda = 4.5 times the edge's normal [1, 1], so sliding along the edge cannot help."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, RED

here = Path(__file__).parent
Q, c = np.array([[2, 1], [1, 2]]), np.array([-8, -7])
f = lambda X, Y: X ** 2 + X * Y + Y ** 2 - 8 * X - 7 * Y
x = np.array([1.5, 0.5])
g = Q @ x + c
assert np.allclose(g, [-4.5, -4.5]) and np.isclose(f(*x), -12.25)
gr = np.linspace(-0.5, 4, 200)
X, Y = np.meshgrid(gr, gr)
fig = go.Figure(go.Contour(x=gr, y=gr, z=f(X, Y), colorscale="Blues", reversescale=True, zmin=-20, zmax=12, showscale=False, opacity=1,
                           contours=dict(start=-18, end=6, size=3), line=dict(width=1)))
fig.add_scatter(x=[0, 2, 0, 0], y=[0, 0, 2, 0], fill="toself", fillcolor="rgba(245,133,24,0.25)", line=dict(color=ORANGE, width=3),
                name="feasible triangle")
fig.add_scatter(x=[3], y=[2], mode="markers", marker=dict(size=12, color="black", symbol="x"), name="unconstrained minimum (3, 2)")
fig.add_annotation(x=x[0] - 0.25 * g[0], y=x[1] - 0.25 * g[1], ax=x[0], ay=x[1], xref="x", yref="y", axref="x", ayref="y",
                   arrowhead=3, arrowsize=1.3, arrowwidth=4, arrowcolor=RED)
fig.add_annotation(x=x[0] - 0.25 * g[0], y=x[1] - 0.25 * g[1], text="−∇f = [4.5, 4.5] = 4.5 × [1, 1]", showarrow=False,
                   xanchor="left", xshift=8, font=dict(size=19, color=RED), bgcolor="white")
fig.add_scatter(x=[1.5], y=[0.5], mode="markers", marker=dict(size=18, color="black", symbol="star"), name="answer (1.5, 0.5)")
fig.update_layout(template="simple_white", width=900, height=760, font=FONT,
                  xaxis=dict(title="x₁", range=[-0.5, 4]), yaxis=dict(title="x₂", range=[-0.5, 4], scaleanchor="x"),
                  legend=dict(x=0.5, y=0.99), margin=dict(l=70, r=20, t=20, b=70))
fig.write_image(here / "qp_kkt.png", scale=2)
