"""The same 100 samples of n = 10 from N(50, 15^2) with two 95% intervals each: z with the sample standard
deviation s (left, too narrow) and t with s (right). Coverage over 100,000 samples is printed in the titles."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
mu, sigma, n, level = 50, 15, 10, 0.95
crit = {"z": stats.norm.ppf((1 + level) / 2), "t": stats.t.ppf((1 + level) / 2, n - 1)}


def limits(sims, kind, seed=42):
    x = np.random.default_rng(seed).normal(mu, sigma, (sims, n))
    m, s = x.mean(axis=1), x.std(axis=1, ddof=1)
    e = crit[kind] * s / np.sqrt(n)
    return m - e, m + e


titles = []
for kind in ["z", "t"]:
    lo, hi = limits(100_000, kind)
    titles.append(f"{kind} with s (critical value {crit[kind]:.2f}): {np.mean((lo <= mu) & (mu <= hi)):.1%} of 100,000 contain μ")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.05, shared_yaxes=True, subplot_titles=titles)
for col, kind in enumerate(["z", "t"], start=1):
    lo, hi = limits(100, kind)
    hit = (lo <= mu) & (mu <= hi)
    for ok, colour in [(True, BLUE), (False, ORANGE)]:
        xs, ys = [], []
        for i in np.flatnonzero(hit == ok):
            xs += [i + 1, i + 1, None]
            ys += [lo[i], hi[i], None]
        fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=colour, width=2.5 if ok else 3.5), row=1, col=col)
    fig.add_hline(y=mu, line=dict(color=RED, width=2.5), opacity=1, layer="above", row=1, col=col)
    fig.add_annotation(x=50, y=24, text=f"{int(hit.sum())} of these 100 contain μ = 50", showarrow=False,
                       font_size=19, bgcolor="white", row=1, col=col)
    fig.update_xaxes(title_text="sample number", range=[0, 101], row=1, col=col)
fig.update_yaxes(title_text="95% interval", row=1, col=1)
fig.update_yaxes(range=[20, 80])
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1200, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "z_vs_t_coverage.png", scale=2)
fig.write_image(here / "z_vs_t_coverage.pdf")
