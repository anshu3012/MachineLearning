"""Alpha = 1/2 ln((1 - error) / error) against the error, with three example models (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
e = np.linspace(0.005, 0.995, 400)
alpha = 0.5 * np.log((1 - e) / e)
fig = go.Figure(go.Scatter(x=e, y=alpha, mode="lines", line=dict(color="#4C78A8", width=3), showlegend=False))
pts = [(0.02, "A: almost always right", "top right"), (0.4, "our stump: error 0.4, alpha 0.20", "top right"),
       (0.5, "C: right half the time", "bottom left"), (0.98, "B: almost always wrong", "bottom left")]
for x, label, pos in pts:
    y = 0.5 * np.log((1 - x) / x)
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[label], textposition=pos, showlegend=False,
                             marker=dict(color="#E45756" if x == 0.4 else "#F58518", size=12),
                             textfont=dict(size=19)))
    print(label, round(y, 4))
fig.add_hline(y=0, line=dict(color="#6B6B6B", width=1, dash="dash"))
fig.update_xaxes(title="error", range=[0, 1], dtick=0.1)
fig.update_yaxes(title="alpha (the model's say)", range=[-2.6, 2.6])
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(HERE / "alpha_curve.png", scale=2)
fig.write_image(HERE / "alpha_curve.pdf")
