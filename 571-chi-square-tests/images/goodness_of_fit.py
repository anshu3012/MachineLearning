"""Goodness of fit for the age groups. Left: observed counts against the counts expected from the claimed shares.
Right: chi-square density with df = 2; the red area beyond 3.48 is the p-value, the dashed line the 5% critical value."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
groups, observed, expected = ["child", "adult", "elderly"], [20, 26, 14], [15, 33, 12]
stat = stats.chisquare(observed, expected).statistic
crit = stats.chi2.ppf(0.95, 2)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, column_widths=[0.42, 0.58],
                    subplot_titles=["observed and expected counts", f"χ² = {stat:.2f}: p = 0.175"])
fig.add_bar(x=groups, y=observed, name="observed", marker_color="#4C78A8", row=1, col=1)
fig.add_bar(x=groups, y=expected, name="expected under H0", marker_color="#54A24B", row=1, col=1)
x = np.linspace(0, 12, 500)
fig.add_scatter(x=x, y=stats.chi2.pdf(x, 2), mode="lines", line=dict(color="black", width=3), showlegend=False,
                row=1, col=2)
tail = x[x >= stat]
fig.add_scatter(x=np.r_[stat, tail, tail[-1]], y=np.r_[0, stats.chi2.pdf(tail, 2), 0], fill="toself",
                fillcolor="rgba(228,87,86,0.55)", line=dict(width=0), showlegend=False, row=1, col=2)
fig.add_scatter(x=[crit, crit], y=[0, 0.3], mode="lines", line=dict(color="#6B6B6B", dash="dash", width=2),
                showlegend=False, row=1, col=2)
fig.add_annotation(x=crit, y=0.32, text="5.99: critical value for α = 0.05", showarrow=False, xanchor="left",
                   font=dict(size=16, color="#6B6B6B"), row=1, col=2)
fig.add_annotation(x=stat + 0.3, y=0.14, text="p = red area", showarrow=False, xanchor="left",
                   font=dict(size=16, color="#E45756"), row=1, col=2)
fig.update_xaxes(title_text="χ² with df = 2", row=1, col=2)
fig.update_yaxes(title_text="count", row=1, col=1)
fig.update_yaxes(title_text="density", row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1100, height=430, barmode="group",
                  legend=dict(orientation="h", x=0.2, xanchor="center", y=-0.18),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "goodness_of_fit.png", scale=2)
fig.write_image(here / "goodness_of_fit.pdf")
