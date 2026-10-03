"""The mixture density of MML Figure 11.2: three weighted normal components (dashed) and their sum (black)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import COLS, FONT, MU, PI, VAR, components, mixture

HERE = Path(__file__).parent
g = np.linspace(-5, 8, 500)
comp = components(g)
fig = go.Figure()
for k in range(3):
    fig.add_trace(go.Scatter(x=g, y=comp[:, k], mode="lines", line=dict(color=COLS[k], width=3, dash="dash"),
                             name=f"{PI[k]} × N(x | {MU[k]:g}, {VAR[k]:g})"))
fig.add_trace(go.Scatter(x=g, y=mixture(g), mode="lines", line=dict(color="black", width=4), name="mixture p(x)"))
fig.add_trace(go.Scatter(x=[0], y=[mixture([0])[0]], mode="markers", marker=dict(size=12, color="black"),
                         showlegend=False))
fig.add_annotation(x=0, y=mixture([0])[0], text=f"p(0) = {mixture([0])[0]:.3f}", ax=-10, ay=-80, bgcolor="white")
fig.update_layout(template="simple_white", width=1000, height=500, font=FONT, xaxis=dict(title="x"),
                  yaxis=dict(title="density", range=[0, 0.32]), legend=dict(x=0.62, y=0.98),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(HERE / "mixture_density.png", scale=2)
fig.write_image(HERE / "mixture_density.pdf")
