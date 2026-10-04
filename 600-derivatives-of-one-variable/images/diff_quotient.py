"""The difference quotient as rise over run (Plotly): f(x) = x^2 between x = 1 and x = 2. The secant line has slope
(4 - 1) / 1 = 3, the average slope over the step. The tangent slopes at the two ends are 2 and 4: the curve is
flatter than 3 at the start and steeper at the end."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED

here = Path(__file__).parent
f = lambda x: x ** 2
assert (f(2) - f(1)) / 1 == 3
xs = np.linspace(0, 2.6, 300)
fig = go.Figure(go.Scatter(x=xs, y=f(xs), mode="lines", line=dict(color=BLUE, width=4), name="f(x) = x²"))
s = np.array([0.3, 2.5])
fig.add_scatter(x=s, y=1 + 3 * (s - 1), mode="lines", line=dict(color=ORANGE, width=4), name="secant line: slope 3")
for x0, slope in ((1, 2), (2, 4)):
    t = np.array([x0 - 0.45, x0 + 0.45])
    fig.add_scatter(x=t, y=f(x0) + slope * (t - x0), mode="lines", line=dict(color=GREEN, width=3, dash="dash"),
                    name="tangent slopes 2 and 4", showlegend=x0 == 1)
fig.add_scatter(x=[1, 2, 2], y=[1, 1, 4], mode="lines", line=dict(color=RED, width=3), showlegend=False)
fig.add_annotation(x=1.5, y=1, text="run h = 1", showarrow=False, yshift=-18, font=dict(size=20, color=RED))
fig.add_annotation(x=2, y=2.5, text="rise f(2) − f(1) = 3", showarrow=False, xanchor="left", xshift=8,
                   font=dict(size=20, color=RED))
fig.add_scatter(x=[1, 2], y=[1, 4], mode="markers+text", text=["(1, 1)", "(2, 4)"], textposition="middle left",
                textfont=dict(size=18), marker=dict(size=13, color="black"), showlegend=False)
fig.update_layout(template="simple_white", width=900, height=620, font=FONT,
                  xaxis=dict(title="x", range=[0, 2.7]), yaxis=dict(title="f(x)", range=[-0.5, 7]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "diff_quotient.png", scale=2)
