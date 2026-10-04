"""The dual function of the quadratic program along the edge multiplier lambda (the sign-constraint multipliers held
at 0) (Plotly): D(lambda) = -1/2 (c + a lambda)^T Q^-1 (c + a lambda) - 2 lambda with a = [1, 1]. It is a concave
curve below the primal minimum -12.25 and touches it at lambda = 4.5."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
Q, c, a = np.array([[2.0, 1], [1, 2]]), np.array([-8.0, -7]), np.array([1.0, 1])
Qi = np.linalg.inv(Q)
D = lambda l: -0.5 * (c + a * l) @ Qi @ (c + a * l) - 2 * l
ls = np.linspace(0, 9, 300)
vals = np.array([D(l) for l in ls])
assert np.isclose(D(4.5), -12.25) and abs(ls[np.argmax(vals)] - 4.5) < 0.02 and vals.max() <= -12.25 + 1e-9
fig = go.Figure([go.Scatter(x=ls, y=vals, mode="lines", line=dict(color=BLUE, width=4), name="dual function D(λ)"),
                 go.Scatter(x=[0, 9], y=[-12.25, -12.25], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                            name="primal minimum −12.25")])
fig.add_scatter(x=[4.5], y=[-12.25], mode="markers+text", text=["λ = 4.5: D = −12.25"], textposition="top center",
                textfont=dict(size=19, color=ORANGE), marker=dict(size=14, color=ORANGE), showlegend=False)
fig.add_scatter(x=[0], y=[D(0)], mode="markers+text", text=[f"λ = 0: D = {D(0):.2f}"], textposition="middle right",
                textfont=dict(size=17), marker=dict(size=10, color=BLUE), showlegend=False)
fig.update_layout(template="simple_white", width=950, height=540, font=FONT,
                  xaxis=dict(title="multiplier λ of the edge x₁ + x₂ ≤ 2"), yaxis=dict(title="value"),
                  legend=dict(x=0.55, y=0.2), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "qp_dual.png", scale=2)
