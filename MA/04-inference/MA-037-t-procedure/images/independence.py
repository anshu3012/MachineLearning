"""Section 3: the independence assumption. Samples of 30 from a normal population (mean 50, sd 15): independent
values, or each value tied to the one before (correlation 0.5, an AR(1) series). 60 t-intervals of each kind; coverage
over 20,000 samples (the Notebook's ar_cov, seed 0) in the titles."""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"


def ar_samples(n, rho, sims=20_000, seed=0):                     # same draws as the Notebook's ar_cov
    rng = np.random.default_rng(seed)
    e = rng.normal(0, 1, (sims, n)); x = np.empty_like(e); x[:, 0] = e[:, 0]
    for i in range(1, n):
        x[:, i] = rho * x[:, i - 1] + np.sqrt(1 - rho ** 2) * e[:, i]
    x = 50 + 15 * x
    m, s = x.mean(1), x.std(1, ddof=1)
    h = stats.t.ppf(0.975, n - 1) * s / np.sqrt(n)
    return m, h


res = {rho: ar_samples(30, rho) for rho in (0, 0.5)}
cov = {rho: np.mean(np.abs(m - 50) <= h) for rho, (m, h) in res.items()}
assert round(100 * cov[0], 1) == 95.2 and round(100 * cov[0.5], 1) == 74.1
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=[f"independent values<br>{100 * cov[0]:.1f}% contain μ",
                                    f"each value tied to the one before (0.5)<br>{100 * cov[0.5]:.1f}% contain μ"])
for col, rho in [(1, 0), (2, 0.5)]:
    m, h = res[rho][0][:60], res[rho][1][:60]
    for i in range(60):
        hit = abs(m[i] - 50) <= h[i]
        fig.add_scatter(x=[m[i] - h[i], m[i] + h[i]], y=[i + 1, i + 1], mode="lines", showlegend=False,
                        line=dict(color=BLUE if hit else RED, width=3.5), row=1, col=col)
    fig.add_vline(x=50, line=dict(color="black", width=2, dash="dash"), row=1, col=col)
fig.update_xaxes(title_text="95% t-interval for the mean", range=[30, 70])
fig.update_yaxes(title_text="sample", row=1, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=70, r=20, t=90, b=55))
fig.write_image(here / "independence.png", scale=2)
fig.write_image(here / "independence.pdf")
