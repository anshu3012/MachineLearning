"""Pareto PDFs and CDFs with x_m = 1 and alpha = 1, 2, 3: a larger alpha gives a higher peak at x_m, a thinner tail
and a CDF that reaches 1 sooner."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
x = np.linspace(1, 5, 600)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=["PDF", "CDF"])
for alpha, colour, dash in ((1, "#54A24B", "dot"), (2, "#4C78A8", "dash"), (3, "#E45756", "solid")):
    d = stats.pareto(alpha)              # scale 1 = x_m
    xx = np.r_[0.5, 0.9999, x]          # 0 below x_m, then a jump to the peak at x_m
    fig.add_scatter(x=xx, y=d.pdf(xx), mode="lines", name=f"α = {alpha}", line=dict(color=colour, width=4, dash=dash,
                    shape="linear"), row=1, col=1)
    fig.add_scatter(x=xx, y=d.cdf(xx), mode="lines", showlegend=False, line=dict(color=colour, width=4, dash=dash),
                    row=1, col=2)
fig.add_annotation(x=1, y=3, text="peak α / x<sub>m</sub> at x = x<sub>m</sub>", ax=110, ay=40, font=dict(size=17),
                   arrowcolor="#6B6B6B", row=1, col=1)
fig.update_xaxes(title_text="x", range=[0.5, 5], dtick=1)
fig.update_yaxes(title_text="density f(x)", row=1, col=1)
fig.update_yaxes(title_text="F(x) = P(X ≤ x)", range=[0, 1.05], row=1, col=2)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1150, height=440, legend=dict(x=0.3, y=0.95, font=dict(size=18)),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "pareto_pdf_cdf.png", scale=2)
fig.write_image(here / "pareto_pdf_cdf.pdf")
