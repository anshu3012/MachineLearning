"""Results of the from-scratch KMeans class (Plotly): four datasets, and a bad versus a good random start."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_blobs

here = Path(__file__).parent
sys.path.insert(0, str(here.parent))
from kmeans import KMeans

FONT = dict(family="Latin Modern Roman", size=17)
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
C4 = [(-5, -5), (5, 5), (-2.5, 2.5), (2.5, -2.5)]
students = pd.read_csv(here.parent / "data" / "student_clustering.csv").values


def add(fig, X, km, labels, r, c):
    for k in range(km.n_clusters):
        m = labels == k
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(color=COLS[k], size=6),
                                 showlegend=False), r, c)
    fig.add_trace(go.Scatter(x=km.centroids[:, 0], y=km.centroids[:, 1], mode="markers", showlegend=False,
                             marker=dict(color="black", size=13, symbol="x")), r, c)


# 1. Four datasets
sets = [(make_blobs(n_samples=100, centers=C4[:n], cluster_std=1, random_state=2)[0], n) for n in (2, 3, 4)]
sets.append((students, 4))
titles = ["2 blobs, k = 2", "3 blobs, k = 3", "4 blobs, k = 4", "students, k = 4"]
fig = make_subplots(rows=2, cols=2, subplot_titles=titles, vertical_spacing=0.12, horizontal_spacing=0.08)
for i, (X, k) in enumerate(sets):
    km = KMeans(n_clusters=k, random_state=3)
    lab = km.fit_predict(X)
    print(titles[i], "rounds:", km.n_iter_)
    add(fig, X, km, lab, i // 2 + 1, i % 2 + 1)
fig.update_xaxes(title_text="CGPA", row=2, col=2); fig.update_yaxes(title_text="IQ", row=2, col=2)
fig.update_layout(template="simple_white", width=1000, height=800, font=FONT, margin=dict(l=60, r=20, t=40, b=50))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=19))
fig.write_image(here / "four_datasets.png", scale=2); fig.write_image(here / "four_datasets.pdf")

# 2. Bad start versus good start on the students
runs = []
for seed in (0, 3):
    km = KMeans(n_clusters=4, max_iter=500, random_state=seed)
    runs.append((km, km.fit_predict(students)))
    print("seed", seed, "rounds", km.n_iter_, "WCSS", round(km.inertia_, 1), np.bincount(runs[-1][1]))
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
    f"bad start: stuck after {runs[0][0].n_iter_} rounds, WCSS {runs[0][0].inertia_:,.0f}",
    f"good start: {runs[1][0].n_iter_} rounds, WCSS {runs[1][0].inertia_:,.0f}"])
for j, (km, lab) in enumerate(runs):
    add(fig, students, km, lab, 1, j + 1)
fig.update_xaxes(title_text="CGPA"); fig.update_yaxes(title_text="IQ")
fig.update_layout(template="simple_white", width=1100, height=470, font=FONT, margin=dict(l=60, r=20, t=50, b=50))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=19))
fig.write_image(here / "bad_start.png", scale=2); fig.write_image(here / "bad_start.pdf")
