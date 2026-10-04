"""Reflection across the line y = x, matrix rows [0, 1] and [1, 0]. A vector on the mirror line stays put (eigenvalue 1);
a vector at 90 degrees to it is flipped (eigenvalue -1); any other vector leaves its line.
Tool: Plotly, a still chart of six 2D arrows. Example idea after Khan Academy, "Introduction to eigenvalues and
eigenvectors"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#9a9a9a"
M = np.array([[0, 1], [1, 0]])
CASES = [(np.array([2, 2]), GREEN, "on the mirror line:<br>[2, 2] → [2, 2], eigenvalue 1"),
         (np.array([1, -1]), GREEN, "at 90° to the mirror line:<br>[1, −1] → [−1, 1], eigenvalue −1"),
         (np.array([3, 1]), RED, "any other vector:<br>[3, 1] → [1, 3], off its line")]
assert (M @ [2, 2] == [2, 2]).all() and (M @ [1, -1] == [-1, 1]).all() and (M @ [3, 1] == [1, 3]).all()
assert np.allclose(sorted(np.linalg.eigvals(M)), [-1, 1])

fig = go.Figure()
fig.add_scatter(x=[-3.5, 3.5], y=[-3.5, 3.5], mode="lines", line=dict(color=GREY, width=2, dash="dash"))
fig.add_annotation(x=-2.6, y=-2.6, text="mirror line y = x", showarrow=False, xshift=95, font=dict(size=20, color="#6B6B6B"))
for v, col, _ in CASES:
    w = M @ v
    fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3, arrowwidth=3,
                       arrowcolor=col, opacity=0.45, text="")
    fig.add_annotation(x=w[0], y=w[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3, arrowwidth=5,
                       arrowcolor=col, text="")
fig.add_annotation(x=3.45, y=1.9, text=CASES[0][2], showarrow=False, font=dict(size=20, color="#2e7d32"))
fig.add_annotation(x=-1, y=1, text=CASES[1][2], showarrow=False, xshift=-150, yshift=34, font=dict(size=20, color="#2e7d32"))
fig.add_annotation(x=3, y=1, text=CASES[2][2], showarrow=False, xshift=40, yshift=-44, font=dict(size=20, color=RED))
fig.update_layout(template="simple_white", width=1000, height=820, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Reflection across y = x: pale arrows before, solid arrows after", x=0.5),
                  xaxis=dict(range=[-4.6, 4.6], zeroline=True, zerolinewidth=2, dtick=1),
                  yaxis=dict(range=[-3.6, 3.9], zeroline=True, zerolinewidth=2, dtick=1, scaleanchor="x"),
                  margin=dict(l=60, r=30, t=70, b=50))
fig.write_image(here / "reflection.png", scale=2)
