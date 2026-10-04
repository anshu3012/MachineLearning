"""The constrained problem of the Note (Plotly): contours of f = x^2 + 2y^2 and the feasible region, the line
x + y = 3. The unconstrained minimum (0, 0) has f = 0 but is not on the line; (3, 0) is feasible with f = 9; the
best feasible point is (2, 1) with f = 6."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, RED

here = Path(__file__).parent
f = lambda x, y: x ** 2 + 2 * y ** 2
assert f(3, 0) == 9 and f(2, 1) == 6 and 2 + 1 == 3
g = np.linspace(-1.5, 4, 221)
X, Y = np.meshgrid(g, g)
fig = go.Figure(go.Contour(x=g, y=g, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.6,
                           contours=dict(start=0, end=30, size=3, showlabels=True, labelfont=dict(size=13)), line=dict(width=1)))
xs = np.array([-1, 4])
fig.add_scatter(x=xs, y=3 - xs, mode="lines", line=dict(color=GREEN, width=6), name="feasible region: x + y = 3")
pts = [((0, 0), RED, "(0, 0): f = 0, not allowed"), ((3, 0), "black", "(3, 0): allowed, f = 9"),
       ((2, 1), GREEN, "(2, 1): best allowed, f = 6")]
for (px, py), c, t in pts:
    fig.add_scatter(x=[px], y=[py], mode="markers", marker=dict(size=16, color=c, symbol="x" if c == RED else "circle",
                                                                line=dict(color="white", width=1)), showlegend=False)
    fig.add_annotation(x=px, y=py, text=t, ax=60, ay=-45, font=dict(size=19, color=c), bgcolor="white", arrowcolor=c)
fig.update_layout(template="simple_white", width=850, height=760, font=FONT,
                  xaxis=dict(title="x", range=[-1.5, 4]), yaxis=dict(title="y", range=[-1.5, 4], scaleanchor="x"),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=20, b=70))
fig.write_image(here / "feasible.png", scale=2)
