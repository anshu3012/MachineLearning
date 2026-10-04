"""KDE by hand: a Gaussian bump (bandwidth 1) on each of six points; their sum divided by n is the KDE."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
pts = np.array([2, 2.5, 3, 4, 8, 8.5])
h = 1.0
x = np.linspace(-1, 11.5, 600)
bumps = [stats.norm.pdf((x - p) / h) / (len(pts) * h) for p in pts]
kde = np.sum(bumps, axis=0)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=["Histogram of six points", "One bump per point; their sum is the KDE"])
fig.add_histogram(x=pts, xbins=dict(start=0, end=11, size=1), histnorm="probability density",
                  marker=dict(color="#4C78A8", line=dict(color="white", width=1.5)), row=1, col=1)
for b in bumps:
    fig.add_scatter(x=x, y=b, mode="lines", line=dict(color="#4C78A8", width=2, dash="dot"), row=1, col=2)
fig.add_scatter(x=x, y=kde, mode="lines", line=dict(color="#F58518", width=4.5), row=1, col=2)
for col in (1, 2):
    fig.add_scatter(x=pts, y=np.full(len(pts), -0.012), mode="markers", row=1, col=col,
                    marker=dict(symbol="line-ns-open", size=16, color="black", line=dict(width=2.5)))
fig.add_shape(type="line", x0=3, x1=3, y0=0, y1=kde[np.argmin(abs(x - 3))], line=dict(color="#E45756", dash="dash", width=2),
              row=1, col=2)
fig.add_annotation(x=3, y=kde[np.argmin(abs(x - 3))], text="KDE at 3: 0.206", ax=70, ay=-30, font=dict(size=18, color="#E45756"),
                   arrowcolor="#E45756", row=1, col=2)
fig.update_xaxes(title_text="x", range=[-1, 11.5], dtick=1)
fig.update_yaxes(title_text="density", range=[-0.025, 0.35], row=1, col=1)
fig.update_yaxes(range=[-0.025, 0.25], row=1, col=2)
fig.update_annotations(selector=dict(xref="paper"), font_size=20)
fig.update_layout(template="simple_white", width=1100, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "kde_build.png", scale=2)
fig.write_image(here / "kde_build.pdf")
