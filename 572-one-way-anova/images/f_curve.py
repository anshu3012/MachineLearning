"""F distribution with 2 and 6 degrees of freedom. Left: the whole curve with the 5% critical value 5.14 (dashed).
Right: the tail zoomed in; the red area beyond F = 12 is the p-value 0.008."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
crit = stats.f.ppf(0.95, 2, 6)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["the whole curve", "the tail, zoomed in: p = 0.008"])
for col, (lo, hi, top) in enumerate([(0, 16, 1.05), (4, 16, 0.035)], start=1):
    x = np.linspace(lo, hi, 600)
    fig.add_scatter(x=x, y=stats.f.pdf(x, 2, 6), mode="lines", line=dict(color="black", width=3), showlegend=False,
                    row=1, col=col)
    tail = x[x >= 12]
    fig.add_scatter(x=np.r_[12, tail, tail[-1]], y=np.r_[0, stats.f.pdf(tail, 2, 6), 0], fill="toself",
                    fillcolor="rgba(228,87,86,0.6)", line=dict(width=0), showlegend=False, row=1, col=col)
    fig.add_scatter(x=[crit, crit], y=[0, top * 0.8], mode="lines", line=dict(color="#6B6B6B", dash="dash", width=2),
                    showlegend=False, row=1, col=col)
    fig.update_yaxes(range=[0, top], row=1, col=col)
    fig.update_xaxes(title_text="F with 2 and 6 df", row=1, col=col)
fig.add_annotation(x=crit, y=0.86, text="5.14: critical value, α = 0.05", showarrow=False, xanchor="left",
                   font=dict(size=16, color="#6B6B6B"), row=1, col=1)
fig.add_annotation(x=12.3, y=0.012, text="F = 12", showarrow=False, xanchor="left",
                   font=dict(size=17, color="#E45756"), row=1, col=2)
fig.update_yaxes(title_text="density", row=1, col=1)
for t in ["the whole curve", "the tail, zoomed in: p = 0.008"]:
    fig.update_annotations(font_size=19, selector=dict(text=t))
fig.update_layout(template="simple_white", width=1100, height=420, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=70, r=20, t=40, b=50))
fig.write_image(here / "f_curve.png", scale=2)
fig.write_image(here / "f_curve.pdf")
