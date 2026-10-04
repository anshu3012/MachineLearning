"""Penalty shapes for two coefficients: the set where each penalty equals 1 (Plotly).
Ridge: w1² + w2²; Lasso: |w1| + |w2|; Elastic Net (l1_ratio 0.5): 0.5(|w1| + |w2|) + 0.5(w1² + w2²)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import brentq

here = Path(__file__).parent
t = np.linspace(0, 2 * np.pi, 721)
d = np.c_[np.cos(t), np.sin(t)]


def boundary(pen):
    r = np.array([brentq(lambda s: pen(s * v) - 1, 1e-9, 10) for v in d])
    return d * r[:, None]


shapes = [("Ridge (L2): w₁² + w₂² = 1", lambda w: (w ** 2).sum(), "#4C78A8"),
          ("Lasso (L1): |w₁| + |w₂| = 1", lambda w: np.abs(w).sum(), "#E45756"),
          ("Elastic Net: ½(|w₁| + |w₂|) + ½(w₁² + w₂²) = 1", lambda w: 0.5 * np.abs(w).sum() + 0.5 * (w ** 2).sum(), "#54A24B")]
fig = go.Figure()
for name, pen, col in shapes:
    b = boundary(pen)
    fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="lines", line=dict(color=col, width=5), name=name))
fig.add_trace(go.Scatter(x=[0, 1, 0, -1], y=[1, 0, -1, 0], mode="markers", marker=dict(size=10, color="#E45756"),
                         showlegend=False))
fig.add_annotation(x=0.08, y=1.12, text="sharp corners on the axes: coefficients can be exactly 0", showarrow=False,
                   xanchor="left", font=dict(color="#E45756", size=15))
fig.update_layout(template="simple_white", width=1250, height=620, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=60, r=30, t=30, b=60), legend=dict(x=1.02, y=0.5, yanchor="middle"),
                  xaxis=dict(title="w₁", range=[-1.3, 1.3], zeroline=True, zerolinecolor="#BBBBBB"),
                  yaxis=dict(title="w₂", range=[-1.25, 1.25], scaleanchor="x", zeroline=True, zerolinecolor="#BBBBBB"))
fig.write_image(here / "shapes.png", scale=2)
fig.write_image(here / "shapes.pdf")
