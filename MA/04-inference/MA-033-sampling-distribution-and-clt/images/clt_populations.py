"""The CLT on five populations. Top: the population (100,000 draws). Bottom: the means of 1000 samples of
size n (30 for the uniform, 50 for the rest) with the normal curve N(mu, sigma^2/n) the CLT predicts."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
ORANGE, GREEN = "#F58518", "#54A24B"
# name, scipy distribution, sample size, discrete?
pops = [("uniform(0, 1)", stats.uniform(0, 1), 30, False),
        ("exponential(1)", stats.expon(), 50, False),
        ("Poisson(3)", stats.poisson(3), 50, True),
        ("gamma(2, 1)", stats.gamma(2), 50, False),
        ("binomial(10, 0.2)", stats.binom(10, 0.2), 50, True)]
fig = make_subplots(rows=2, cols=5, vertical_spacing=0.2, horizontal_spacing=0.04,
                    subplot_titles=[p[0] for p in pops] + [f"means, n = {p[2]}" for p in pops])
for i, (name, dist, n, discrete) in enumerate(pops, start=1):
    rng = np.random.default_rng(i)
    population = dist.rvs(size=100_000, random_state=rng)
    means = dist.rvs(size=(1000, n), random_state=rng).mean(axis=1)
    if discrete:
        k = np.arange(population.max() + 1)
        fig.add_bar(x=k, y=np.bincount(population.astype(int)) / population.size, marker_color=ORANGE,
                    row=1, col=i)
    else:
        fig.add_histogram(x=population, histnorm="probability density", xbins=dict(start=0, size=population.max() / 50), marker_color=ORANGE,
                          row=1, col=i)
    # discrete populations give means on a grid of steps 1/n: bins of 5 steps keep the bars even
    bins = dict(start=means.min() - 0.5 / n, size=5 / n) if discrete else dict(size=(means.max() - means.min()) / 30)
    fig.add_histogram(x=means, histnorm="probability density", xbins=bins, marker_color=GREEN, opacity=0.6,
                      row=2, col=i)
    grid = np.linspace(means.min(), means.max(), 200)
    fig.add_scatter(x=grid, y=stats.norm(dist.mean(), dist.std() / np.sqrt(n)).pdf(grid), mode="lines",
                    line=dict(color="black", width=2.5), row=2, col=i)
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(title_text="population", row=1, col=1)
fig.update_yaxes(title_text="sample means", row=2, col=1)
fig.update_xaxes(nticks=4)
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1200, height=520, showlegend=False, bargap=0.05,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=50, r=15, t=40, b=30))
fig.write_image(here / "clt_populations.png", scale=2)
fig.write_image(here / "clt_populations.pdf")
