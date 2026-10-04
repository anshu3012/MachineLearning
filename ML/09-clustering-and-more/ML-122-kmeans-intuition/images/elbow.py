"""Elbow curve: WCSS (inertia) for k = 1 to 10 on the Old Faithful eruptions, standardized (Plotly)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "old_faithful.csv")      # 272 eruptions: duration, waiting
X = StandardScaler().fit_transform(df[["duration", "waiting"]])  # k-means is distance-based
ks = np.arange(1, 11)
wcss = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_ for k in ks]
print(np.round(wcss, 1))
fig = go.Figure(go.Scatter(x=ks, y=wcss, mode="lines+markers", line=dict(color="#4C78A8", width=3), marker=dict(size=10)))
fig.add_trace(go.Scatter(x=[2], y=[wcss[1]], mode="markers", marker=dict(size=22, color="#E45756", symbol="circle-open",
                                                                          line=dict(width=3))))
fig.add_annotation(x=2, y=wcss[1], ax=80, ay=-90, text="elbow: k = 2", font=dict(size=19, color="#E45756"),
                   arrowcolor="#E45756", arrowwidth=2, bgcolor="white")
fig.add_annotation(x=2.1, y=wcss[0] * 0.75, text="steep: each extra<br>cluster helps a lot", showarrow=False, font=dict(size=16))
fig.add_annotation(x=7.5, y=wcss[1] + 0.12 * wcss[0], text="flat: extra clusters<br>barely help", showarrow=False, font=dict(size=16))
fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18),
                  xaxis=dict(title="number of clusters k", dtick=1), yaxis=dict(title="WCSS (inertia)", rangemode="tozero"),
                  margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(here / "elbow.png", scale=2); fig.write_image(here / "elbow.pdf")
