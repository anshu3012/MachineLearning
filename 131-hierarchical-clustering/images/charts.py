"""Plotly figures for the hierarchical clustering Note: where k-means fails, the four linkages compared,
the Ward dendrogram of the shopping data with its cut, and the 5 customer clusters."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=17)
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"]


def scatter(fig, X, lab, r, c, size=5):
    for k in np.unique(lab):
        m = lab == k
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=COLS[int(k) % len(COLS)], size=size)), r, c)


def finish(fig, name, w, h):
    fig.update_xaxes(showticklabels=False, ticks=""); fig.update_yaxes(showticklabels=False, ticks="")
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, margin=dict(l=20, r=20, t=50, b=20))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=19))
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# 1. Where k-means fails
n = 500
rng = np.random.default_rng(0)
Xb, _ = datasets.make_blobs(n_samples=450, centers=[(-4, 0), (0, 4), (4, 0)], cluster_std=0.8, random_state=1)
noisy = np.vstack([Xb, rng.uniform(-8, 8, (50, 2))])
X_aniso, _ = datasets.make_blobs(n_samples=n, random_state=170)
sets = [("two circles", datasets.make_circles(n_samples=n, factor=0.5, noise=0.05, random_state=170)[0], 2),
        ("two moons", datasets.make_moons(n_samples=n, noise=0.05, random_state=170)[0], 2),
        ("three stretched groups", X_aniso @ [[0.6, -0.6], [-0.4, 0.8]], 3),
        ("three groups plus noise", noisy, 3)]
fig = make_subplots(rows=2, cols=2, subplot_titles=[s[0] for s in sets], vertical_spacing=0.08, horizontal_spacing=0.05)
for i, (name, X, k) in enumerate(sets):
    lab = KMeans(n_clusters=k, random_state=0).fit_predict(StandardScaler().fit_transform(X))
    scatter(fig, X, lab, i // 2 + 1, i % 2 + 1)
finish(fig, "kmeans_fails", 1000, 860)

# 2. The four linkages on three datasets
Xm, _ = datasets.make_moons(n_samples=n, noise=0.05, random_state=170)
Xn, _ = datasets.make_moons(n_samples=n, noise=0.12, random_state=1)
Xs = np.vstack([rng.normal([0, 0], 1.5, (400, 2)), rng.normal([6, 0], 0.4, (40, 2))])
rows = [("moons, clear gap", Xm), ("moons, noisy", Xn), ("big and small group", Xs)]
links = ["single", "complete", "average", "ward"]
fig = make_subplots(rows=3, cols=4, column_titles=links, row_titles=[r[0] for r in rows],
                    vertical_spacing=0.04, horizontal_spacing=0.02)
for i, (_, X) in enumerate(rows):
    Xsc = StandardScaler().fit_transform(X)
    for j, L in enumerate(links):
        scatter(fig, X, AgglomerativeClustering(n_clusters=2, linkage=L).fit_predict(Xsc), i + 1, j + 1, size=4)
finish(fig, "linkage_compare", 1100, 820)

CUT = 7
# 3. Dendrogram of the shopping data (Ward), drawn from scipy's coordinates
df = pd.read_csv(here.parent / "data" / "shopping_data.csv")
X = df.iloc[:, 3:5].values
Xstd = (X - X.mean(0)) / X.std(0)   # standardized, as StandardScaler does
Z = linkage(Xstd, method="ward")
d = dendrogram(Z, no_plot=True, color_threshold=CUT)
palette = {c: COLS[i % len(COLS)] for i, c in enumerate(sorted(set(d["color_list"]) - {"C0"}))}
palette["C0"] = "#6B6B6B"
fig = go.Figure()
for xs, ys, c in zip(d["icoord"], d["dcoord"], d["color_list"]):
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=palette[c], width=1.6), showlegend=False,
                             hoverinfo="skip"))
heights = np.sort(Z[:, 2])[::-1]
print("top merge heights", heights[:6].round(2))
fig.add_hline(y=CUT, line=dict(color="#E45756", width=3, dash="dash"))
fig.add_annotation(x=1980, y=CUT, text=f"cut at {CUT}: 5 clusters", xanchor="right", yanchor="bottom", showarrow=False,
                   font=dict(size=19, color="#E45756"), bgcolor="white")
fig.add_shape(type="rect", x0=0, x1=2000, y0=heights[4], y1=heights[3], fillcolor="#E45756", opacity=0.08, line_width=0, layer="below")
fig.add_shape(type="rect", x0=0, x1=2000, y0=heights[2], y1=heights[1], fillcolor="#4C78A8", opacity=0.08, line_width=0, layer="below")
fig.add_annotation(x=480, y=(heights[2] + heights[1]) / 2, text=f"gap of {heights[1]-heights[2]:.2f}: a cut here gives 3 clusters",
                   xanchor="left", showarrow=False, font=dict(size=16, color="#4C78A8"))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=80, r=20, t=30, b=40),
                  xaxis=dict(showticklabels=False, ticks="", title="200 customers"),
                  yaxis=dict(title="merge distance (Ward, standardized data)"))
fig.write_image(here / "dendrogram_cut.png", scale=2); fig.write_image(here / "dendrogram_cut.pdf")

# 4. The 5 clusters of customers
lab = AgglomerativeClustering(n_clusters=5, metric="euclidean", linkage="ward").fit_predict(Xstd)
print("customers per cluster", np.bincount(lab))
fig = go.Figure()
for k in range(5):
    m = lab == k
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=f"cluster {k}", marker=dict(color=COLS[k], size=8)))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=20, t=30, b=60),
                  xaxis_title="annual income (thousand dollars)", yaxis_title="spending score (1 to 100)")
fig.write_image(here / "customer_clusters.png", scale=2); fig.write_image(here / "customer_clusters.pdf")
