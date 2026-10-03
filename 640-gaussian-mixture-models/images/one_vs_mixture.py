"""Why one Gaussian is not enough: the 272 waiting times (minutes) between eruptions of the Old Faithful geyser
(data/old_faithful.csv, seaborn's "geyser" dataset). The single normal fitted by maximum likelihood (mean and
standard deviation of the data) against a two-component GMM fitted by scikit-learn (EM)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
from sklearn.mixture import GaussianMixture

from common import BLUE, FONT, RED

HERE = Path(__file__).parent
x = pd.read_csv(HERE.parent / "data" / "old_faithful.csv")["waiting"].to_numpy(float)
one = stats.norm(x.mean(), x.std())
gmm = GaussianMixture(2, random_state=0).fit(x[:, None])
ll_one = one.logpdf(x).sum()
ll_gmm = gmm.score(x[:, None]) * len(x)
assert ll_gmm > ll_one
g = np.linspace(40, 100, 400)
fig = go.Figure()
fig.add_trace(go.Histogram(x=x, histnorm="probability density", xbins=dict(start=40, end=100, size=2.5),
                           marker_color="#C9D6E5", name="272 waiting times"))
fig.add_trace(go.Scatter(x=g, y=one.pdf(g), mode="lines", line=dict(color=RED, width=4),
                         name=f"one normal (MLE): log-likelihood {ll_one:.0f}"))
fig.add_trace(go.Scatter(x=g, y=np.exp(gmm.score_samples(g[:, None])), mode="lines", line=dict(color=BLUE, width=4),
                         name=f"mixture of 2 normals: log-likelihood {ll_gmm:.0f}"))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, bargap=0.05,
                  xaxis=dict(title="waiting time between eruptions (minutes)"), yaxis=dict(title="density"),
                  legend=dict(orientation="h", x=0, y=-0.2), margin=dict(l=70, r=20, t=20, b=150))
fig.write_image(HERE / "one_vs_mixture.png", scale=2)
fig.write_image(HERE / "one_vs_mixture.pdf")
print(round(ll_one, 1), round(ll_gmm, 1), gmm.weights_.round(2), gmm.means_.ravel().round(1),
      np.sqrt(gmm.covariances_.ravel()).round(1), x.mean().round(1), x.std().round(1))
