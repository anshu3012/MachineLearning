"""Is it log-normal? 1,000 simulated comment lengths (words): the raw values are right-skewed; their natural logs
look normal, and the Q-Q plot of the logs against the normal is a straight line."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
words = np.round(np.random.default_rng(42).lognormal(mean=3, sigma=1, size=1000)).clip(1)
logs = np.log(words)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.08,
                    subplot_titles=[f"Comment length (skewness {stats.skew(words):.1f})",
                                    f"ln(length) (skewness {stats.skew(logs):.2f})",
                                    "Q-Q plot of ln(length) vs normal"])
fig.add_histogram(x=words, xbins=dict(start=0, end=500, size=10), histnorm="probability density",
                  marker=dict(color=BLUE, opacity=0.65), row=1, col=1)
fig.add_histogram(x=logs, nbinsx=30, histnorm="probability density", marker=dict(color=BLUE, opacity=0.65),
                  row=1, col=2)
(osm, osr), (slope, icpt, _) = stats.probplot(logs, dist="norm")
fig.add_scatter(x=osm, y=osr, mode="markers", marker=dict(color=BLUE, size=5, opacity=0.7), row=1, col=3)
ends = np.array([osm.min(), osm.max()])
fig.add_scatter(x=ends, y=icpt + slope * ends, mode="lines", line=dict(color=RED, width=3), row=1, col=3)
fig.update_xaxes(title_text="words", row=1, col=1)
fig.update_xaxes(title_text="ln(words)", row=1, col=2)
fig.update_xaxes(title_text="normal quantiles", row=1, col=3)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(title_text="ln(words) quantiles", row=1, col=3)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1250, height=430, showlegend=False, bargap=0.03,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=50, b=50))
fig.write_image(here / "lognormal_check.png", scale=2)
fig.write_image(here / "lognormal_check.pdf")
