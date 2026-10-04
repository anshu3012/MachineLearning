"""Random forest playground: change the four forest-level hyperparameters (n_estimators, max_features, bootstrap,
max_samples) and see the decision surface and test accuracy. Data: concentric circles, 500 points, 375 for training.

Run:  python app.py   then open http://127.0.0.1:8050
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv(Path(__file__).parent / "data" / "concertriccir2.csv")
X, y = df.iloc[:, :2].values, df.iloc[:, -1].values.astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)       # 375 training, 125 test rows
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN Note)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]


def fit(n_estimators=100, max_features="sqrt", bootstrap=True, max_samples=None):
    """Train a random forest; return it with its test accuracy. max_samples only applies when bootstrap=True."""
    rf = RandomForestClassifier(n_estimators=n_estimators, max_features=max_features, bootstrap=bootstrap,
                                max_samples=max_samples if bootstrap else None, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    return rf, rf.score(X_test, y_test)


xs = np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 250)
ys = np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 250)


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
    fig = make_subplots(rows, cols, subplot_titles=[t for t, _ in panels], horizontal_spacing=0.04,
                        vertical_spacing=0.1)
    for i, (_, model) in enumerate(panels):
        for t in traces(model, show_legend=(i == 0)):
            fig.add_trace(t, i // cols + 1, i % cols + 1)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
    fig.update_layout(template="simple_white", height=480 * rows, margin=dict(l=20, r=20, t=60, b=40),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.04))
    return fig


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "900px"}, children=[
    html.H3("Random forest classifier"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px 32px"}, children=[
        html.Div(["n_estimators (trees)", dcc.Slider(1, 300, value=100, id="n",
                                                     marks={v: str(v) for v in (1, 50, 100, 200, 300)}, **slider)]),
        html.Div(["max_features (columns per split)", dcc.RadioItems(["sqrt", "log2", "1", "2"], "sqrt", id="mf",
                                                                     inline=True)]),
        html.Div(["bootstrap", dcc.RadioItems(["True", "False"], "True", id="boot", inline=True)]),
        html.Div(["max_samples (rows per tree, only with bootstrap)",
                  dcc.Slider(25, 375, 25, value=375, id="rows", **slider)]),
    ]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("n", "value"), Input("mf", "value"), Input("boot", "value"),
              Input("rows", "value"))
def update(n, mf, boot, rows):
    rf, acc = fit(n, int(mf) if mf.isdigit() else mf, boot == "True", rows)
    return figure([(f"random forest: test accuracy {acc:.3f}", rf)], cols=1)


if __name__ == "__main__":
    app.run(debug=False)
