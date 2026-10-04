"""Distances from one point to 500 random points, in 2, 10, 100 and 1000 columns (Plotly histograms).
Each distance is divided by the average distance, so the panels share one scale."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(0)
dists, titles = [], []
for d in (2, 10, 100, 1000):
    pts = rng.uniform(0, 1, (501, d))
    dist = np.linalg.norm(pts[1:] - pts[0], axis=1)
    print(f"{d:5d} columns: farthest / nearest = {dist.max() / dist.min():.1f}")
    dists.append(dist / dist.mean())
    titles.append(f"{d} columns (farthest is {dist.max() / dist.min():.1f}× the nearest)")
fig = make_subplots(rows=2, cols=2, subplot_titles=titles, shared_xaxes=True, shared_yaxes=True,
                    vertical_spacing=0.14, horizontal_spacing=0.06)
for i, x in enumerate(dists):
    fig.add_histogram(x=x, xbins=dict(start=0, end=2.2, size=0.1), histnorm="percent",
                      marker=dict(color="#4C78A8", line=dict(color="white", width=1)), row=i // 2 + 1, col=i % 2 + 1)
fig.update_xaxes(range=[0, 2.2])
fig.update_yaxes(range=[0, 85])
fig.update_xaxes(title_text="Distance ÷ average distance", row=2)
fig.update_yaxes(title_text="% of points", col=1)
for a in fig.layout.annotations:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1400, height=860, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "distances.png", scale=2)
fig.write_image(here / "distances.pdf")
