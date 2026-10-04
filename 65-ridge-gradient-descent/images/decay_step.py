"""One Ridge gradient step split in two (lambda = 100, learning rate 0.005, start m = -5, b = 20):
first shrink the slope by 1 - eta * lambda = 0.5, then take the plain least-squares step (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from ridge_race import X, y, x, ms, bs, Z, paths, GREY, ORANGE, RED, BLUE

here = Path(__file__).parent
eta, lam = 0.005, 100
m0, b0 = -5.0, 20.0
m1 = (1 - eta * lam) * m0                                        # shrink: intercept untouched
err = y - m0 * x - b0
m2, b2 = m1 + eta * (err * x).sum(), b0 + eta * err.sum()       # least-squares step, gradient taken at the old point
assert np.allclose([m2, b2], paths[100][1])                      # the two parts add up to the Ridge step
print(f"shrink to m = {m1}, then LS step to ({m2:.1f}, {b2:.1f})")
fig = go.Figure(go.Contour(x=ms, y=bs, z=Z, showscale=False, colorscale="Greys", reversescale=True, opacity=0.8,
                           contours=dict(coloring="lines", size=0.25), line=dict(width=1)))
for (xa, ya, xb, yb, c, t, pos) in ((m0, b0, m1, b0, RED, f"1. shrink: m × {1 - eta * lam:.1f}", "top center"),
                                    (m1, b0, m2, b2, BLUE, "2. least-squares step", "middle right")):
    fig.add_annotation(x=xb, y=yb, ax=xa, ay=ya, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor=c)
    fig.add_trace(go.Scatter(x=[(xa + xb) / 2], y=[(ya + yb) / 2 + (1.5 if c == RED else 3)], mode="text", text=[t],
                             textposition=pos, textfont=dict(size=20, color=c)))
fig.add_trace(go.Scatter(x=[m0, m2], y=[b0, b2], mode="markers+text", text=["old w", "new w"],
                         textposition=["middle left", "middle right"], marker=dict(size=12, color="black")))
fig.update_layout(template="simple_white", width=900, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=30, b=60),
                  xaxis=dict(title="slope m", range=[-10, 35]), yaxis=dict(title="intercept b", range=[-15, 25]))
fig.write_image(here / "decay_step.png", scale=2)
fig.write_image(here / "decay_step.pdf")
