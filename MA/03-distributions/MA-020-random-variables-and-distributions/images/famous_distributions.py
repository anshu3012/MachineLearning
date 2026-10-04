"""A gallery of famous distributions: four discrete (bars) and four continuous (curves), with their parameters."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
discrete = [
    ("Bernoulli (p = 0.3)", np.array([0, 1]), stats.bernoulli(0.3).pmf),
    ("Binomial (n = 10, p = 0.5)", np.arange(0, 11), stats.binom(10, 0.5).pmf),
    ("Poisson (λ = 3)", np.arange(0, 11), stats.poisson(3).pmf),
    ("Discrete uniform (1 to 6)", np.arange(1, 7), lambda k: np.full(len(k), 1 / 6)),
]
continuous = [
    ("Normal (μ = 0, σ = 1)", np.linspace(-4, 4, 300), stats.norm(0, 1).pdf),
    ("Uniform (a = 0, b = 1)", np.linspace(-0.5, 1.5, 401), stats.uniform(0, 1).pdf),
    ("Log-normal (μ = 0, σ = 0.5)", np.linspace(0.001, 4, 300), stats.lognorm(0.5).pdf),
    ("Exponential (λ = 1)", np.linspace(0, 5, 300), stats.expon().pdf),
]
fig = make_subplots(rows=2, cols=4, subplot_titles=[t for t, _, _ in discrete + continuous],
                    horizontal_spacing=0.07, vertical_spacing=0.2)
for i, (_, k, pmf) in enumerate(discrete, start=1):
    fig.add_bar(x=k, y=pmf(k), marker_color=BLUE, width=0.6, row=1, col=i)
for i, (_, x, pdf) in enumerate(continuous, start=1):
    fig.add_scatter(x=x, y=pdf(x), mode="lines", line=dict(color=ORANGE, width=3.5), fill="tozeroy",
                    fillcolor="rgba(245,133,24,0.15)", row=2, col=i)
fig.update_xaxes(tickvals=[0, 1], range=[-0.6, 1.6], row=1, col=1)
fig.update_xaxes(dtick=1, row=1, col=4)
fig.update_yaxes(title_text="probability", row=1, col=1)
fig.update_yaxes(title_text="density", row=2, col=1)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1200, height=680, showlegend=False, bargap=0.3,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=50, b=40))
fig.write_image(here / "famous_distributions.png", scale=2)
fig.write_image(here / "famous_distributions.pdf")
