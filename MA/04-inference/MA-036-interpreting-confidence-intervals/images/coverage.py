"""100 samples of n = 50 from N(50, 15^2); a 95% z-interval (sigma known) from each. Blue intervals contain the
population mean 50, orange ones miss it. Same seed as the Notebook."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
mu, sigma, n, sims, level = 50, 15, 50, 100, 0.95
rng = np.random.default_rng(42)
means = rng.normal(mu, sigma, (sims, n)).mean(axis=1)
margin = stats.norm.ppf((1 + level) / 2) * sigma / np.sqrt(n)
low, high = means - margin, means + margin
hit = (low <= mu) & (mu <= high)
fig = go.Figure()
for ok, colour, name in [(True, BLUE, "contains μ"), (False, ORANGE, "misses μ")]:
    xs, ys = [], []
    for i in np.flatnonzero(hit == ok):
        xs += [i + 1, i + 1, None]
        ys += [low[i], high[i], None]
    fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=colour, width=4 if not ok else 2.5),
                    name=f"{name}: {int((hit == ok).sum())}")
fig.add_scatter(x=np.arange(1, sims + 1), y=means, mode="markers", marker=dict(color="black", size=4),
                name="sample mean")
fig.add_hline(y=mu, line=dict(color=RED, width=2.5), opacity=1, layer="above")
fig.add_annotation(x=sims + 1, y=mu, text="μ = 50", xanchor="left", showarrow=False, font_size=18)
fig.update_xaxes(title_text="sample number", range=[0, sims + 8])
fig.update_yaxes(title_text="95% confidence interval")
fig.update_layout(template="simple_white", width=1100, height=430,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=50))
fig.write_image(here / "coverage.png", scale=2)
fig.write_image(here / "coverage.pdf")
