"""Sections 4.3 and 5.1's worked example: the cluster (1, 2), (3, 2), (2, 5) has centroid (2, 3), the mean of each
feature; the squared distances to it are 2, 2 and 4, so its WCSS is 8. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
P = np.array([[1, 2], [3, 2], [2, 5]], float)
c = P.mean(0)
d2 = ((P - c) ** 2).sum(1)
assert c.tolist() == [2, 3] and d2.tolist() == [2, 2, 4] and d2.sum() == 8
fig = go.Figure()
for p, d in zip(P, d2):
    fig.add_scatter(x=[p[0], c[0]], y=[p[1], c[1]], mode="lines", line=dict(color=GREY, dash="dash", width=2), showlegend=False)
    fig.add_annotation(x=(p[0] + c[0]) / 2, y=(p[1] + c[1]) / 2, text=f"squared distance {d:g}", showarrow=False,
                       font=dict(size=16, color=GREY), xshift=70 if p[0] >= 2 else -70, yshift=8)
fig.add_scatter(x=P[:, 0], y=P[:, 1], mode="markers+text", marker=dict(size=16, color=BLUE),
                text=[f"({a:g}, {b:g})" for a, b in P], textposition="bottom center", showlegend=False)
fig.add_scatter(x=[c[0]], y=[c[1]], mode="markers+text", marker=dict(size=20, color=RED, symbol="x"),
                text=["centroid (2, 3)"], textposition="middle right", textfont=dict(color=RED), showlegend=False)
fig.update_layout(template="simple_white", width=800, height=520, font=FONT,
                  title=dict(text="centroid = (mean of 1, 3, 2; mean of 2, 2, 5) = (2, 3)<br>WCSS = 2 + 2 + 4 = 8", x=0.5, font=dict(size=18)),
                  xaxis=dict(title="feature 1", range=[0, 4.5], dtick=1, constrain="domain"), yaxis=dict(title="feature 2", range=[1, 6], dtick=1, scaleanchor="x"),
                  margin=dict(l=60, r=20, t=90, b=60))
fig.write_image(here / "centroid_example.png", scale=2)
fig.write_image(here / "centroid_example.pdf")
