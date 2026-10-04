"""Overdispersion, from the Notebook's experiment (Plotly). Three sets of 100,000 simulated days, mean near 4:
constant rate and independent events; a rate that varies from day to day (gamma, shape 2, scale 2); events in
pairs. Bars: the simulated shares; dots: the Poisson PMF with the same mean. Only the first matches; the other two
are wider, with variance 11.99 and 7.96."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, ORANGE, RED

here = Path(__file__).parent
rng = np.random.default_rng(42)
cases = {
    "constant rate, independent": rng.poisson(4, size=100_000),
    "rate varies from day to day": rng.poisson(rng.gamma(shape=2, scale=2, size=100_000)),
    "events come in pairs": 2 * rng.poisson(2, size=100_000),
}
want = {"constant rate, independent": 3.99, "rate varies from day to day": 11.99, "events come in pairs": 7.96}
y = np.arange(0, 21)
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=[f"{k}<br>mean {v.mean():.2f}, variance {v.var():.2f}" for k, v in cases.items()])
fig.update_annotations(font_size=20)
for col, (k, v) in enumerate(cases.items(), 1):
    assert round(v.var(), 2) == want[k]
    share = np.bincount(v, minlength=21)[:21] / len(v)
    fig.add_trace(go.Bar(x=y, y=share, marker_color=BLUE if col == 1 else ORANGE, name="simulated days",
                         showlegend=col == 1), 1, col)
    fig.add_trace(go.Scatter(x=y, y=stats.poisson.pmf(y, v.mean()), mode="markers", marker=dict(size=9, color=RED),
                             name="Poisson with the same mean", showlegend=col == 1), 1, col)
    fig.update_xaxes(title="events in one day", row=1, col=col)
fig.update_yaxes(title="share of days", row=1, col=1)
fig.update_layout(template="simple_white", width=1300, height=520, font=FONT, bargap=0.1,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22), margin=dict(l=70, r=20, t=90, b=130))
fig.write_image(here / "overdispersion.png", scale=2)
