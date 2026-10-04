"""The error E(m, b) = sum of squared errors on the 160 training students, as a surface and as two slices (Plotly).
The minimum is where the slope of E is zero in both directions."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import X_train, y_train, M, B

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
E = lambda m, b: ((y - (m[..., None] * x + b[..., None])) ** 2).sum(-1)
ms, bs = np.linspace(M - 0.15, M + 0.15, 80), np.linspace(B - 1.0, B + 1.0, 80)
MM, BB = np.meshgrid(ms, bs)
Z = E(MM, BB)
emin = float(((y - (M * x + B)) ** 2).sum())
fig = make_subplots(1, 3, specs=[[{"type": "scene"}, {}, {}]], column_widths=[0.46, 0.27, 0.27],
                    horizontal_spacing=0.06,
                    subplot_titles=("E(m, b): a bowl", f"Slice with b = {B:.2f}", f"Slice with m = {M:.3f}"))
fig.add_trace(go.Surface(x=MM, y=BB, z=Z, colorscale="Blues", reversescale=True, showscale=False, opacity=0.9), 1, 1)
fig.add_trace(go.Scatter3d(x=[M], y=[B], z=[emin], mode="markers", marker=dict(size=6, color=ORANGE)), 1, 1)
e_m = E(ms, np.full_like(ms, B))
e_b = E(np.full_like(bs, M), bs)
fig.add_trace(go.Scatter(x=ms, y=e_m, mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
fig.add_trace(go.Scatter(x=bs, y=e_b, mode="lines", line=dict(color=BLUE, width=4)), 1, 3)
for col, xv in ((2, M), (3, B)):
    fig.add_trace(go.Scatter(x=[xv], y=[emin], mode="markers", marker=dict(size=11, color=ORANGE)), 1, col)
    span = 0.05 if col == 2 else 0.35
    fig.add_trace(go.Scatter(x=[xv - span, xv + span], y=[emin, emin], mode="lines",
                             line=dict(color=ORANGE, width=3, dash="dash")), 1, col)
fig.add_annotation(x=M, y=emin, xref="x", yref="y", yshift=-22, text="slope 0", showarrow=False,
                   font=dict(color=ORANGE, size=15))
fig.add_annotation(x=B, y=emin, xref="x2", yref="y2", yshift=-22, text="slope 0", showarrow=False,
                   font=dict(color=ORANGE, size=15))
fig.update_xaxes(title="m (slope)", row=1, col=2)
fig.update_xaxes(title="b (intercept)", row=1, col=3)
fig.update_yaxes(title="E", row=1, col=2)
fig.update_scenes(xaxis_title="m", yaxis_title="b", zaxis_title="E", camera=dict(eye=dict(x=1.7, y=-1.5, z=0.7)), xaxis=dict(nticks=4), yaxis=dict(nticks=4), zaxis=dict(nticks=4))
fig.update_layout(template="simple_white", width=1150, height=470, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=10, r=20, t=50, b=50))
fig.update_annotations(font_size=16, selector=dict(xref="paper"))
print("minimum E", round(emin, 2))
fig.write_image(here / "loss_surface.png", scale=2)
fig.write_image(here / "loss_surface.pdf")
