"""Is it Pareto? Left: the Pareto PDF on log-log axes is a straight line with slope -(alpha + 1).
Middle: for data, the share of values above x (the survival function) on log-log axes: straight for 1,000 Pareto
values, curved for 1,000 log-normal values. Right: Q-Q plot of the Pareto values against a fitted Pareto."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
rng = np.random.default_rng(42)
par = stats.pareto.rvs(3, size=1000, random_state=rng)
logn = rng.lognormal(0.3, 0.5, 1000)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.09,
                    subplot_titles=["PDF formula, log-log axes", "Data: share above x, log-log axes",
                                    "Q-Q plot against Pareto"])
x = np.linspace(1, 10, 200)
fig.add_scatter(x=np.log(x), y=np.log(stats.pareto(3).pdf(x)), mode="lines", showlegend=False, line=dict(color=RED, width=4),
                row=1, col=1)
fig.add_annotation(x=1.2, y=np.log(stats.pareto(3).pdf(np.exp(1.2))), text="slope −(α + 1) = −4", ax=60, ay=-40,
                   font=dict(size=16), row=1, col=1)
for data, name, colour in ((par, "Pareto data", BLUE), (logn, "log-normal data", ORANGE)):
    s = np.sort(data)
    surv = 1 - np.arange(len(s)) / len(s)                   # share of values >= each sorted value
    fig.add_scatter(x=np.log(s), y=np.log(surv), mode="markers", name=name, marker=dict(color=colour, size=4),
                    row=1, col=2)
b, loc, scale = stats.pareto.fit(par, floc=0)
(osm, osr), (slope, icpt, _) = stats.probplot(par, dist=stats.pareto, sparams=(b, loc, scale))
fig.add_scatter(x=osm, y=osr, mode="markers", showlegend=False, marker=dict(color=BLUE, size=5, opacity=0.7),
                row=1, col=3)
fig.add_scatter(x=[osm.min(), osm.max()], y=icpt + slope * np.array([osm.min(), osm.max()]), mode="lines",
                showlegend=False, line=dict(color=RED, width=3), row=1, col=3)
fig.update_xaxes(title_text="ln x", row=1, col=1)
fig.update_yaxes(title_text="ln f(x)", row=1, col=1)
fig.update_xaxes(title_text="ln x", row=1, col=2)
fig.update_yaxes(title_text="ln(share of values ≥ x)", row=1, col=2)
fig.update_xaxes(title_text=f"Pareto quantiles (fitted α = {b:.2f})", row=1, col=3)
fig.update_yaxes(title_text="data quantiles", row=1, col=3)
fig.update_annotations(selector=dict(xref="paper"), font_size=18)
fig.update_layout(template="simple_white", width=1300, height=450,
                  legend=dict(x=0.37, y=0.08, font=dict(size=15), bgcolor="rgba(255,255,255,0.8)"),
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=50, b=50))
fig.write_image(here / "pareto_check.png", scale=2)
fig.write_image(here / "pareto_check.pdf")
