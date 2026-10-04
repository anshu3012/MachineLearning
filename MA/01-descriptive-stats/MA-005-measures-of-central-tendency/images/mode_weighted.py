"""Two stills. mode_counts: how often each value of 1, 2, 1, 3, 1, 4, 2, 1 appears; the tallest bar is the mode.
weighted_mean: three model predictions (10, 15, 12 lakh) drawn as weights on a beam (dot size = weight 0.2, 0.3,
0.5); the weighted mean 12.5 is the balance point, the plain mean 12.33 treats every model the same."""
from collections import Counter
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)

counts = Counter([1, 2, 1, 3, 1, 4, 2, 1])
vals = sorted(counts)
fig = go.Figure(go.Bar(x=vals, y=[counts[v] for v in vals], marker_color=[ORANGE if v == 1 else BLUE for v in vals],
                       text=[f"{counts[v]}×" for v in vals], textposition="outside", textfont=dict(size=22)))
fig.add_annotation(x=1, y=5.0, text="mode = 1", showarrow=False, font=dict(size=24, color=ORANGE))
fig.update_layout(template="simple_white", width=700, height=420, font=FONT, margin=dict(l=70, r=20, t=30, b=60),
                  xaxis=dict(title="value", dtick=1), yaxis=dict(title="count", range=[0, 5.5], dtick=1))
fig.write_image(HERE / "mode_counts.png", scale=2)
fig.write_image(HERE / "mode_counts.pdf")

pred, w = np.array([10, 15, 12]), np.array([0.2, 0.3, 0.5])
names = ["linear regression", "random forest", "XGBoost"]
wm, pm = np.average(pred, weights=w), pred.mean()
assert abs(wm - 12.5) < 1e-9
fig = go.Figure()
fig.add_shape(type="line", x0=9, x1=16, y0=0, y1=0, line=dict(color=GREY, width=4))
fig.add_scatter(x=pred, y=np.zeros(3), mode="markers+text", marker=dict(size=140 * w, color=BLUE),
                text=[f"{n}<br>{p} lakh · w = {x}" for n, p, x in zip(names, pred, w)], textposition="top center",
                textfont=dict(size=18))
fig.add_scatter(x=[wm], y=[-0.13], mode="markers", marker=dict(symbol="triangle-up", size=30, color=ORANGE))
fig.add_scatter(x=[pm], y=[-0.13], mode="markers", marker=dict(symbol="triangle-up", size=22, color="white",
                line=dict(color=GREY, width=2)))
fig.add_annotation(x=wm, y=-0.25, text=f"weighted mean {wm:.1f}", showarrow=False, xanchor="left", xshift=4,
                   font=dict(size=20, color=ORANGE))
fig.add_annotation(x=pm, y=-0.25, text=f"plain mean {pm:.2f}", showarrow=False, xanchor="right", xshift=-4,
                   font=dict(size=18, color=GREY))
fig.update_layout(template="simple_white", width=900, height=420, font=FONT, showlegend=False,
                  margin=dict(l=30, r=30, t=20, b=60), xaxis=dict(title="predicted price (lakh rupees)", range=[8.5, 16.5]),
                  yaxis=dict(visible=False, range=[-0.35, 0.4]))
fig.write_image(HERE / "weighted_mean.png", scale=2)
fig.write_image(HERE / "weighted_mean.pdf")
