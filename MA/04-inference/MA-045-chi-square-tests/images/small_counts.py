"""Why expected counts must not be tiny, from the Notebook's simulation (Plotly): 200,000 samples drawn with H0
true (rng seed 0, same order of draws as the Notebook). Bars: the simulated chi-square values; curve: the chi-square
distribution with 2 df the test uses. With every E at least 12 the curve fits and 4.9% pass the 5% line; with
expected counts of 0.4 or 0.5 the values bunch on a few spikes and the rejection rate is 11.2% or 2.7%."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
rng = np.random.default_rng(0)
crit = stats.chi2.ppf(0.95, 2)


def sim(shares, n, reps=200_000):
    shares = np.asarray(shares)
    counts = rng.multinomial(n, shares, size=reps)
    e = n * shares
    chi = ((counts - e) ** 2 / e).sum(axis=1)
    return chi, (chi > crit).mean()


cases = [("shares 0.25 / 0.55 / 0.20, n = 60<br>smallest E = 12", *sim([0.25, 0.55, 0.20], 60)),
         ("shares 0.90 / 0.05 / 0.05, n = 8<br>smallest E = 0.4", *sim([0.90, 0.05, 0.05], 8)),
         ("shares 0.90 / 0.05 / 0.05, n = 10<br>smallest E = 0.5", *sim([0.90, 0.05, 0.05], 10))]
assert [round(c[2], 3) for c in cases] == [0.049, 0.112, 0.027], [c[2] for c in cases]
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=[f"{t}<br><b>rejected: {r * 100:.1f}%</b>" for t, _, r in cases])
fig.update_annotations(font_size=18)
xs = np.linspace(0.01, 15, 300)
edges = np.linspace(0, 15, 61)
for col, (_, chi, r) in enumerate(cases, 1):
    h, _ = np.histogram(chi, bins=edges)
    fig.add_trace(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=h / len(chi) / np.diff(edges), marker_color=BLUE,
                         name="simulated χ² (H₀ true)", showlegend=col == 1, width=0.25), 1, col)
    fig.add_trace(go.Scatter(x=xs, y=stats.chi2.pdf(xs, 2), mode="lines", line=dict(color=RED, width=3),
                             name="chi-square, 2 df", showlegend=col == 1), 1, col)
    fig.add_vline(x=crit, line=dict(color="black", dash="dash"), row=1, col=col)
    fig.update_xaxes(title="χ²", range=[0, 15], row=1, col=col)
fig.update_yaxes(title="density", range=[0, 0.8], row=1, col=1)
fig.update_layout(template="simple_white", width=1300, height=520, font=FONT, bargap=0,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22), margin=dict(l=70, r=20, t=110, b=120))
fig.write_image(here / "small_counts.png", scale=2)
