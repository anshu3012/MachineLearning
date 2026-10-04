"""A function of two variables: a vector in, one number out (Plotly). Contour map of the running example
f(x1, x2) = x1^2 + x1 x2 + 2 x2^2, with four input vectors marked and the single number f gives each:
(1, 1) -> 4, (2, -1) -> 4 (the same contour line), (0, 1) -> 2, (-1, 0) -> 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, ORANGE

here = Path(__file__).parent
f = lambda a, b: a * a + a * b + 2 * b * b
pts = [(1, 1), (2, -1), (0, 1), (-1, 0)]
assert [f(*p) for p in pts] == [4, 4, 2, 1]
g = np.linspace(-2.5, 2.5, 201)
A, B = np.meshgrid(g, g)
fig = go.Figure(go.Contour(x=g, y=g, z=f(A, B), colorscale="Blues", reversescale=True, showscale=False, opacity=0.7,
                           contours=dict(start=0, end=16, size=1, showlabels=True, labelfont=dict(size=13)),
                           line=dict(width=1)))
for p in pts:
    fig.add_annotation(x=p[0], y=p[1], text=f"<b>[{p[0]}, {p[1]}] ↦ {f(*p)}</b>", ax=40, ay=-40,
                       font=dict(size=20, color="black"), bgcolor="white", arrowcolor=ORANGE, arrowwidth=2)
fig.add_scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers",
                marker=dict(size=14, color=ORANGE, line=dict(color="white", width=2)))
fig.update_layout(template="simple_white", width=760, height=700, font=FONT, showlegend=False,
                  xaxis=dict(title="x₁", range=[-2.5, 2.5]), yaxis=dict(title="x₂", range=[-2.5, 2.5], scaleanchor="x"),
                  margin=dict(l=70, r=20, t=20, b=70))
fig.write_image(here / "vector_in.png", scale=2)
