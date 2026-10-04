"""Gradient checking and the step size h (Plotly), on the Note's three-point squared-error loss at m = 1, b = 0
(true gradient [-22, -10]). Relative error of the one-sided and central differences against h. The one-sided
error shrinks in proportion to h; the central difference is exact for this quadratic loss, so only rounding error
is left, which grows as h becomes tiny. At h = 1e-4 the central relative error is about 2.5e-13."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
x, y = np.array([1.0, 2.0, 3.0]), np.array([2.0, 4.0, 5.0])
loss = lambda p: np.sum((y - p[0] * x - p[1]) ** 2)
p = np.array([1.0, 0.0])
true = np.array([-22.0, -10.0])
rel = lambda num: np.linalg.norm(num - true) / np.linalg.norm(num + true)
hs = np.logspace(-12, 0, 49)
fwd = [rel(np.array([(loss(p + h * e) - loss(p)) / h for e in np.eye(2)])) for h in hs]
cen = [rel(np.array([(loss(p + h * e) - loss(p - h * e)) / (2 * h) for e in np.eye(2)])) for h in hs]
c4 = rel(np.array([(loss(p + 1e-4 * e) - loss(p - 1e-4 * e)) / 2e-4 for e in np.eye(2)]))
assert 1e-14 < c4 < 1e-12, c4
floor = 1e-17
fig = go.Figure([go.Scatter(x=hs, y=np.maximum(fwd, floor), mode="lines+markers", name="one-sided difference",
                            line=dict(color=ORANGE, width=3)),
                 go.Scatter(x=hs, y=np.maximum(cen, floor), mode="lines+markers", name="central difference",
                            line=dict(color=BLUE, width=3))])
fig.add_hline(y=1e-6, line=dict(color=GREY, dash="dash", width=2), opacity=1)
fig.add_annotation(x=0, y=-6, xref="x", yref="y", text="10⁻⁶: formula very probably correct", showarrow=False,
                   xanchor="right", yshift=14, font=dict(size=18, color=GREY))
fig.add_annotation(x=-4, y=np.log10(c4), text=f"h = 10⁻⁴: {c4:.1e}", ax=70, ay=-50, font=dict(size=18, color=BLUE),
                   arrowcolor=BLUE)
fig.update_layout(template="simple_white", width=1000, height=580, font=FONT,
                  xaxis=dict(title="step h (log scale)", type="log", exponentformat="power", dtick=2),
                  yaxis=dict(title="relative error (log scale)", type="log", range=[-17.2, 1], exponentformat="power", dtick=2),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "gradcheck_h.png", scale=2)
