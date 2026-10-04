"""Clustering students by IQ and CGPA with no labels. Example data. Plotly: a scatter coloured by the group found."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans

here = Path(__file__).parent
rng = np.random.default_rng(11)
centres = {"high IQ, high CGPA": (120, 8.8), "high IQ, low CGPA": (118, 6.2), "low IQ, high CGPA": (85, 8.5)}
X = np.vstack([np.column_stack([rng.normal(i, 5, 30), rng.normal(c, 0.35, 30)]) for i, c in centres.values()])

# The algorithm only sees the numbers; it finds the 3 groups itself.
scaled = (X - X.mean(0)) / X.std(0)
labels = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(scaled)
names = {}
for k in range(3):
    centre = X[labels == k].mean(0)
    names[k] = min(centres, key=lambda n: np.hypot((centres[n][0] - centre[0]) / 20, centres[n][1] - centre[1]))
COL = dict(zip(centres, ["#4C78A8", "#F58518", "#54A24B"]))

if __name__ == "__main__":
    fig = go.Figure()
    for k in sorted(names, key=lambda k: list(centres).index(names[k])):
        fig.add_scatter(x=X[labels == k, 0], y=X[labels == k, 1], mode="markers", name=names[k],
                        marker=dict(size=12, color=COL[names[k]]))
    fig.update_layout(template="simple_white", width=950, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text="Clustering: 3 groups found without any labels  (example data)", x=0.5),
                      xaxis=dict(title="IQ", showgrid=True), yaxis=dict(title="CGPA", showgrid=True),
                      legend=dict(title="Group found"), margin=dict(l=80, r=30, t=70, b=70))
    fig.write_image(here / "clustering.png", scale=2)
    fig.write_image(here / "clustering.pdf")
