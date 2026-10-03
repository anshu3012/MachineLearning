"""Plotly figures for the DBSCAN Note: k-means against DBSCAN on moons and circles, the 6-point scikit-learn example
with three settings, a dataset with two densities, and the k-distance plot."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import datasets
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=17)
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"]
NOISE = "#6B6B6B"


def scatter(fig, X, lab, r, c, size=5):
    for k in np.unique(lab):
        m = lab == k
        mk = dict(color=NOISE, size=size + 2, symbol="x") if k == -1 else dict(color=COLS[k % len(COLS)], size=size)
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=mk, showlegend=False), r, c)


def save(fig, name, w, h, ticks=False):
    if not ticks:
        fig.update_xaxes(showticklabels=False, ticks=""); fig.update_yaxes(showticklabels=False, ticks="")
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, margin=dict(l=30, r=20, t=50, b=30))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=19))
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# 1. k-means against DBSCAN
moons = StandardScaler().fit_transform(datasets.make_moons(500, noise=0.05, random_state=170)[0])
circles = StandardScaler().fit_transform(datasets.make_circles(500, factor=0.5, noise=0.05, random_state=170)[0])
fig = make_subplots(rows=2, cols=2, column_titles=["k-means, k = 2", "DBSCAN, eps = 0.3, MinPts = 5"],
                    vertical_spacing=0.06, horizontal_spacing=0.05)
for i, X in enumerate([moons, circles]):
    scatter(fig, X, KMeans(n_clusters=2, random_state=0).fit_predict(X), i + 1, 1)
    scatter(fig, X, DBSCAN(eps=0.3, min_samples=5).fit_predict(X), i + 1, 2)
save(fig, "dbscan_vs_kmeans", 1000, 900)

# 2. The 6-point example with three settings
X6 = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])
settings = [(3, 2), (3, 3), (10, 3)]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                    subplot_titles=[f"eps = {e}, MinPts = {m}" for e, m in settings])
for j, (e, m) in enumerate(settings):
    lab = DBSCAN(eps=e, min_samples=m).fit_predict(X6)
    print(e, m, lab)
    scatter(fig, X6, lab, 1, j + 1, size=13)
    for (x, y), l in zip(X6, lab):
        fig.add_annotation(x=np.log10(x), y=np.log10(y), text=str(l), showarrow=False, xshift=-22 if x > 20 else 18, yshift={8: 9, 7: -9}.get(y, 0), font=dict(size=16),
                           row=1, col=j + 1)
fig.update_xaxes(type="log", range=[-0.1, 1.5]); fig.update_yaxes(type="log", range=[0.15, 2.05])
save(fig, "sklearn_toy", 1100, 400)

# 3. Two clusters of different density
Xv, _ = datasets.make_blobs(n_samples=[300, 100], centers=[(0, 0), (4, 0)], cluster_std=[0.3, 1.3], random_state=0)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.05, subplot_titles=[
    "eps = 0.3: most of the sparse group is noise", "eps = 0.8: everything is one cluster"])
for j, e in enumerate([0.3, 0.8]):
    lab = DBSCAN(eps=e, min_samples=5).fit_predict(Xv)
    print("eps", e, "clusters", len(set(lab) - {-1}), "noise", (lab == -1).sum())
    scatter(fig, Xv, lab, 1, j + 1)
save(fig, "varying_density", 1100, 430)

# 4. k-distance plot for the moons (k = min_samples = 5)
dist, _ = NearestNeighbors(n_neighbors=5).fit(moons).kneighbors(moons)
kd = np.sort(dist[:, -1])
fig = go.Figure(go.Scatter(x=np.arange(len(kd)), y=kd, mode="lines", line=dict(color="#4C78A8", width=3)))
fig.add_hline(y=0.2, line=dict(color="#E45756", dash="dash", width=2))
fig.add_annotation(x=80, y=0.2, text="the curve bends upward here: eps of about 0.2 or a little more", yshift=14, showarrow=False,
                   font=dict(size=17, color="#E45756"), xanchor="left")
fig.update_layout(xaxis_title="points, sorted by distance", yaxis_title="distance to 5th nearest point (itself included)")
save(fig, "k_distance", 1000, 460, ticks=True)
