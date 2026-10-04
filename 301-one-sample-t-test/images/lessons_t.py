"""Five lessons (7, 9, 5, 11, 13 minutes) against H0: mu = 6, right-tailed: t = 2.12 on Student's t with 4 degrees
of freedom. The p-value 0.051 is the red tail; the 5 percent critical value 2.132 is just to its right (zoomed
in the right panel)."""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
GREEN, RED = "#54A24B", "#E45756"
v = np.array([7, 9, 5, 11, 13])
t = (v.mean() - 6) / (v.std(ddof=1) / np.sqrt(5))
p, crit = stats.t.sf(t, 4), stats.t.ppf(0.95, 4)
assert round(t, 2) == 2.12 and round(p, 3) == 0.051 and round(crit, 3) == 2.132
fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.08,
                    subplot_titles=["right tail beyond t = 2.12: p = 0.051", "zoom: t falls short of 2.132"])
for col, x in ((1, np.linspace(-4, 5, 700)), (2, np.linspace(2.0, 2.25, 200))):
    s = x[x >= t]
    fig.add_scatter(x=s, y=stats.t.pdf(s, 4), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)", line_width=0,
                    row=1, col=col)
    fig.add_scatter(x=x, y=stats.t.pdf(x, 4), mode="lines", line=dict(color="black", width=3), row=1, col=col)
    fig.add_vline(x=t, line=dict(color=GREEN, width=4), opacity=1, row=1, col=col)
    fig.add_vline(x=crit, line=dict(color=RED, width=3, dash="dash"), opacity=1, row=1, col=col)
fig.add_annotation(x=t, y=0.3, ax=90, ay=0, text="t = 2.12", arrowcolor=GREEN, arrowwidth=3,
                   font=dict(size=22, color=GREEN), row=1, col=1)
fig.add_annotation(x=3.3, y=stats.t.pdf(3.3, 4) / 2, ax=30, ay=-70, text="p = 0.051", arrowcolor=RED,
                   font=dict(size=22, color=RED), row=1, col=1)
fig.add_annotation(x=t, y=0.025, ax=-75, ay=0, text="t = 2.12", arrowcolor=GREEN, arrowwidth=2,
                   font=dict(size=20, color=GREEN), bgcolor="white", row=1, col=2)
fig.add_annotation(x=crit, y=0.012, ax=75, ay=0, text="5% cutoff<br>2.132", arrowcolor=RED, arrowwidth=2,
                   font=dict(size=20, color=RED), bgcolor="white", row=1, col=2)
fig.update_xaxes(title_text="t (df = 4)", range=[-4, 5], row=1, col=1)
fig.update_xaxes(title_text="t", range=[2.0, 2.25], dtick=0.05, row=1, col=2)
fig.update_yaxes(showticklabels=False, range=[0, 0.42], row=1, col=1)
fig.update_yaxes(showticklabels=False, range=[0, 0.075], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=20, r=20, t=60, b=60))
for a in fig.layout.annotations[:2]:
    a.font.size = 22
fig.write_image(here / "lessons_t.png", scale=2)
fig.write_image(here / "lessons_t.pdf")
