"""Q-Q plots and kurtosis. Top: histograms; bottom: Q-Q plots.
Uniform data (thin tails) against the normal; the same uniform data against the uniform distribution.
(The fat-tail case is Figure 2 of Note ML-029.)"""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
rng = np.random.default_rng(42)
uni = rng.uniform(0, 1, 1000)
cases = [  # (title, data, distribution compared with, x label)
    (f"Uniform, thin tails (excess kurtosis {stats.kurtosis(uni):.1f})<br>against normal", uni, "norm",
     "normal quantiles"),
    ("Same uniform data<br>against uniform", uni, "uniform", "uniform quantiles"),
]
fig = make_subplots(rows=2, cols=2, subplot_titles=[c[0] for c in cases], vertical_spacing=0.2,
                    horizontal_spacing=0.1, row_heights=[0.35, 0.65])
for col, (_, data, dist, xlab) in enumerate(cases, start=1):
    fig.add_histogram(x=data, nbinsx=30, histnorm="probability density", marker=dict(color=BLUE, opacity=0.6,
                      line=dict(color="white", width=0.5)), row=1, col=col)
    (osm, osr), (slope, icpt, _) = stats.probplot(data, dist=dist)
    fig.add_scatter(x=osm, y=osr, mode="markers", marker=dict(color=BLUE, size=5, opacity=0.7), row=2, col=col)
    ends = np.array([osm.min(), osm.max()])
    fig.add_scatter(x=ends, y=icpt + slope * ends, mode="lines", line=dict(color=RED, width=3), row=2, col=col)
    fig.update_xaxes(title_text=xlab, row=2, col=col)
    fig.update_yaxes(showticklabels=False, row=1, col=col)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(title_text="data quantiles", row=2, col=1)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=900, height=720, showlegend=False, bargap=0.02,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=70, b=50))
fig.write_image(here / "qq_tails.png", scale=2)
fig.write_image(here / "qq_tails.pdf")
