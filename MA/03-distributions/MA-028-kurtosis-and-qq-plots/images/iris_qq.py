"""Q-Q plot of the 150 iris sepal lengths against the normal distribution, two ways.
Left: by hand, the 1st to 99th percentiles of the data against those of 1,000 standard normal values.
Right: scipy.stats.probplot, with its least-squares line."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.datasets import load_iris

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
sepal = load_iris().data[:, 0]
theo = np.random.default_rng(42).normal(0, 1, 1000)
pct = np.arange(1, 100)
xq, yq = np.percentile(theo, pct), np.percentile(sepal, pct)
(osm, osr), (slope, icpt, r) = stats.probplot(sepal, dist="norm")

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["By hand: 99 percentiles of each", "scipy probplot: all 150 values"])
fig.add_scatter(x=xq, y=yq, mode="markers", marker=dict(color=BLUE, size=8, opacity=0.8), row=1, col=1)
b, a = np.polyfit(xq, yq, 1)
fig.add_scatter(x=[-2.6, 2.6], y=[a - 2.6 * b, a + 2.6 * b], mode="lines", line=dict(color=RED, width=3), row=1, col=1)
fig.add_scatter(x=osm, y=osr, mode="markers", marker=dict(color=BLUE, size=8, opacity=0.8), row=1, col=2)
fig.add_scatter(x=[-2.7, 2.7], y=[icpt - 2.7 * slope, icpt + 2.7 * slope], mode="lines",
                line=dict(color=RED, width=3), row=1, col=2)
for c in (1, 2):
    fig.update_xaxes(title_text="theoretical quantiles (standard normal)", range=[-2.9, 2.9], dtick=1, row=1, col=c)
fig.update_yaxes(title_text="sepal length quantiles (cm)", range=[3.9, 8.2], row=1, col=1)
fig.update_yaxes(range=[3.9, 8.2], row=1, col=2)
fig.add_annotation(x=1.2, y=4.4, text=f"line: slope {slope:.2f}, intercept {icpt:.2f}", showarrow=False,
                   font=dict(size=16, color=RED), row=1, col=2)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1150, height=470, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=50, b=50))
fig.write_image(here / "iris_qq.png", scale=2)
fig.write_image(here / "iris_qq.pdf")
