"""Decision tree playground: change every main hyperparameter and watch the decision surface and the tree change.
Data: two moons (500 points, 375 for training) or the Social Network Ads data (age, salary).

Run:  python app.py   then open http://127.0.0.1:8050
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

HERE = Path(__file__).parent
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN Note)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]


def load(name):
    """Return X_train, X_test, y_train, y_test, axis names, class names."""
    if name == "moons":
        X, y = make_moons(n_samples=500, noise=0.3, random_state=42)
        return (*train_test_split(X, y, random_state=42), ("x1", "x2"), ("class 0", "class 1"))
    df = pd.read_csv(HERE / "data" / "Social_Network_Ads.csv")
    X, y = df[["Age", "EstimatedSalary"]].values, df["Purchased"].values
    return (*train_test_split(X, y, test_size=0.25, random_state=0), ("age", "estimated salary"),
            ("not purchased", "purchased"))


def grid(X, steps=300):
    """Every point of the plotting area (the meshgrid of the KNN Note)."""
    pad = (X.max(0) - X.min(0)) * 0.05
    xs = np.linspace(X[:, 0].min() - pad[0], X[:, 0].max() + pad[0], steps)
    ys = np.linspace(X[:, 1].min() - pad[1], X[:, 1].max() + pad[1], steps)
    return xs, ys


def fit(name, **params):
    """Train a tree; return it with its data and train/test accuracy."""
    X_train, X_test, y_train, y_test, axes, classes = load(name)
    tree = DecisionTreeClassifier(random_state=42, **params).fit(X_train, y_train)
    return tree, X_train, X_test, y_train, y_test, axes, classes


def traces(tree, X_train, y_train, classes, show_legend=True):
    """Heatmap of the decision regions plus the training points."""
    xs, ys = grid(X_train)
    XX, YY = np.meshgrid(xs, ys)
    Z = tree.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    out = [go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    for cls in (0, 1):
        m = y_train == cls
        out.append(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"{classes[cls]} (training)",
                              showlegend=show_legend, legendgroup=str(cls),
                              marker=dict(color=COLOURS[cls], size=6, line=dict(color="white", width=0.5))))
    return out


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "1200px"}, children=[
    html.H3("Decision tree hyperparameters"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px 32px"}, children=[
        html.Div(["data", dcc.Dropdown(["moons", "social network ads"], "moons", id="data", clearable=False)]),
        html.Div(["criterion", dcc.Dropdown(["gini", "entropy"], "gini", id="criterion", clearable=False)]),
        html.Div(["splitter", dcc.Dropdown(["best", "random"], "best", id="splitter", clearable=False)]),
        html.Div(["max_features (0 = all columns)", dcc.Slider(0, 2, 1, value=0, id="max_features", **slider)]),
        html.Div(["max_depth (0 = None, grow fully)", dcc.Slider(0, 20, 1, value=0, id="max_depth", **slider)]),
        html.Div(["min_samples_split", dcc.Slider(2, 375, 1, value=2, id="min_samples_split",
                                                  marks={v: str(v) for v in (2, 50, 100, 200, 301, 375)}, **slider)]),
        html.Div(["min_samples_leaf", dcc.Slider(1, 200, 1, value=1, id="min_samples_leaf",
                                                 marks={v: str(v) for v in (1, 20, 50, 100, 200)}, **slider)]),
        html.Div(["max_leaf_nodes (0 = no limit)", dcc.Slider(0, 50, 1, value=0, id="max_leaf_nodes",
                                                             marks={v: str(v) for v in (0, 2, 5, 10, 20, 50)}, **slider)]),
        html.Div(["min_impurity_decrease", dcc.Slider(0, 0.2, 0.005, value=0, id="min_impurity_decrease",
                                                      marks={v: str(v) for v in (0, 0.01, 0.05, 0.1, 0.2)}, **slider)]),
    ]),
    dcc.Graph(id="plot"),
    html.Pre(id="tree", style={"fontSize": "12px", "maxHeight": "400px", "overflow": "auto", "background": "#f6f6f6"}),
])


@app.callback(Output("plot", "figure"), Output("tree", "children"),
              Input("data", "value"), Input("criterion", "value"), Input("splitter", "value"),
              Input("max_features", "value"), Input("max_depth", "value"), Input("min_samples_split", "value"),
              Input("min_samples_leaf", "value"), Input("max_leaf_nodes", "value"), Input("min_impurity_decrease", "value"))
def update(data, criterion, splitter, max_features, max_depth, min_samples_split, min_samples_leaf, max_leaf_nodes, mid):
    name = "moons" if data == "moons" else "ads"
    tree, X_train, X_test, y_train, y_test, axes, classes = fit(
        name, criterion=criterion, splitter=splitter, max_features=max_features or None, max_depth=max_depth or None,
        min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
        max_leaf_nodes=max_leaf_nodes if max_leaf_nodes >= 2 else None, min_impurity_decrease=mid)
    fig = go.Figure(traces(tree, X_train, y_train, classes))
    fig.update_layout(template="simple_white", height=560, margin=dict(l=60, r=20, t=60, b=50),
                      title=f"depth {tree.get_depth()}, {tree.get_n_leaves()} leaves   |   "
                            f"train accuracy {tree.score(X_train, y_train):.3f}, test accuracy {tree.score(X_test, y_test):.3f}",
                      xaxis_title=axes[0], yaxis_title=axes[1])
    return fig, export_text(tree, feature_names=list(axes), show_weights=True)


if __name__ == "__main__":
    app.run(debug=False)
