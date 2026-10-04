"""DBSCAN on the two moons of Figure 1 (500 points, standardized) as eps grows, MinPts fixed at 5 (Plotly frames ->
GIF). Left: the clusters (grey crosses: noise). Right: the number of clusters and of noise points for every eps
tried so far. Too small an eps: many small clusters and much noise; eps = 0.3: the two moons; too large: one cluster."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import datasets
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from gifkit import BLUE, FONT, GREY, make_gif

here = Path(__file__).parent
X = StandardScaler().fit_transform(datasets.make_moons(500, noise=0.05, random_state=170)[0])
EPS = [0.05, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
LAB = [DBSCAN(eps=e, min_samples=5).fit(X).labels_ for e in EPS]
NC = [len(set(l)) - (1 if -1 in l else 0) for l in LAB]
NN = [int((l == -1).sum()) for l in LAB]
assert NC[EPS.index(0.3)] == 2 and NN[EPS.index(0.3)] == 0 and NC[-1] == 1 and NC[0] > 10
PAL = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#9D755D", "#E45756", "#72B7B2", "#EECA3B", "#FF9DA6", "#BAB0AC"]


def frame(k):
    lab = LAB[k]
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=[f"eps = {EPS[k]}: {NC[k]} cluster{'s' if NC[k] != 1 else ''}, {NN[k]} noise points", "number of clusters so far"])
    fig.update_annotations(font_size=23)
    m = lab == -1
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(size=7, color=GREY, symbol="x"), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=X[~m, 0], y=X[~m, 1], mode="markers", showlegend=False,
                             marker=dict(size=8, color=[PAL[c % len(PAL)] for c in lab[~m]])), 1, 1)
    xs = [str(e) for e in EPS]
    fig.add_trace(go.Scatter(x=xs[:k + 1], y=NC[:k + 1], mode="lines+markers", name="clusters", line=dict(color=BLUE, width=4),
                             marker=dict(size=11)), 1, 2)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)
    fig.update_xaxes(title="eps", type="category", categoryorder="array", categoryarray=xs, range=[-0.5, len(EPS) - 0.5], tickangle=0, tickfont=dict(size=17), row=1, col=2)
    fig.update_yaxes(title="clusters", range=[0, max(NC) * 1.15], row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=520, font=FONT, margin=dict(l=20, r=30, t=70, b=70), showlegend=False)
    return fig


if __name__ == "__main__":
    print(list(zip(EPS, NC, NN)))
    n = len(EPS)
    make_gif([frame(k) for k in range(n)], here / "eps_sweep", fps=1, holds=[2] * (n - 1) + [4], keys=[1, n - 1], cols=1)
