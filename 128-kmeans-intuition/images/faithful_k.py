"""Section 5.4: k-means on the 272 Old Faithful eruptions (standardized, as elbow.py) with k = 2 (the elbow) and
k = 3. With k = 2 the clusters match the dataset's short and long eruptions; k = 3 cuts one real group in two.
Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
COL = ["#4C78A8", "#F58518", "#54A24B"]
df = pd.read_csv(here.parent / "data" / "old_faithful.csv")
X = StandardScaler().fit_transform(df[["duration", "waiting"]])
fits = {k: KMeans(n_clusters=k, n_init=10, random_state=0).fit(X) for k in (2, 3)}
assert round(fits[2].inertia_) == 80 and round(fits[3].inertia_) == 56          # the elbow curve's values
lab2 = pd.Series(fits[2].labels_)
agree = max((lab2.map({0: "short", 1: "long"}) == df.kind).mean(), (lab2.map({1: "short", 0: "long"}) == df.kind).mean())
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, shared_yaxes=True,
                    subplot_titles=(f"k = 2: WCSS 80; matches the short/long label for {agree:.0%}", "k = 3: WCSS 56; one group cut in two"))
for c, k in enumerate((2, 3), start=1):
    for j in range(k):
        m = fits[k].labels_ == j
        fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(size=7, color=COL[j], opacity=0.8), showlegend=False, row=1, col=c)
    cen = fits[k].cluster_centers_
    fig.add_scatter(x=cen[:, 0], y=cen[:, 1], mode="markers", marker=dict(size=18, color="black", symbol="x"), showlegend=False, row=1, col=c)
    fig.update_xaxes(title="duration (standardized)", row=1, col=c)
fig.update_yaxes(title="waiting time (standardized)", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "faithful_k.png", scale=2)
fig.write_image(here / "faithful_k.pdf")
print(agree)
