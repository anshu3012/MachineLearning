"""Bagging classifier playground: pick a base model and the bagging settings; see the single model's decision surface
next to the bagging classifier's, with test accuracies. Data: two moons, 500 points, 375 for training.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

X, y = make_moons(n_samples=500, noise=0.30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN Note)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
BASE = {"decision tree": lambda: DecisionTreeClassifier(random_state=42), "KNN": KNeighborsClassifier,
        "SVM": lambda: SVC(random_state=42)}


def fit(base, n_estimators=100, max_samples=375, bootstrap=True, max_features=2, bootstrap_features=False):
    """Train the single base model and a bagging classifier built from it; return both with test accuracies."""
    single = BASE[base]().fit(X_train, y_train)
    bag = BaggingClassifier(BASE[base](), n_estimators=n_estimators, max_samples=max_samples, bootstrap=bootstrap,
                            max_features=max_features, bootstrap_features=bootstrap_features,
                            random_state=42).fit(X_train, y_train)
    return (single, single.score(X_test, y_test)), (bag, bag.score(X_test, y_test))


xs = np.linspace(X[:, 0].min() - 0.3, X[:, 0].max() + 0.3, 250)
ys = np.linspace(X[:, 1].min() - 0.3, X[:, 1].max() + 0.3, 250)


def traces(model, show_legend=False):
    """Decision regions (predicted class on a meshgrid, as in the KNN Note) plus the training points."""
    XX, YY = np.meshgrid(xs, ys)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    out = [go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    for cls in (0, 1):
        m = y_train == cls
        out.append(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                              showlegend=show_legend, legendgroup=str(cls),
                              marker=dict(color=COLOURS[cls], size=5, line=dict(color="white", width=0.5))))
    return out


def figure(panels, cols=2):
    """panels: list of (title, model)."""
    rows = -(-len(panels) // cols)
    fig = make_subplots(rows, cols, subplot_titles=[t for t, _ in panels], horizontal_spacing=0.05,
                        vertical_spacing=0.1)
    for i, (_, model) in enumerate(panels):
        for t in traces(model, show_legend=(i == 0)):
            fig.add_trace(t, i // cols + 1, i % cols + 1)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
    fig.update_layout(template="simple_white", height=420 * rows, margin=dict(l=20, r=20, t=60, b=40),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.04))
    return fig


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "1100px"}, children=[
    html.H3("Bagging classifier"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px 32px"}, children=[
        html.Div(["base model", dcc.Dropdown(list(BASE), "decision tree", id="base", clearable=False)]),
        html.Div(["n_estimators", dcc.Slider(1, 500, value=100, id="n", marks={v: str(v) for v in (1, 10, 100, 250, 500)},
                                             **slider)]),
        html.Div(["max_samples (rows per model)", dcc.Slider(25, 375, 25, value=375, id="rows", **slider)]),
        html.Div(["bootstrap (rows with replacement)", dcc.RadioItems(["True", "False"], "True", id="boot", inline=True)]),
        html.Div(["max_features (columns per model)", dcc.Slider(1, 2, 1, value=2, id="cols", **slider)]),
        html.Div(["bootstrap_features", dcc.RadioItems(["False", "True"], "False", id="bootf", inline=True)]),
    ]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("base", "value"), Input("n", "value"), Input("rows", "value"),
              Input("boot", "value"), Input("cols", "value"), Input("bootf", "value"))
def update(base, n, rows, boot, cols, bootf):
    (single, a1), (bag, a2) = fit(base, n, rows, boot == "True", cols, bootf == "True")
    return figure([(f"single {base}: test accuracy {a1:.2f}", single), (f"bagging: test accuracy {a2:.2f}", bag)])


if __name__ == "__main__":
    app.run(debug=False)
