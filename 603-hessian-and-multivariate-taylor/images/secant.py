"""The secant idea behind BFGS, in one variable: for f = x^3 the slope f'(x) = 3x^2 is read at x = 1 (3) and x = 2 (12).
The line through the two readings has slope 9: a stand-in for the curvature f'' without computing it.
The true curvatures are the tangent slopes 6 and 12 (dashed)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
x = np.linspace(0.4, 2.4, 100)
B = (3 * 2 ** 2 - 3 * 1 ** 2) / (2 - 1)
assert B == 9
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=3 * x ** 2, mode="lines", name="slope of f: f'(x) = 3x²", line=dict(color=BLUE, width=4)))
xs = np.array([0.6, 2.4])
fig.add_trace(go.Scatter(x=xs, y=3 + B * (xs - 1), mode="lines", name="secant: slope (12 − 3)/(2 − 1) = 9",
                         line=dict(color=ORANGE, width=4)))
for x0, s in ((1, 6), (2, 12)):
    xt = np.array([x0 - 0.45, x0 + 0.45])
    fig.add_trace(go.Scatter(x=xt, y=3 * x0 ** 2 + s * (xt - x0), mode="lines", name=f"true curvature f''({x0}) = {s}",
                             line=dict(color=GREEN if x0 == 1 else GREY, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 12], mode="markers+text", text=["f'(1) = 3", "f'(2) = 12"],
                         textposition=["bottom right", "top left"], marker=dict(size=13, color="black"),
                         showlegend=False))
fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="x", range=[0.4, 2.4]), yaxis=dict(title="f'(x)", range=[-2, 18]),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(here / "secant.png", scale=2)
fig.write_image(here / "secant.pdf")
