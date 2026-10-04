"""Type I and Type II errors by simulation, for the training-program test (H0: mu = 50, H1: mu > 50, sigma = 5,
n = 30, alpha = 0.05, critical value 1.645). Left: 200 tests when H0 is true; red z values beyond 1.645 are Type I
errors (about 5 percent). Right: 200 tests when the true mean is 52; orange z values below 1.645 are Type II errors
(about 29 percent)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(0)
se = 5 / np.sqrt(30)


def zs(mu, k=200):
    return (rng.normal(mu, 5, (k, 30)).mean(axis=1) - 50) / se


z0, z1 = zs(50), zs(52)
t1, t2 = np.mean(z0 > 1.645), np.mean(z1 <= 1.645)
assert 0.02 < t1 < 0.09 and 0.2 < t2 < 0.38, (t1, t2)
big = np.mean(zs(52, 100_000) <= 1.645)
assert abs(big - 0.29) < 0.01                                   # the Note's beta = 0.29
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=[
    f"H<sub>0</sub> true (μ = 50): <b>{int(round(200 * t1))}</b> of 200 tests reject → Type I errors",
    f"H<sub>0</sub> false (μ = 52): <b>{int(round(200 * t2))}</b> of 200 tests fail to reject → Type II errors"])
jit = np.random.default_rng(1).uniform(-1, 1, 200)
fig.add_scatter(x=z0, y=jit, mode="markers", marker=dict(size=9, color=np.where(z0 > 1.645, "#E45756", "#9a9a9a")), row=1, col=1)
fig.add_scatter(x=z1, y=jit, mode="markers", marker=dict(size=9, color=np.where(z1 <= 1.645, "#F58518", "#54A24B")), row=1, col=2)
for c in (1, 2):
    fig.add_vline(x=1.645, line=dict(color="black", width=2, dash="dash"), row=1, col=c)
    fig.update_xaxes(title_text="z statistic of one test", range=[-3.5, 6], row=1, col=c)
    fig.update_yaxes(visible=False, range=[-1.5, 1.5], row=1, col=c)
fig.add_annotation(x=1.645, y=1.35, text="critical value 1.645", showarrow=False, xanchor="left", xshift=5, row=1, col=1, font=dict(size=16))
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1500, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=30, r=20, t=70, b=60))
fig.write_image(here / "error_sim.png", scale=2)
fig.write_image(here / "error_sim.pdf")
