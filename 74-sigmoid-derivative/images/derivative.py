"""The sigmoid and its derivative σ'(z) = σ(z)(1 − σ(z)) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
sig = lambda z: 1 / (1 + np.exp(-z))
z = np.linspace(-8, 8, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=z, y=sig(z), mode="lines", line=dict(color="#4C78A8", width=4), name="σ(z)"))
fig.add_trace(go.Scatter(x=z, y=sig(z) * (1 - sig(z)), mode="lines", line=dict(color="#E45756", width=4), name="σ′(z) = σ(z)(1 − σ(z))"))
for v in (0, 2, -4):
    d = sig(v) * (1 - sig(v))
    fig.add_trace(go.Scatter(x=[v], y=[d], mode="markers+text", marker=dict(size=11, color="#E45756"),
                             text=[f"z = {v}: {sig(v):.2f} × {1 - sig(v):.2f} = {d:.3f}".replace("-", "−")],
                             textposition="top right" if v != -4 else "top left", textfont=dict(color="#E45756", size=14), showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=470, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=60, r=20, t=30, b=60), legend=dict(x=0.01, y=0.98),
                  xaxis=dict(title="z"), yaxis=dict(title="value", range=[-0.03, 1.05]))
fig.write_image(here / "derivative.png", scale=2); fig.write_image(here / "derivative.pdf")
