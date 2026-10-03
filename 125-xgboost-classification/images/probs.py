"""Five students on the CGPA axis: placed (1) or not (0); predicted probability at stage 1 (0.6) and stage 2, Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=23)
x = np.array([5.70, 6.25, 7.10, 8.15, 9.60])
y = np.array([0, 1, 0, 1, 1])
z0 = np.log(3 / 2)
sig = lambda z: 1 / (1 + np.exp(-z))
tree = lambda v: np.where(v < 7.625, -0.8 / 0.72, 0.8 / 0.48)
grid = np.linspace(5.3, 10.0, 1000)
p2 = sig(z0 + 0.3 * tree(x))
print("p2", p2.round(4), "res2", (y - p2).round(4))

fig = go.Figure()
fig.add_trace(go.Scatter(x=grid, y=np.full_like(grid, sig(z0)), mode="lines", name="stage 1: p = 0.6",
                         line=dict(color="#6B6B6B", width=3, dash="dash")))
fig.add_trace(go.Scatter(x=grid, y=sig(z0 + 0.3 * tree(grid)), mode="lines", name="stage 2",
                         line=dict(color="#E45756", width=3, shape="hv")))
for c, name, colour in [(0, "not placed (0)", "#F58518"), (1, "placed (1)", "#4C78A8")]:
    m = y == c
    fig.add_trace(go.Scatter(x=x[m], y=y[m], mode="markers", name=name, marker=dict(color=colour, size=14)))
for xi, pi in zip(x, p2):
    fig.add_annotation(x=xi, y=pi, text=f"{pi:.3f}", showarrow=False, yshift=16, font=dict(size=20, color="#E45756"))
fig.add_vline(x=7.625, line=dict(color="#54A24B", width=2.5, dash="dot"), opacity=1)
fig.add_annotation(x=7.625, y=0.25, text="split: CGPA < 7.625", showarrow=False, xanchor="left", xshift=6,
                   font=dict(size=20, color="#54A24B"))
fig.add_hline(y=0.5, line=dict(color="#6B6B6B", width=1))
fig.update_xaxes(title="CGPA", range=[5.3, 10.0])
fig.update_yaxes(title="probability of placement", range=[-0.08, 1.08], dtick=0.2)
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=80, r=20, t=20, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(HERE / "probs.png", scale=2)
fig.write_image(HERE / "probs.pdf")
