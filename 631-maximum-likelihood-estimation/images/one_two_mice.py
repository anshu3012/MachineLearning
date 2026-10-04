"""One mouse, then two (Plotly). Left: one mouse at 32 grams under normal curves with sigma = 2 and means 28, 30, 32:
heights 0.027, 0.121, 0.199, highest for the curve centred on the mouse. Right: two mice at 32 and 34; under mean 28
the two heights 0.027 and 0.0022 multiply to 6.0e-5, under mean 33 (their average) to 0.031."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda x, m: stats.norm(m, 2).pdf(x)
assert np.allclose([f(32, 28), f(32, 30), f(32, 32)], [0.027, 0.121, 0.199], atol=5e-4)
assert abs(f(34, 28) - 0.0022) < 1e-4 and abs(f(32, 28) * f(34, 28) / 6.0e-5 - 1) < 0.01

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("one mouse at 32: the height is the likelihood", "two mice: multiply the heights"))
x = np.linspace(21, 41, 400)
for m, col in ((28, RED), (30, ORANGE), (32, GREEN)):
    fig.add_trace(go.Scatter(x=x, y=f(x, m), mode="lines", line=dict(color=col, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=[32], y=[f(32, m)], mode="markers", marker=dict(size=12, color=col)), 1, 1)
    fig.add_annotation(x=32.3, y=f(32, m), text=f"μ = {m}: {f(32, m):.3f}", showarrow=False, xanchor="left",
                       bgcolor="white", font=dict(size=19, color=col), xref="x1", yref="y1")
fig.add_trace(go.Scatter(x=[32, 32], y=[0, f(32, 32)], mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, 1)
for m, col, lx in ((33, GREEN, 37.5), (28, RED, 24.5)):
    h = f(np.array([32, 34.0]), m)
    fig.add_trace(go.Scatter(x=x, y=f(x, m), mode="lines", line=dict(color=col, width=3)), 1, 2)
    for xi, hi in zip((32, 34), h):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[0, hi], mode="lines+markers", line=dict(color=col, width=5),
                                 marker=dict(size=[0, 11], color=col)), 1, 2)
    prod = f"{h.prod():.1e}".replace("e-05", " × 10⁻⁵") if h.prod() < 1e-3 else f"{h.prod():.3f}"
    fig.add_annotation(x=lx, y=0.222, text=f"μ = {m}<br>product {prod}", showarrow=False,
                       font=dict(size=18, color=col), xref="x2", yref="y2")
for c in (1, 2):
    pts = [32] if c == 1 else [32, 34]
    fig.add_trace(go.Scatter(x=pts, y=[0] * len(pts), mode="markers", marker=dict(size=13, color="black")), 1, c)
fig.update_xaxes(title_text="mouse weight (grams)")
fig.update_yaxes(title_text="height of the curve", row=1, col=1)
fig.update_yaxes(range=[0, 0.24])
fig.update_layout(template="simple_white", width=1200, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=19)
fig.write_image(HERE / "one_two_mice.png", scale=2)
fig.write_image(HERE / "one_two_mice.pdf")
