"""The elbow curve built one k at a time (Plotly frames -> GIF) on the 272 Old Faithful eruptions (standardized, as
elbow.py). Left: the k-means clusters for the current k. Right: the WCSS of every k tried so far. The curve drops
from 544 to 80 at k = 2 and then flattens: the elbow."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from gifkit import BLUE, FONT, RED, make_gif

here = Path(__file__).parent
COL = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#9D755D"]
df = pd.read_csv(here.parent / "data" / "old_faithful.csv")
X = StandardScaler().fit_transform(df[["duration", "waiting"]])
KS = list(range(1, 7))
fits = {k: KMeans(n_clusters=k, n_init=10, random_state=0).fit(X) for k in KS}
W = [fits[k].inertia_ for k in KS]
assert [round(w) for w in W[:5]] == [544, 80, 56, 44, 34]                  # the Note's numbers


def frame(k, final=False):
    fig = make_subplots(1, 2, horizontal_spacing=0.13, subplot_titles=[f"k = {k}: WCSS {W[k - 1]:.0f}", "WCSS so far"])
    fig.update_annotations(font_size=24)
    for j in range(k):
        m = fits[k].labels_ == j
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(size=8, color=COL[j], opacity=0.8)), 1, 1)
    cen = fits[k].cluster_centers_
    fig.add_trace(go.Scatter(x=cen[:, 0], y=cen[:, 1], mode="markers", marker=dict(size=18, color="black", symbol="x")), 1, 1)
    fig.add_trace(go.Scatter(x=KS[:k], y=W[:k], mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=12)), 1, 2)
    if final:
        fig.add_annotation(x=2, y=W[1], ax=70, ay=-80, text="elbow: k = 2", font=dict(size=22, color=RED), arrowcolor=RED,
                           arrowwidth=3, row=1, col=2)
    fig.update_xaxes(title="duration (standardized)", row=1, col=1)
    fig.update_yaxes(title="waiting time (standardized)", row=1, col=1)
    fig.update_xaxes(title="number of clusters k", range=[0.5, 6.5], dtick=1, row=1, col=2)
    fig.update_yaxes(title="WCSS", range=[0, 590], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False, margin=dict(l=70, r=20, t=60, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in KS] + [frame(2, final=True)]
    figs[-1].data[-1].update(x=KS, y=W)
    make_gif(figs, here / "elbow_build", fps=1, holds=[2] * 6 + [5], keys=[0, 6], cols=1)
