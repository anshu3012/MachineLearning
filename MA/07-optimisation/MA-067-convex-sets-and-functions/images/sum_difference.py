"""Building rules (Plotly). Left: w^2 + 2|w| is a non-negative sum of convex functions; between a = -1 and b = 3 its
midpoint value is 3, below the chord value 9. Right: the difference w^2 - 2w^2 = -w^2; the chord from -1 to 1 sits at
-1, below the curve's value 0 at the midpoint (red), so the difference is not convex."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
s = lambda w: w ** 2 + 2 * np.abs(w)
d = lambda w: w ** 2 - 2 * w ** 2
assert s(1) == 3 and 0.5 * (s(-1) + s(3)) == 9 and d(0) == 0 and 0.5 * (d(-1) + d(1)) == -1

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("sum w² + 2|w|: convex", "difference w² − 2w² = −w²: not convex"))
w = np.linspace(-2, 4, 300)
fig.add_trace(go.Scatter(x=w, y=w ** 2, mode="lines", line=dict(color=GREY, width=2, dash="dot"), name="w²"), 1, 1)
fig.add_trace(go.Scatter(x=w, y=2 * np.abs(w), mode="lines", line=dict(color=GREY, width=2, dash="dash"), name="2|w|"), 1, 1)
fig.add_trace(go.Scatter(x=w, y=s(w), mode="lines", line=dict(color=BLUE, width=4), name="sum"), 1, 1)
fig.add_trace(go.Scatter(x=[-1, 3], y=[s(-1), s(3)], mode="lines+markers", line=dict(color=GREEN, width=3),
                         marker=dict(size=11, color="black")), 1, 1)
fig.add_trace(go.Scatter(x=[1, 1], y=[s(1), 9], mode="lines+markers", line=dict(color=GREEN, width=2, dash="dash"),
                         marker=dict(size=10, color=GREEN)), 1, 1)
fig.add_annotation(x=1, y=9, text="chord 9", xshift=-48, yshift=12, showarrow=False, font=dict(color=GREEN, size=19), row=1, col=1)
fig.add_annotation(x=1, y=3, text="curve 3", xshift=52, yshift=-6, showarrow=False, bgcolor="white", font=dict(color=BLUE, size=19), row=1, col=1)
v = np.linspace(-1.8, 1.8, 300)
fig.add_trace(go.Scatter(x=v, y=d(v), mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
fig.add_trace(go.Scatter(x=[-1, 1], y=[-1, -1], mode="lines+markers", line=dict(color=RED, width=3),
                         marker=dict(size=11, color="black")), 1, 2)
fig.add_trace(go.Scatter(x=[0, 0], y=[-1, 0], mode="lines+markers", line=dict(color=RED, width=2, dash="dash"),
                         marker=dict(size=10, color=RED)), 1, 2)
fig.add_annotation(x=0, y=-1, text="chord −1 below the curve", yshift=-20, showarrow=False, font=dict(color=RED, size=19), row=1, col=2)
fig.add_annotation(x=0, y=0, text="curve 0", yshift=18, showarrow=False, font=dict(color=BLUE, size=19), row=1, col=2)
fig.update_xaxes(title_text="w")
fig.update_yaxes(range=[-1, 25], row=1, col=1)
fig.update_yaxes(range=[-3.5, 0.8], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "sum_difference.png", scale=2)
fig.write_image(HERE / "sum_difference.pdf")
