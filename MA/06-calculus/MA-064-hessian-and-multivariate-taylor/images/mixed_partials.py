"""Mixed partial derivatives agree (Plotly), for f(x, y) = x^3 + xy + y^2 near (1, 1). Left: the x-slope
df/dx = 3x^2 + y, watched as y moves with x = 1 fixed: it rises with slope 1. Right: the y-slope df/dy = x + 2y,
watched as x moves with y = 1 fixed: it also rises with slope 1. Both orders give the mixed derivative 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE

here = Path(__file__).parent
fx = lambda x, y: 3 * x ** 2 + y
fy = lambda x, y: x + 2 * y
h = 1e-6
assert round((fx(1, 1 + h) - fx(1, 1 - h)) / (2 * h), 6) == 1 == round((fy(1 + h, 1) - fy(1 - h, 1)) / (2 * h), 6)
t = np.linspace(0, 2, 101)
fig = make_subplots(1, 2, horizontal_spacing=0.12,
                    subplot_titles=["∂f/∂x = 3x² + y as y moves (x = 1)", "∂f/∂y = x + 2y as x moves (y = 1)"])
fig.update_annotations(font_size=21)
for col, vals, c, lab in ((1, fx(1, t), ORANGE, "slope 1: ∂²f/∂y∂x = 1"), (2, fy(t, 1), GREEN, "slope 1: ∂²f/∂x∂y = 1")):
    fig.add_trace(go.Scatter(x=t, y=vals, mode="lines", line=dict(color=c, width=4)), 1, col)
    base = vals[50]
    fig.add_trace(go.Scatter(x=[1, 1.5, 1.5], y=[base, base, base + 0.5], mode="lines", line=dict(color=BLUE, width=3, dash="dot")), 1, col)
    fig.add_annotation(x=1.5, y=base + 0.25, text=lab, showarrow=False, xanchor="left", xshift=8, font=dict(size=19, color=BLUE),
                       row=1, col=col)
    fig.add_trace(go.Scatter(x=[1], y=[base], mode="markers", marker=dict(size=13, color="black")), 1, col)
fig.update_xaxes(title="y", row=1, col=1)
fig.update_xaxes(title="x", row=1, col=2)
fig.update_yaxes(title="value of the first partial derivative", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=500, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "mixed_partials.png", scale=2)
