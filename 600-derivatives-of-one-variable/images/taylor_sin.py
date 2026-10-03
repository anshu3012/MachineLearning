"""Taylor polynomials of sin(x) around x0 = 0 (Plotly): T1 = x, T3, T5 and T9. Higher degree follows the curve
over a wider range. Also writes .pdf for the PDF build."""
from math import factorial
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
x = np.linspace(-6, 6, 600)


def T(n, x):
    # only odd powers survive: sin, cos, -sin, -cos repeat, and sin(0) = 0
    return sum((-1) ** (k // 2) * x ** k / factorial(k) for k in range(1, n + 1, 2))


assert abs(T(5, 0.5) - 0.479427) < 1e-6
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=np.sin(x), name="sin x", line=dict(color="black", width=4)))
for n, c in ((1, ORANGE), (3, GREEN), (5, RED), (9, PURPLE)):
    fig.add_trace(go.Scatter(x=x, y=T(n, x), name=f"T{n}", line=dict(color=c, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=11, color=BLUE), showlegend=False))
fig.update_xaxes(title="x", range=[-6, 6], zeroline=True, zerolinecolor="#DDDDDD")
fig.update_yaxes(title="y", range=[-2.2, 2.2], zeroline=True, zerolinecolor="#DDDDDD")
fig.update_layout(template="simple_white", width=900, height=430, font=dict(family="Latin Modern Roman", size=17),
                  legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), margin=dict(l=60, r=20, t=40, b=55))
fig.write_image(here / "taylor_sin.png", scale=2)
fig.write_image(here / "taylor_sin.pdf")
