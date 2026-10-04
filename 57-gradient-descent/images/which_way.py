"""Which way and how far (Plotly): the loss L(b) of the 4-point example (m fixed at 78.35). At four starting
values of b the tangent shows the slope; the arrow is the gradient descent step, minus 0.1 times the slope. Where
the slope is positive the arrow points left, where negative it points right, and steep slopes give long steps."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import loss_b, slope_b
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
LR = 0.1
assert round(slope_b(100), 1) == 590.7 and round(100 - LR * slope_b(100), 2) == 40.93
grid = np.linspace(-70, 120, 300)
fig = go.Figure(go.Scatter(x=grid, y=[loss_b(b) for b in grid], mode="lines", line=dict(color=BLUE, width=4),
                           name="loss L(b)"))
for b0 in (100, 60, -15, -50):
    s, L0 = slope_b(b0), loss_b(b0)
    c = ORANGE if s > 0 else RED
    tx = np.array([b0 - 12, b0 + 12])
    fig.add_scatter(x=tx, y=L0 + s * (tx - b0), mode="lines", line=dict(color="black", width=2), showlegend=False)
    nb = b0 - LR * s
    fig.add_annotation(x=nb, y=L0, ax=b0, ay=L0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3, arrowsize=1.4,
                       arrowwidth=4, arrowcolor=c, showarrow=True)
    fig.add_scatter(x=[b0], y=[L0], mode="markers", marker=dict(size=14, color=c), showlegend=False)
    fig.add_annotation(x=b0, y=L0, yshift=48, showarrow=False, font=dict(size=19, color=c),
                       text=f"slope {s:+.0f}<br>step {-LR * s:+.1f}")
bstar = 26.16
fig.add_scatter(x=[bstar], y=[loss_b(bstar)], mode="markers", marker=dict(size=14, color=GREEN, symbol="star"),
                name="the bottom, b = 26.16")
fig.add_scatter(x=[None], y=[None], mode="lines", line=dict(color=ORANGE, width=4), name="slope > 0: step left")
fig.add_scatter(x=[None], y=[None], mode="lines", line=dict(color=RED, width=4), name="slope < 0: step right")
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  xaxis=dict(title="intercept b"), yaxis=dict(title="loss L(b)", range=[-2000, 1.15 * loss_b(-70)]),
                  legend=dict(x=0.35, y=0.98), margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "which_way.png", scale=2)
