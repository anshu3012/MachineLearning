"""A Gaussian alone as the model of one beam: wall expected at 3 m, sigma = 0.05 m. A person 1 m ahead gives
the reading 1.00 m, where the density is about e^-800 (0 in a computer). Run -> gaussian_fails.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import ZSTAR, SIG_HIT, gauss
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
z = np.linspace(0, 5, 4001)
fig = go.Figure(go.Scatter(x=z, y=gauss(z, ZSTAR, SIG_HIT), mode="lines", line=dict(color=BLUE, width=3)))
fig.add_trace(go.Scatter(x=[1.0], y=[0], mode="markers", marker=dict(size=16, color=RED, symbol="x")))
fig.add_annotation(x=1.0, y=0.3, ax=0, ay=-90, text="reading 1.00 m (person)<br>density ≈ e<sup>−800</sup> ≈ 0",
                   font=dict(color=RED, size=20), arrowcolor=RED, arrowwidth=2)
fig.add_annotation(x=3.0, y=8.0, xanchor="left", ax=60, ay=0, text="expected range z* = 3 m<br>σ = 0.05 m, peak 7.98 per m",
                   font=dict(color=BLUE, size=20), arrowcolor=BLUE, arrowwidth=2, showarrow=True)
fig.update_layout(template="simple_white", width=900, height=500, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=30, b=70))
fig.update_xaxes(title="reading z (m)", range=[0, 5.05], dtick=1)
fig.update_yaxes(title="density (per m)", range=[0, 9])
fig.write_image(here / "gaussian_fails.png", scale=1)
assert gauss(1.0, ZSTAR, SIG_HIT) == 0.0
