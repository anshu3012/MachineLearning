"""Binomial PMFs (bars) with n * p = 4 against the Poisson PMF with lambda = 4 (dots): as n grows and p shrinks,
the binomial bars settle onto the Poisson dots."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
CASES = [(10, 0.4), (40, 0.1), (1000, 0.004)]
y = np.arange(0, 13)
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=[f"n = {n}, p = {p}" for n, p in CASES])
for i, (n, p) in enumerate(CASES, start=1):
    fig.add_bar(x=y, y=stats.binom.pmf(y, n, p), marker_color="#4C78A8", opacity=0.6, name="binomial",
                showlegend=(i == 1), row=1, col=i)
    fig.add_scatter(x=y, y=stats.poisson.pmf(y, 4), mode="markers", marker=dict(color="black", size=9),
                    name="Poisson, λ = 4", showlegend=(i == 1), row=1, col=i)
    fig.update_xaxes(tickvals=list(range(0, 13, 2)), title_text="number of successes", row=1, col=i)
fig.update_yaxes(title_text="probability", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=440, bargap=0.1,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.28),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "binomial_to_poisson.png", scale=2)
fig.write_image(here / "binomial_to_poisson.pdf")
