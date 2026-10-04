"""Misreadings 2 and 3 measured, with the Notebook's draws (seed 1): one 95% interval (45.30 to 53.62) catches 94.2%
of 100,000 new sample means and only 21.7% of 100,000 individual values; over 2,000 different first samples the share
of new means caught averages 0.834, not 0.95."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
rng = np.random.default_rng(1)
se = 15 / np.sqrt(50)
first = rng.normal(50, 15, 50).mean()
low, high = first - 1.96 * se, first + 1.96 * se
new_means = rng.normal(50, 15, (100_000, 50)).mean(axis=1)
ages = rng.normal(50, 15, 100_000)
in_means = np.mean((low <= new_means) & (new_means <= high))
in_ages = np.mean((low <= ages) & (ages <= high))
assert (round(low, 2), round(high, 2)) == (45.30, 53.62) and round(in_means, 3) == 0.942 and round(in_ages, 3) == 0.217
firsts = np.random.default_rng(7).normal(50, se, 2000)               # 2,000 other first sample means
caught = stats.norm.cdf((firsts + 1.96 * se - 50) / se) - stats.norm.cdf((firsts - 1.96 * se - 50) / se)
assert abs(caught.mean() - (2 * stats.norm.cdf(1.96 / np.sqrt(2)) - 1)) < 0.01
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07, subplot_titles=[
    f"Misreading 2: new sample means<br><b>{100 * in_means:.1f}%</b> inside this interval",
    f"Misreading 3: individual values<br><b>{100 * in_ages:.1f}%</b> inside this interval",
    f"Many first samples: share of new means<br>caught averages <b>{caught.mean():.3f}</b>, not 0.95"])
for j, v in ((1, new_means), (2, ages)):
    fig.add_histogram(x=v, nbinsx=80, marker_color="#4C78A8", opacity=0.75, row=1, col=j)
    fig.add_vrect(x0=low, x1=high, fillcolor="#F58518", opacity=0.3, line_width=0, row=1, col=j)
fig.add_histogram(x=caught, nbinsx=40, marker_color="#9a9a9a", row=1, col=3)
fig.add_vline(x=caught.mean(), line=dict(color="#E45756", width=3), row=1, col=3)
fig.add_vline(x=0.95, line=dict(color="black", width=2, dash="dash"), row=1, col=3)
fig.update_xaxes(title_text="sample mean", range=[38, 62], row=1, col=1)
fig.update_xaxes(title_text="individual value", row=1, col=2)
fig.update_xaxes(title_text="share of new means caught", row=1, col=3)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1500, height=500, showlegend=False, bargap=0.02,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=50, r=20, t=90, b=60))
fig.write_image(here / "misreadings.png", scale=2)
fig.write_image(here / "misreadings.pdf")
