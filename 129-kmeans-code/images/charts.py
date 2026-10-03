"""Figures for the k-means in Python Note (Plotly): elbow curve and clusters of the 200 students, and k-means on 3-D blobs."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
df = pd.read_csv(here.parent / "data" / "student_clustering.csv")
X = df.values

# 1. Elbow curve on the students
ks = np.arange(1, 11)
wcss = [KMeans(n_clusters=k, random_state=0).fit(X).inertia_ for k in ks]
print("students WCSS", np.round(wcss, 1))
fig = go.Figure(go.Scatter(x=ks, y=wcss, mode="lines+markers", line=dict(color="#4C78A8", width=3), marker=dict(size=10)))
fig.add_trace(go.Scatter(x=[4], y=[wcss[3]], mode="markers",
                         marker=dict(size=22, color="#E45756", symbol="circle-open", line=dict(width=3))))
fig.add_annotation(x=4, y=wcss[3], ax=70, ay=-110, text="elbow: k = 4", font=dict(size=19, color="#E45756"),
                   arrowcolor="#E45756", arrowwidth=2, bgcolor="white")
fig.update_layout(template="simple_white", width=1000, height=480, showlegend=False, font=FONT,
                  xaxis=dict(title="number of clusters k", dtick=1), yaxis=dict(title="WCSS (inertia_)", rangemode="tozero"),
                  margin=dict(l=90, r=30, t=30, b=60))
fig.write_image(here / "elbow_students.png", scale=2); fig.write_image(here / "elbow_students.pdf")

# 2. The students before and after clustering with k = 4
km = KMeans(n_clusters=4, random_state=0)
y = km.fit_predict(X)
order = np.lexsort((km.cluster_centers_[:, 1], -km.cluster_centers_[:, 0]))   # fixed colour order
names = {}
for c in range(4):
    cg, iq = km.cluster_centers_[c]
    names[c] = ("high" if cg > 7 else "low") + " CGPA, " + ("high" if iq > 102 else "low") + " IQ"
fig = make_subplots(rows=1, cols=2, subplot_titles=("the data", "4 clusters found by k-means"), horizontal_spacing=0.1)
fig.add_trace(go.Scatter(x=df.cgpa, y=df.iq, mode="markers", marker=dict(color="#6B6B6B", size=7), showlegend=False), 1, 1)
for i, c in enumerate(order):
    m = y == c
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(color=COLS[i], size=7), name=names[c]), 1, 2)
fig.add_trace(go.Scatter(x=km.cluster_centers_[:, 0], y=km.cluster_centers_[:, 1], mode="markers", name="centroid",
                         marker=dict(color="black", size=16, symbol="x")), 1, 2)
fig.update_xaxes(title="CGPA"); fig.update_yaxes(title="IQ")
fig.update_layout(template="simple_white", width=1100, height=500, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=20))
fig.write_image(here / "student_clusters.png", scale=2); fig.write_image(here / "student_clusters.pdf")

# 3. k-means on 3-D blobs
centres = [(-5, -5, 5), (5, 5, -5), (3.5, -2.5, 4), (-2.5, 2.5, -4)]
X3, _ = make_blobs(n_samples=200, centers=centres, cluster_std=1, n_features=3, random_state=1)
w3 = [KMeans(n_clusters=k, random_state=0).fit(X3).inertia_ for k in range(1, 21)]
print("3-D WCSS", np.round(w3[:8], 1))
y3 = KMeans(n_clusters=4, random_state=0).fit_predict(X3)
fig = go.Figure([go.Scatter3d(x=X3[y3 == c, 0], y=X3[y3 == c, 1], z=X3[y3 == c, 2], mode="markers", name=f"cluster {c}",
                              marker=dict(size=4, color=COLS[c])) for c in range(4)])
fig.update_layout(width=900, height=700, font=FONT, margin=dict(l=0, r=0, t=0, b=0), legend=dict(x=0.8, y=0.9),
                  scene=dict(xaxis_title="col1", yaxis_title="col2", zaxis_title="col3",
                             camera=dict(eye=dict(x=1.6, y=1.4, z=0.9))))
fig.write_image(here / "blobs_3d.png", scale=2); fig.write_image(here / "blobs_3d.pdf")
