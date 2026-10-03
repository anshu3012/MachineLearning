"""1000 binomial experiments of 10 coin tosses for three values of p: simulated share of each head count (bars)
against the exact binomial PMF (dots). Same seed as the Notebook."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
COLOURS = {0.1: "#E45756", 0.5: "#54A24B", 0.8: "#4C78A8"}
n, runs = 10, 1000
k = np.arange(n + 1)
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=[f"p = {p}" for p in COLOURS])
for i, (p, colour) in enumerate(COLOURS.items(), start=1):
    heads = np.random.default_rng(42).binomial(n, p, runs)        # heads in each of 1000 experiments
    share = np.bincount(heads, minlength=n + 1) / runs
    fig.add_bar(x=k, y=share, marker_color=colour, opacity=0.55, name="simulated", showlegend=(i == 1),
                row=1, col=i)
    fig.add_scatter(x=k, y=stats.binom.pmf(k, n, p), mode="markers", marker=dict(color="black", size=9),
                    name="exact PMF", showlegend=(i == 1), row=1, col=i)
    fig.update_xaxes(tickvals=list(range(0, 11, 2)), title_text="number of heads in 10 tosses", row=1, col=i)
fig.update_yaxes(title_text="probability", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=420, bargap=0.1,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "binomial_shapes.png", scale=2)
fig.write_image(here / "binomial_shapes.pdf")
