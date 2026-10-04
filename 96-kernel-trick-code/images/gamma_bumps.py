"""How far one point's influence reaches in the RBF kernel K = exp(-gamma * distance^2), for gamma = 0.1, 1
and 10 (section 8). At distance 1 the values are 0.90, 0.37 and 0.00005. (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
d = np.linspace(0, 3, 301)
fig = go.Figure()
for g, color in [(0.1, "#54A24B"), (1, "#4C78A8"), (10, "#E45756")]:
    k1 = np.exp(-g)
    fig.add_trace(go.Scatter(x=d, y=np.exp(-g * d ** 2), mode="lines", line=dict(color=color, width=4),
                             name=f"gamma = {g}:  K = {k1:.2f} at distance 1" if k1 > 0.005 else
                             f"gamma = {g}:  K = {k1:.5f} at distance 1"))
    fig.add_trace(go.Scatter(x=[1], y=[k1], mode="markers", showlegend=False,
                             marker=dict(size=14, color=color, line=dict(color="black", width=2))))
assert round(np.exp(-0.1), 2) == 0.90 and round(np.exp(-1), 2) == 0.37 and round(np.exp(-10), 5) == 0.00005
fig.add_vline(x=1, line=dict(color="#888888", dash="dot"))
fig.update_xaxes(title="distance between the two points")
fig.update_yaxes(title="kernel value K (influence)", range=[0, 1.05])
fig.update_layout(template="simple_white", width=1000, height=660, legend=dict(x=0.2, y=-0.22, yanchor="top", font_size=22),
                  font=dict(family="Latin Modern Roman", size=22, color="black"), margin=dict(l=80, r=20, t=20, b=190))
fig.write_image(HERE / "gamma_bumps.png", scale=2)
fig.write_image(HERE / "gamma_bumps.pdf")
