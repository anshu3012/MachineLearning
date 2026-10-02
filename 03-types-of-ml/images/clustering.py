"""Clustering students by IQ and CGPA with no labels. Example data."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
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
df = pd.DataFrame({"IQ": X[:, 0], "CGPA": X[:, 1], "Group found": [names[k] for k in labels]})

plot = (
    so.Plot(df, x="IQ", y="CGPA", color="Group found")
    .add(so.Dot(pointsize=10))
    .scale(color=["#4C78A8", "#F58518", "#54A24B"])
    .label(title="Clustering: 3 groups found without any labels  (example data)")
    .layout(size=(8.5, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "clustering.png", dpi=200, bbox_inches="tight")
plot.save(here / "clustering.pdf", bbox_inches="tight")
