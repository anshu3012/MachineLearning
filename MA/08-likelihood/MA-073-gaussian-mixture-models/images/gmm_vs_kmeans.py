"""k-means against a GMM on the Iris dataset (150 flowers, 4 features, 3 species; scikit-learn's load_iris). Both
are fitted on all 4 features; the plot shows petal length against petal width. Left: k-means labels. Right: GMM with
full covariance matrices; colours mix by responsibility, ellipses show 1 and 2 standard deviations of each component
in these two features. Titles give the adjusted Rand index against the true species."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

from common import FONT

HERE = Path(__file__).parent
RGB = np.array([[76, 120, 168], [245, 133, 24], [84, 162, 75]])          # blue, orange, green
col = lambda c: "rgb(%d,%d,%d)" % tuple(int(v) for v in c)
X, species = load_iris(return_X_y=True)
km = KMeans(3, n_init=10, random_state=0).fit(X)
gmm = GaussianMixture(3, covariance_type="full", n_init=10, random_state=0).fit(X)
sph = GaussianMixture(3, covariance_type="spherical", n_init=10, random_state=0).fit(X)
ari = {name: adjusted_rand_score(species, lab) for name, lab in
       (("km", km.labels_), ("full", gmm.predict(X)), ("sph", sph.predict(X)))}
assert ari["full"] > ari["km"] + 0.1 and abs(ari["sph"] - ari["km"]) < 0.05
P = [2, 3]                                                       # petal length, petal width


def order(labels):                                              # colour k = the species most of its flowers belong to
    return [int(np.bincount(species[labels == k], minlength=3).argmax()) for k in range(3)]


fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=(f"k-means: hard labels (ARI {ari['km']:.2f})",
                                    f"GMM: soft labels and ellipses (ARI {ari['full']:.2f})"))
ok = order(km.labels_)
fig.add_trace(go.Scatter(x=X[:, 2], y=X[:, 3], mode="markers", showlegend=False,
                         marker=dict(size=8, color=[col(RGB[ok[l]]) for l in km.labels_])), 1, 1)
og = order(gmm.predict(X))
R = gmm.predict_proba(X)
mix = sum(R[:, [k]] * RGB[og[k]] for k in range(3))
fig.add_trace(go.Scatter(x=X[:, 2], y=X[:, 3], mode="markers", showlegend=False,
                         marker=dict(size=8, color=[col(c) for c in mix])), 1, 2)
t = np.linspace(0, 2 * np.pi, 200)
for k in range(3):
    C = gmm.covariances_[k][np.ix_(P, P)]
    vals, vecs = np.linalg.eigh(C)
    for s in (1, 2):
        e = gmm.means_[k, P] + s * (vecs @ np.diag(np.sqrt(vals)) @ np.vstack([np.cos(t), np.sin(t)])).T
        fig.add_trace(go.Scatter(x=e[:, 0], y=e[:, 1], mode="lines", showlegend=False,
                                 line=dict(color=col(RGB[og[k]]), width=3 if s == 1 else 2,
                                           dash="solid" if s == 1 else "dash")), 1, 2)
for c in (1, 2):
    fig.update_xaxes(title_text="petal length (cm)", range=[0.5, 7.5], row=1, col=c)
    fig.update_yaxes(title_text="petal width (cm)", range=[-0.5, 3], row=1, col=c)
fig.update_layout(template="simple_white", width=1200, height=540, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "gmm_vs_kmeans.png", scale=2)
fig.write_image(HERE / "gmm_vs_kmeans.pdf")
print({k: round(v, 3) for k, v in ari.items()})
