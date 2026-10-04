"""Logistic regression playground: change the hyperparameters and watch the decision regions.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import warnings

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.datasets import make_blobs, make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

warnings.simplefilter("ignore")
COLOURS = ["#4C78A8", "#F58518", "#54A24B"]
REGION = ["#DCE6F2", "#FDE5CC", "#DDEFD9"]


def make_data(name):
    if name == "binary":
        return make_classification(n_samples=300, n_features=2, n_informative=2, n_redundant=0,
                                   n_clusters_per_class=1, class_sep=0.8, random_state=1)
    return make_blobs(n_samples=300, centers=3, cluster_std=1.6, random_state=7)


def figure_for(dataset, penalty, C_exp, solver, l1_ratio, max_iter):
    X, y = make_data(dataset)
    a, b, c, d = train_test_split(X, y, test_size=0.3, random_state=0)
    ratio = {"none": 0.0, "l2": 0.0, "l1": 1.0, "elasticnet": l1_ratio}[penalty]
    C = np.inf if penalty == "none" else 10.0 ** C_exp
    try:
        model = LogisticRegression(C=C, l1_ratio=ratio, solver=solver, max_iter=max_iter).fit(a, c)
    except ValueError as err:                       # some solver / penalty pairs are not allowed
        fig = go.Figure()
        fig.add_annotation(text=f"Not allowed: {err}", x=0.5, y=0.5, xref="paper", yref="paper",
                           showarrow=False, font=dict(size=14, color="#E45756"))
        fig.update_layout(template="simple_white", height=520, xaxis_visible=False, yaxis_visible=False)
        return fig
    xs = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 250)
    ys = np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 250)
    XX, YY = np.meshgrid(xs, ys)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    k = len(np.unique(y))
    fig = go.Figure(go.Heatmap(x=xs, y=ys, z=Z, showscale=False, hoverinfo="skip",
                               colorscale=[[i / max(k - 1, 1), REGION[i]] for i in range(k)]))
    for cls in range(k):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", name=f"class {cls}",
                                 marker=dict(color=COLOURS[cls], size=7, line=dict(color="white", width=0.5))))
    coefs = ", ".join(f"{v:.2f}" for v in np.ravel(model.coef_))
    fig.update_layout(template="simple_white", height=520, margin=dict(l=40, r=20, t=60, b=40),
                      title=f"test accuracy {model.score(b, d):.3f} | C = {C:g} | coefficients: {coefs}")
    return fig


app = Dash(__name__)
control = {"marginBottom": "14px"}
app.layout = html.Div(style={"fontFamily": "sans-serif", "display": "flex", "gap": "20px", "padding": "16px"}, children=[
    html.Div(style={"width": "260px"}, children=[
        html.H3("Logistic regression"),
        html.Label("Dataset"), dcc.RadioItems(["binary", "three classes"], "binary", id="dataset", style=control),
        html.Label("Penalty"), dcc.Dropdown(["none", "l2", "l1", "elasticnet"], "l2", id="penalty", clearable=False, style=control),
        html.Label("C = 10 to the power ..."), dcc.Slider(-3, 3, 0.5, value=0, id="C", marks={i: str(i) for i in range(-3, 4)}),
        html.Label("Solver"), dcc.Dropdown(["lbfgs", "newton-cg", "newton-cholesky", "liblinear", "sag", "saga"], "lbfgs",
                                           id="solver", clearable=False, style=control),
        html.Label("l1_ratio (Elastic Net only)"), dcc.Slider(0, 1, 0.1, value=0.5, id="l1_ratio"),
        html.Label("max_iter"), dcc.Slider(10, 1000, 10, value=100, id="max_iter", marks={10: "10", 500: "500", 1000: "1000"}),
    ]),
    dcc.Graph(id="plot", style={"flex": "1"}),
])


@app.callback(Output("plot", "figure"), Input("dataset", "value"), Input("penalty", "value"), Input("C", "value"),
              Input("solver", "value"), Input("l1_ratio", "value"), Input("max_iter", "value"))
def update(dataset, penalty, C_exp, solver, l1_ratio, max_iter):
    return figure_for("binary" if dataset == "binary" else "three", penalty, C_exp, solver, l1_ratio, max_iter)


if __name__ == "__main__":
    app.run(debug=False)
