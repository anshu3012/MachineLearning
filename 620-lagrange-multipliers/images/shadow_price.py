"""The multiplier as a rate (Plotly): the best value f*(c) = 2c^2/3 of min x^2 + 2y^2 subject to x + y = c, against c.
Its tangent at c = 3 has slope 4 = lambda. Moving the line to c = 3.1 or 3.3 raises the best value to 6.41 or 7.26,
close to the straight-line estimates 6.4 and 7.2."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, RED

here = Path(__file__).parent
fs = lambda c: 2 * c ** 2 / 3
assert fs(3) == 6 and round(fs(3.1), 2) == 6.41 and round(fs(3.3), 2) == 7.26 and 4 * 3 / 3 == 4
c = np.linspace(2.6, 3.5, 200)
fig = go.Figure([go.Scatter(x=c, y=fs(c), mode="lines", line=dict(color=BLUE, width=4), name="best value f*(c) = 2c²/3"),
                 go.Scatter(x=c, y=6 + 4 * (c - 3), mode="lines", line=dict(color=ORANGE, width=3, dash="dash"),
                            name="tangent at c = 3: slope λ = 4")])
for cc in (3.1, 3.3):
    fig.add_scatter(x=[cc, cc], y=[6 + 4 * (cc - 3), fs(cc)], mode="lines+markers", line=dict(color=RED, width=3),
                    marker=dict(size=9), showlegend=False)
    fig.add_annotation(x=cc, y=fs(cc), text=f"c = {cc}: {fs(cc):.2f} (estimate {6 + 4 * (cc - 3):.1f})", ax=-170 if cc == 3.3 else 120,
                       ay=-40 if cc == 3.3 else 60, font=dict(size=18, color=RED), arrowcolor=RED)
fig.add_scatter(x=[3], y=[6], mode="markers", marker=dict(size=14, color="black"), showlegend=False)
fig.update_layout(template="simple_white", width=950, height=580, font=FONT,
                  xaxis=dict(title="the constraint x + y = c"), yaxis=dict(title="best value f*", range=[4.4, 8.3]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "shadow_price.png", scale=2)
