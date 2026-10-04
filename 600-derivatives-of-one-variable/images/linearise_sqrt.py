"""Linearisation (Plotly): sqrt(x) and its tangent line at x0 = 4, T1(x) = 2 + 0.25 (x - 4). At x = 4.1 the line gives
2.025 (true 2.0248); at x = 5 it gives 2.25 (true 2.2361): the gap grows with the distance from x0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, RED

here = Path(__file__).parent
T1 = lambda x: 2 + 0.25 * (x - 4)
assert (round(T1(4.1), 3), round(np.sqrt(4.1), 4), T1(5), round(np.sqrt(5), 4)) == (2.025, 2.0248, 2.25, 2.2361)
xs = np.linspace(1, 9, 400)
fig = go.Figure([go.Scatter(x=xs, y=np.sqrt(xs), mode="lines", line=dict(color=BLUE, width=4), name="f(x) = √x"),
                 go.Scatter(x=xs, y=T1(xs), mode="lines", line=dict(color=ORANGE, width=3), name="tangent line T₁ at x₀ = 4")])
fig.add_scatter(x=[4], y=[2], mode="markers", marker=dict(size=14, color="black"), showlegend=False)
for x in (4.1, 5, 8):
    fig.add_scatter(x=[x, x], y=[np.sqrt(x), T1(x)], mode="lines+markers", line=dict(color=RED, width=3),
                    marker=dict(size=8, color=RED), showlegend=False)
fig.add_annotation(x=0.98, y=0.04, xref="paper", yref="paper", xanchor="right", yanchor="bottom", showarrow=False,
                   align="left", font=dict(size=19, color=RED), bgcolor="white",
                   text="<br>".join(f"x = {x}: line {T1(x):.4f}, √x {np.sqrt(x):.4f}, gap {T1(x) - np.sqrt(x):.4f}"
                                    for x in (4.1, 5, 8)))
fig.update_layout(template="simple_white", width=950, height=560, font=FONT,
                  xaxis=dict(title="x", range=[1, 9.8]), yaxis=dict(title="y", range=[0.8, 3.4]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "linearise_sqrt.png", scale=2)
