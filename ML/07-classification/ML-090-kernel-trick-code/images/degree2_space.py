"""Section 6: the circles data drawn in the degree-2 features (x1^2, x2^2). The circle x1^2 + x2^2 = r^2 becomes
the straight line u + v = r^2, so a linear boundary separates the classes there. A degree-3 kernel with coef0 = 0
has only degree-3 terms, so it cannot form x1^2 + x2^2.
Run: python degree2_space.py  -> degree2_space.png (Plotly)"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, make_data  # noqa: E402

X, y = make_data("circles")
r2 = (X ** 2).sum(axis=1)
cut = (r2[y == 1].max() + r2[y == 0].min()) / 2                   # a line u + v = cut between the classes
assert r2[y == 1].max() < cut < r2[y == 0].min()
print("inner max r^2", r2[y == 1].max().round(3), "ring min r^2", r2[y == 0].min().round(3), "cut", cut.round(3))

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("original features: a circle", "squared features: a straight line"))
for cls, name in ((0, "ring (class 0)"), (1, "centre (class 1)")):
    m = y == cls
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name,
                             marker=dict(color=COLOURS[cls], size=9)), 1, 1)
    fig.add_trace(go.Scatter(x=X[m, 0] ** 2, y=X[m, 1] ** 2, mode="markers", showlegend=False,
                             marker=dict(color=COLOURS[cls], size=9)), 1, 2)
th = np.linspace(0, 2 * np.pi, 200)
fig.add_trace(go.Scatter(x=np.sqrt(cut) * np.cos(th), y=np.sqrt(cut) * np.sin(th), mode="lines",
                         name=f"x₁² + x₂² = {cut:.2f}", line=dict(color="#54A24B", width=4, dash="dash")), 1, 1)
fig.add_trace(go.Scatter(x=[0, cut], y=[cut, 0], mode="lines", showlegend=False,
                         line=dict(color="#54A24B", width=4, dash="dash")), 1, 2)
fig.update_xaxes(title="x₁", range=[-1.4, 1.4], col=1)
fig.update_yaxes(title="x₂", range=[-1.4, 1.4], scaleanchor="x", col=1)
fig.update_xaxes(title="x₁²", range=[-0.05, 1.6], col=2)
fig.update_yaxes(title="x₂²", range=[-0.05, 1.6], scaleanchor="x2", col=2)
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=60, r=20, t=50, b=120), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.update_annotations(font_size=22)
fig.write_image(HERE / "degree2_space.png", scale=2)
fig.write_image(HERE / "degree2_space.pdf")
