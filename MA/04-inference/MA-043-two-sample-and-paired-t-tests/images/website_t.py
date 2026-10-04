"""Desktop against mobile (data/website_time.csv, 30 + 30 users). Left: every user's time with the two sample
means. Right: t = 5.20 on Student's t with 58 degrees of freedom, far beyond the two-tailed 5 percent cutoffs."""
from pathlib import Path

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
w = pd.read_csv(here.parent / "data" / "website_time.csv")
d, m = w.minutes[w.device == "desktop"], w.minutes[w.device == "mobile"]
res = stats.ttest_ind(d, m)
crit = stats.t.ppf(0.975, 58)
assert (len(d), len(m)) == (30, 30) and round(d.mean(), 1) == 18.5 and round(m.mean(), 1) == 14.3
assert round(res.statistic, 2) == 5.20 and round(res.pvalue * 1e6, 1) == 2.7, res
fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                    subplot_titles=["30 users each", "t = 5.20 on t, df = 58"])
rng = np.random.default_rng(0)
for i, (v, c, name) in enumerate(((d, BLUE, "desktop"), (m, ORANGE, "mobile"))):
    fig.add_scatter(x=i + rng.uniform(-0.18, 0.18, len(v)), y=v, mode="markers",
                    marker=dict(size=10, color=c, opacity=0.8), row=1, col=1)
    fig.add_scatter(x=[i - 0.3, i + 0.3], y=[v.mean()] * 2, mode="lines", line=dict(color="black", width=4),
                    row=1, col=1)
    fig.add_annotation(x=i + 0.32, y=v.mean(), text=f"{v.mean():.1f}", xanchor="left", showarrow=False,
                       font=dict(size=22), row=1, col=1)
x = np.linspace(-6, 6, 600)
for side in (x[x <= -crit], x[x >= crit]):
    fig.add_scatter(x=side, y=stats.t.pdf(side, 58), fill="tozeroy", fillcolor="rgba(228,87,86,0.4)", line_width=0,
                    row=1, col=2)
fig.add_scatter(x=x, y=stats.t.pdf(x, 58), mode="lines", line=dict(color="black", width=3), row=1, col=2)
fig.add_vline(x=res.statistic, line=dict(color=GREEN, width=5), opacity=1, row=1, col=2)
fig.add_annotation(x=res.statistic, y=0.25, ax=-110, ay=0, text="t = 5.20<br>p = 0.000003", arrowcolor=GREEN,
                   arrowwidth=3, font=dict(size=22, color=GREEN), bgcolor="white", row=1, col=2)
fig.add_annotation(x=crit, y=0.07, ax=40, ay=-50, text="±2.00", font=dict(size=20, color=RED), arrowcolor=RED,
                   row=1, col=2)
fig.update_xaxes(tickvals=[0, 1], ticktext=["desktop", "mobile"], range=[-0.5, 1.7], row=1, col=1)
fig.update_yaxes(title_text="minutes on the site", row=1, col=1)
fig.update_xaxes(title_text="t", range=[-6, 6], row=1, col=2)
fig.update_yaxes(showticklabels=False, range=[0, 0.43], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=60, b=60))
for a in fig.layout.annotations[:2]:
    a.font.size = 22
fig.write_image(here / "website_t.png", scale=2)
fig.write_image(here / "website_t.pdf")
