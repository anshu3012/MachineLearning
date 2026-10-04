"""Why parametric estimation fails on two-peaked data: the Note's 1,000 two-peaked values (300 around 20, 700
around 40) with a fitted normal PDF, which puts its peak in the valley, and the KDE (bandwidth 3), which follows
both peaks."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from sklearn.neighbors import KernelDensity

here = Path(__file__).parent
rng = np.random.default_rng(42)                     # same draws as the Notebook and kde_bandwidth.py
rng.normal(50, 5, 1000)
data = np.concatenate([rng.normal(20, 5, 300), rng.normal(40, 5, 700)])
assert round(data.std(ddof=1), 2) == 10.29          # the Note's s for this data
x = np.linspace(data.min(), data.max(), 300)
norm = stats.norm(data.mean(), data.std())
kde = np.exp(KernelDensity(bandwidth=3).fit(data.reshape(-1, 1)).score_samples(x.reshape(-1, 1)))
fig = go.Figure()
fig.add_histogram(x=data, nbinsx=30, histnorm="probability density", marker_color="rgba(76,120,168,0.4)",
                  name="1,000 two-peaked values")
fig.add_scatter(x=x, y=norm.pdf(x), mode="lines", line=dict(color="#E45756", width=4),
                name=f"parametric: normal with x̄ = {data.mean():.1f}, s = {data.std():.1f}")
fig.add_scatter(x=x, y=kde, mode="lines", line=dict(color="#F58518", width=4), name="non-parametric: KDE, bandwidth 3")
fig.add_annotation(x=data.mean(), y=norm.pdf(data.mean()), text="the normal curve peaks<br>near the valley", ax=-150, ay=-90,
                   font=dict(size=20), arrowwidth=2)
fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Two peaks: one normal curve cannot follow them, a KDE can", x=0.5), bargap=0.05,
                  xaxis=dict(title="value"), yaxis=dict(title="density", range=[0, 0.07]),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=90, r=30, t=70, b=80))
fig.write_image(here / "normal_fails.png", scale=2)
fig.write_image(here / "normal_fails.pdf")
