"""DBSCAN playground: pick a dataset, move eps and min_samples, and watch the clusters and noise change.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#72B7B2", "#EECA3B", "#9D755D"]
rng = np.random.default_rng(0)
blobs, _ = datasets.make_blobs(n_samples=450, centers=[(-4, 0), (0, 4), (4, 0)], cluster_std=0.8, random_state=1)
DATA = {
    "two moons": datasets.make_moons(500, noise=0.05, random_state=170)[0],
    "two circles": datasets.make_circles(500, factor=0.5, noise=0.05, random_state=170)[0],
    "three groups plus noise": np.vstack([blobs, rng.uniform(-8, 8, (50, 2))]),
    "two densities": datasets.make_blobs(n_samples=[300, 100], centers=[(0, 0), (4, 0)], cluster_std=[0.3, 1.3],
                                         random_state=0)[0],
}
DATA = {k: StandardScaler().fit_transform(v) for k, v in DATA.items()}   # every dataset on the same scale


def figure_for(name, eps, min_samples):
    X = DATA[name]
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
    n_clusters = len(set(labels) - {-1})
    fig = go.Figure()
    for k in sorted(set(labels)):
        m = labels == k
        marker = dict(color="#6B6B6B", symbol="x", size=7) if k == -1 else dict(color=COLS[k % len(COLS)], size=6)
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=marker,
                                 name="noise" if k == -1 else f"cluster {k}"))
    fig.update_layout(template="simple_white", height=560, margin=dict(l=40, r=20, t=60, b=40),
                      title=f"{n_clusters} clusters, {(labels == -1).sum()} noise points",
                      yaxis=dict(scaleanchor="x"))
    return fig


app = Dash(__name__)
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "900px"}, children=[
    html.H3("DBSCAN: choose eps and min_samples"),
    dcc.Dropdown(list(DATA), "two moons", id="data", clearable=False),
    html.Label("eps (radius of the neighbourhood, standardized units)"),
    dcc.Slider(0.05, 1.0, 0.05, value=0.3, id="eps", marks={v: f"{v:g}" for v in (0.05, 0.25, 0.5, 0.75, 1.0)},
               tooltip={"placement": "bottom", "always_visible": True}),
    html.Label("min_samples (points needed within eps, itself included)"),
    dcc.Slider(2, 20, 1, value=5, id="min_samples", marks={v: str(v) for v in (2, 5, 10, 15, 20)},
               tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("data", "value"), Input("eps", "value"), Input("min_samples", "value"))
def update(name, eps, min_samples):
    return figure_for(name, eps, min_samples)


if __name__ == "__main__":
    app.run(debug=False)
