"""Squared error versus absolute error for one residual d (Plotly). The square counts large errors more (2 -> 4,
3 -> 9) and is smooth at 0; the absolute value has a sharp corner at 0, where it has no derivative."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
d = np.linspace(-3, 3, 601)
fig = go.Figure([go.Scatter(x=d, y=d ** 2, mode="lines", line=dict(color=ORANGE, width=5), name="squared error  d²"),
                 go.Scatter(x=d, y=np.abs(d), mode="lines", line=dict(color=BLUE, width=5), name="absolute error  |d|")])
for v in (1, 2, 3):
    fig.add_trace(go.Scatter(x=[v, v], y=[v, v * v], mode="markers+text", text=[f" {v}", f" {v * v}"],
                             textposition="middle right", textfont=dict(size=20),
                             marker=dict(size=11, color=[BLUE, ORANGE]), showlegend=False))
fig.add_annotation(x=0, y=0, ax=1.9, ay=0.9, axref="x", ayref="y", xanchor="left", text="sharp corner at 0:<br>|d| has no slope here", font=dict(size=20),
                   arrowcolor=BLUE, arrowwidth=2)
fig.update_layout(template="simple_white", width=900, height=560, font=FONT,
                  xaxis=dict(title="residual d = y − ŷ", range=[-3.2, 3.6], zeroline=True),
                  yaxis=dict(title="what the residual adds to the total", range=[-0.3, 9.6]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "square_vs_abs.png", scale=2)
