"""Elbow curve: WCSS (inertia) for k = 1 to 10 on 150 points in three groups (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

here = Path(__file__).parent
X, _ = make_blobs(n_samples=150, centers=[(-1.2, -1.0), (1.3, -0.6), (0.1, 1.3)], cluster_std=0.4, random_state=3)
ks = np.arange(1, 11)
wcss = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_ for k in ks]
print(np.round(wcss, 1))
fig = go.Figure(go.Scatter(x=ks, y=wcss, mode="lines+markers", line=dict(color="#4C78A8", width=3), marker=dict(size=10)))
fig.add_trace(go.Scatter(x=[3], y=[wcss[2]], mode="markers", marker=dict(size=22, color="#E45756", symbol="circle-open",
                                                                          line=dict(width=3))))
fig.add_annotation(x=3, y=wcss[2], ax=80, ay=-90, text="elbow: k = 3", font=dict(size=19, color="#E45756"),
                   arrowcolor="#E45756", arrowwidth=2, bgcolor="white")
fig.add_annotation(x=2.75, y=wcss[0] * 0.75, text="steep: each extra<br>cluster helps a lot", showarrow=False, font=dict(size=16))
fig.add_annotation(x=7.5, y=wcss[2] + 0.12 * wcss[0], text="flat: extra clusters<br>barely help", showarrow=False, font=dict(size=16))
fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18),
                  xaxis=dict(title="number of clusters k", dtick=1), yaxis=dict(title="WCSS (inertia)", rangemode="tozero"),
                  margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(here / "elbow.png", scale=2); fig.write_image(here / "elbow.pdf")
