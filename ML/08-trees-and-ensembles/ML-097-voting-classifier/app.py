"""Voting classifier playground: pick a dataset, some base models and hard or soft voting; see every model's
decision surface next to the voting classifier's, with test accuracies.

Run:  python app.py   then open http://127.0.0.1:8050
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

HERE = Path(__file__).parent
DATASETS = {"concentric circles": "concertriccir2.csv", "U-shaped": "ushape.csv", "linearly separable": "linearsep.csv",
            "outlier": "outlier.csv", "two spirals": "twoSpirals.csv", "XOR": "xor.csv"}
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN Note)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]


def load(name):
    """Return X_train, X_test, y_train, y_test (80/20 split). Labels -1/1 are mapped to 0/1."""
    df = pd.read_csv(HERE / "data" / DATASETS[name])
    X, y = df[["X", "Y"]].values, (df["class"].values > 0).astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42)


def base_models(names):
    """(name, model) pairs. The SVM is wrapped in CalibratedClassifierCV so it can give probabilities (soft voting needs them)."""
    makers = {"KNN": lambda: KNeighborsClassifier(),
              "logistic regression": lambda: LogisticRegression(random_state=42),
              "Gaussian naive Bayes": lambda: GaussianNB(),
              "SVM": lambda: CalibratedClassifierCV(SVC(random_state=42), ensemble=False),
              "random forest": lambda: RandomForestClassifier(n_estimators=100, random_state=42)}
    return [(n, makers[n]()) for n in names]


def run(name, names, voting):
    """Train each base model and the voting classifier; return [(title, model, test accuracy)], data."""
    X_train, X_test, y_train, y_test = load(name)
    out = []
    vc = VotingClassifier(estimators=base_models(names), voting=voting).fit(X_train, y_train)
    out.append((f"voting ({voting})", vc, vc.score(X_test, y_test)))
    for n, model in base_models(names):
        model.fit(X_train, y_train)
        out.append((n, model, model.score(X_test, y_test)))
    return out, X_train, y_train


def grid(X, steps=200):
    pad = (X.max(0) - X.min(0)) * 0.08
    return (np.linspace(X[:, 0].min() - pad[0], X[:, 0].max() + pad[0], steps),
            np.linspace(X[:, 1].min() - pad[1], X[:, 1].max() + pad[1], steps))


def traces(model, X_train, y_train, show_legend=False):
    """Decision regions (predicted class on a meshgrid, as in the KNN Note) plus the training points."""
    xs, ys = grid(X_train)
    XX, YY = np.meshgrid(xs, ys)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    out = [go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    for cls in (0, 1):
        m = y_train == cls
        out.append(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                              showlegend=show_legend, legendgroup=str(cls),
                              marker=dict(color=COLOURS[cls], size=5, line=dict(color="white", width=0.5))))
    return out


def figure(results, X_train, y_train, cols=3):
    rows = -(-len(results) // cols)
    fig = make_subplots(rows, cols, subplot_titles=[f"{t}: {a:.2f}" for t, _, a in results],
                        horizontal_spacing=0.05, vertical_spacing=0.12)
    for i, (_, model, _) in enumerate(results):
        for t in traces(model, X_train, y_train, show_legend=(i == 0)):
            fig.add_trace(t, i // cols + 1, i % cols + 1)
    xs, ys = grid(X_train)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
    fig.update_layout(template="simple_white", height=330 * rows, margin=dict(l=20, r=20, t=50, b=20),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.03))
    return fig


app = Dash(__name__)
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "1200px"}, children=[
    html.H3("Voting classifier"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 2fr 1fr", "gap": "16px"}, children=[
        html.Div(["dataset", dcc.Dropdown(list(DATASETS), "concentric circles", id="data", clearable=False)]),
        html.Div(["base models", dcc.Checklist(["KNN", "logistic regression", "Gaussian naive Bayes", "SVM",
                                                "random forest"],
                                               ["logistic regression", "Gaussian naive Bayes", "random forest"],
                                               id="models", inline=True)]),
        html.Div(["voting", dcc.RadioItems(["hard", "soft"], "hard", id="voting", inline=True)]),
    ]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("data", "value"), Input("models", "value"), Input("voting", "value"))
def update(data, models, voting):
    if not models:
        return go.Figure().update_layout(title="pick at least one base model")
    return figure(*run(data, models, voting))


if __name__ == "__main__":
    app.run(debug=False)
