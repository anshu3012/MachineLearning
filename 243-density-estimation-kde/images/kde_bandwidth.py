"""Two-peaked data (300 around 20, 700 around 40): scikit-learn KDE with bandwidth 0.5, 3 and 5."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from sklearn.neighbors import KernelDensity

here = Path(__file__).parent
rng = np.random.default_rng(42)                     # same draws as the Notebook
rng.normal(50, 5, 1000)                             # the parametric sample comes first
data = np.concatenate([rng.normal(20, 5, 300), rng.normal(40, 5, 700)])
grid = np.linspace(data.min(), data.max(), 300).reshape(-1, 1)
bws = [(0.5, "spiky"), (3, "two clear peaks"), (5, "valley filled in")]
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.03,
                    subplot_titles=[f"bandwidth {b}: {t}" for b, t in bws])
for i, (bw, _) in enumerate(bws, start=1):
    kde = KernelDensity(kernel="gaussian", bandwidth=bw).fit(data.reshape(-1, 1))
    dens = np.exp(kde.score_samples(grid))
    fig.add_histogram(x=data, nbinsx=30, histnorm="probability density", marker_color="rgba(76,120,168,0.4)",
                      row=1, col=i)
    fig.add_scatter(x=grid[:, 0], y=dens, mode="lines", line=dict(color="#F58518", width=3.5), row=1, col=i)
fig.update_xaxes(title_text="value")
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1250, height=440, showlegend=False, bargap=0.05,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "kde_bandwidth.png", scale=2)
fig.write_image(here / "kde_bandwidth.pdf")
