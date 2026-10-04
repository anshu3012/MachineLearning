"""The slope formula on the 4-point example at b = 100, m = 78.35 (Plotly). Left: the line and each point's residual
y - m x - b as a stick. Right: the four residuals added up, times -2, give the slope 590.7."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import M4, slope_b, x4, y4
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
B = 100
o = np.argsort(x4)
xo, yo = x4[o], y4[o]
r = yo - M4 * xo - B
assert round(-2 * r.sum(), 1) == round(slope_b(B), 1) == 590.7
fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                    subplot_titles=["the line at b = 100: every point lies below it", "∂L/∂b = −2 × (sum of residuals)"])
fig.update_annotations(font_size=22)
xs = np.array([x4.min() - 0.4, x4.max() + 0.4])
fig.add_trace(go.Scatter(x=xs, y=M4 * xs + B, mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
for xi, yi, ri in zip(xo, yo, r):
    fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, yi - ri], mode="lines", line=dict(color=RED, width=4)), 1, 1)
    fig.add_annotation(x=xi, y=yi - ri / 2, text=f"point {list(xo).index(xi) + 1}: {ri:.1f}", xshift=-80 if list(xo).index(xi) == 1 else 70, showarrow=False, font=dict(size=20, color=RED),
                       row=1, col=1)
fig.add_trace(go.Scatter(x=x4, y=y4, mode="markers", marker=dict(size=14, color=GREY)), 1, 1)
labels = [f"point {i + 1}" for i in range(4)] + ["sum", "× (−2)"]
vals = list(r) + [r.sum(), -2 * r.sum()]
fig.add_trace(go.Bar(x=labels, y=vals, marker_color=[RED] * 4 + ["#9D755D", BLUE],
                     text=[f"{v:.1f}" for v in vals], textposition="outside", textfont=dict(size=18)), 1, 2)
fig.update_xaxes(title="x", row=1, col=1)
fig.update_yaxes(title="y", row=1, col=1)
fig.update_yaxes(range=[min(vals) * 1.25, max(vals) * 1.2], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=560, font=FONT, showlegend=False,
                  margin=dict(l=70, r=30, t=60, b=70))
fig.write_image(here / "slope_b_worked.png", scale=2)
