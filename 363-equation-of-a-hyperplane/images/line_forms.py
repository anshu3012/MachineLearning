"""One line, two forms: 2x1 + 3x2 - 6 = 0 is x2 = -(2/3) x1 + 2, slope -a/b = -0.67 and intercept -c/b = 2. Left: the
line with its slope triangle and intercept. Right: points that satisfy w.x + w0 = 0 lie on it; a point off it does not."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
w, w0 = np.array([2, 3.0]), -6.0
on = np.array([[3, 0], [0, 2], [1.5, 1]], float)
off = np.array([3, 2.0])
assert np.allclose(on @ w + w0, 0) and off @ w + w0 == 6
x = np.linspace(-1, 4.5, 50)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
    "2x₁ + 3x₂ − 6 = 0  is  x₂ = −(2/3)x₁ + 2", "w = [2, 3], w₀ = −6: plug in each point"])
for c in (1, 2):
    fig.add_scatter(x=x, y=-(2 / 3) * x + 2, mode="lines", line=dict(color="#4C78A8", width=4), row=1, col=c)
    fig.update_xaxes(range=[-1, 4.5], zeroline=True, title_text="x₁", row=1, col=c)
    fig.update_yaxes(range=[-1, 3.5], zeroline=True, title_text="x₂" if c == 1 else None, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
fig.add_scatter(x=[0, 1.5, 1.5], y=[2, 2, 1], mode="lines", line=dict(color="#F58518", width=3, dash="dash"), row=1, col=1)
fig.add_scatter(x=[0.75, 1.75, 0], y=[2.25, 1.5, 2], mode="text+markers", text=["run 1.5", "fall 1: slope −1/1.5 = −0.67", "intercept 2"],
                textposition=["top center", "middle right", "top left"], marker=dict(size=[0, 0, 12], color="#E45756"),
                textfont=dict(size=16), row=1, col=1)
for p in on:
    fig.add_scatter(x=[p[0]], y=[p[1]], mode="markers+text", marker=dict(size=13, color="#54A24B"),
                    text=[f"[{p[0]:g}, {p[1]:g}]: {w[0]:g}·{p[0]:g} + {w[1]:g}·{p[1]:g} − 6 = 0"], textposition="top right" if p[1] == 0 else "middle right",
                    textfont=dict(size=15, color="#2e7d32"), row=1, col=2)
fig.add_scatter(x=[off[0]], y=[off[1]], mode="markers+text", marker=dict(size=13, color="#E45756"),
                text=["[3, 2]: 6 + 6 − 6 = 6, not on the line"], textposition="top left", textfont=dict(size=15, color="#E45756"),
                row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1500, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=60, b=60))
fig.write_image(here / "line_forms.png", scale=2)
