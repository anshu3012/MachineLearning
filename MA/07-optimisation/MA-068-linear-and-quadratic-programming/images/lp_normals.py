"""The dual condition of the workshop LP as arrows (Plotly). At the best corner (3, 1) two constraints are active,
oven (normal [1, 1]) and demand (normal [1, 0]). The profit direction -c = [3, 2] is 2 x [1, 1] + 1 x [1, 0]: a
combination of the active normals with non-negative weights, the multipliers lambda = 2 and 1 of the Note."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
c = np.array([-3, -2]); n_oven, n_dem = np.array([1, 1]), np.array([1, 0])
assert np.allclose(-c, 2 * n_oven + 1 * n_dem)
corners = [(0, 0), (3, 0), (3, 1), (1.5, 2.5), (0, 3), (0, 0)]
fig = go.Figure(go.Scatter(x=[p[0] for p in corners], y=[p[1] for p in corners], fill="toself",
                           fillcolor="rgba(76,120,168,0.18)", line=dict(color=BLUE, width=2), name="feasible region"))
P = np.array([3, 1])


def arrow(start, vec, color, text, shift):
    end = start + vec
    fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1], xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                       arrowsize=1.3, arrowwidth=4, arrowcolor=color)
    mid = start + vec / 2
    fig.add_annotation(x=mid[0], y=mid[1], text=text, showarrow=False, font=dict(size=19, color=color), xshift=shift[0],
                       yshift=shift[1], bgcolor="white")


arrow(P, 2 * n_oven, ORANGE, "2 × oven normal [1, 1]", (-95, 20))
arrow(P + 2 * n_oven, n_dem, GREEN, "+ 1 × demand normal [1, 0]", (40, 22))
arrow(P, -c, RED, "profit direction −c = [3, 2]", (95, -22))
for x0, x1, y0, y1 in ((0, 5, 4, -1), (3, 3, -0.5, 4)):
    fig.add_scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color="black", width=2, dash="dot"), showlegend=False)
fig.add_annotation(x=0.7, y=3.45, text="oven: x₁ + x₂ = 4", showarrow=False, font=dict(size=17))
fig.add_annotation(x=3, y=3.8, text="demand: x₁ = 3", showarrow=False, xanchor="left", xshift=6, font=dict(size=17))
fig.add_scatter(x=[3], y=[1], mode="markers", marker=dict(size=15, color="black"), name="best corner (3, 1)")
fig.update_layout(template="simple_white", width=950, height=720, font=FONT,
                  xaxis=dict(title="x₁ (batches of A)", range=[-0.3, 7.5]), yaxis=dict(title="x₂ (batches of B)", range=[-0.6, 4.2], scaleanchor="x"),
                  legend=dict(x=0.62, y=0.98), margin=dict(l=70, r=20, t=20, b=70))
fig.write_image(here / "lp_normals.png", scale=2)
