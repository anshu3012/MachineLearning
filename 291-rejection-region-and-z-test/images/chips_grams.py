"""The chips decision in grams: under H0 the mean of 40 packets is normal with mean 50 g and standard error
4/sqrt(40) = 0.632 g, so at alpha = 0.05 we fail to reject for sample means between 50 -+ 1.96 x 0.632, i.e.
48.76 g to 51.24 g. The watchdog's 49 g lies inside."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
RED, GREEN = "#E45756", "#54A24B"
SE = 4 / np.sqrt(40)
lo, hi = 50 - 1.96 * SE, 50 + 1.96 * SE
assert round(SE, 3) == 0.632 and (round(lo, 2), round(hi, 2)) == (48.76, 51.24) and lo < 49 < hi
x = np.linspace(47.5, 52.5, 600)
pdf = stats.norm.pdf(x, 50, SE)
fig = go.Figure()
for side in (x[x <= lo], x[x >= hi]):
    fig.add_scatter(x=side, y=stats.norm.pdf(side, 50, SE), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)",
                    line=dict(width=0))
fig.add_scatter(x=x, y=pdf, mode="lines", line=dict(color="black", width=3))
fig.add_shape(type="line", x0=lo, x1=hi, y0=0.08, y1=0.08, line=dict(color="#4C78A8", width=6))
fig.add_annotation(x=50, y=0.12, text="fail to reject H₀", showarrow=False, font=dict(size=22, color="#4C78A8"))
for v in (lo, hi):
    fig.add_vline(x=v, line=dict(color=RED, width=2.5, dash="dash"), opacity=1)
fig.add_vline(x=49, line=dict(color=GREEN, width=5), opacity=1)
fig.add_annotation(x=49, y=0.5, ax=-90, ay=-30, text="x̄ = 49 g", arrowcolor=GREEN, arrowwidth=3,
                   font=dict(size=24, color=GREEN), bgcolor="white")
fig.update_xaxes(title_text="mean weight of 40 packets (g)", tickvals=[48, round(lo, 2), 50, round(hi, 2), 52],
                 range=[47.5, 52.5])
fig.update_yaxes(showticklabels=False, range=[0, pdf.max() * 1.1])
fig.update_layout(template="simple_white", width=900, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="under H₀: mean 50 g, standard error 0.632 g", x=0.5),
                  margin=dict(l=20, r=20, t=60, b=60))
fig.write_image(here / "chips_grams.png", scale=2)
fig.write_image(here / "chips_grams.pdf")
