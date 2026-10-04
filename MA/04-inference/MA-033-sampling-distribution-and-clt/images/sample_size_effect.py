"""Sampling distribution of the mean of an exponential(1) population for n = 1, 2, 5, 30 (10,000 samples each):
it becomes more normal and narrower as n grows. Black curve: N(1, 1/n)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE = "#4C78A8"
sizes = [1, 2, 5, 30]
fig = make_subplots(rows=1, cols=4, shared_yaxes=False, horizontal_spacing=0.05,
                    subplot_titles=[f"n = {n}" for n in sizes])
grid = np.linspace(0, 4, 300)
for i, n in enumerate(sizes, start=1):
    means = np.random.default_rng(3).exponential(1, (10_000, n)).mean(axis=1)
    fig.add_histogram(x=means, histnorm="probability density", xbins=dict(start=0, end=4, size=0.08),
                      marker_color=BLUE, opacity=0.65, row=1, col=i)
    fig.add_scatter(x=grid, y=stats.norm(1, 1 / np.sqrt(n)).pdf(grid), mode="lines",
                    line=dict(color="black", width=2.5), row=1, col=i)
    fig.add_annotation(x=3.9, y=1, xref=f"x{i if i > 1 else ''}", yref=f"y{i if i > 1 else ''} domain", xanchor="right", showarrow=False,
                       text=f"std of means {means.std():.3f}<br>σ/√n = {1 / np.sqrt(n):.3f}", font_size=15)
    fig.update_xaxes(range=[0, 4], title_text="sample mean", row=1, col=i)
fig.update_yaxes(showticklabels=False)
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1200, height=380, showlegend=False, bargap=0,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=20, r=15, t=40, b=50))
fig.write_image(here / "sample_size_effect.png", scale=2)
fig.write_image(here / "sample_size_effect.pdf")
