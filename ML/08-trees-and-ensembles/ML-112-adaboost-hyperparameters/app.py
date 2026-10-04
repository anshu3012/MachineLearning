"""AdaBoost playground: choose n_estimators, learning_rate and the depth of each tree; see the decision surface
with training and test accuracy. Data: noisy concentric circles, 500 points, 400 for training.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN Note)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
xs = np.linspace(X[:, 0].min() - 0.2, X[:, 0].max() + 0.2, 250)
ys = np.linspace(X[:, 1].min() - 0.2, X[:, 1].max() + 0.2, 250)


def fit(n_estimators=50, learning_rate=1.0, max_depth=1):
    """Train AdaBoost on the training split; return the model and its title with both accuracies."""
    model = AdaBoostClassifier(DecisionTreeClassifier(max_depth=max_depth), n_estimators=n_estimators,
                               learning_rate=learning_rate, random_state=42).fit(X_train, y_train)
    return model, f"train {model.score(X_train, y_train):.2f}, test {model.score(X_test, y_test):.2f}"


def averaged_runs(n_datasets=20, n_estimators=1500, learning_rates=(1.0, 0.1, 0.01), depths=(1, 3, 8)):
    """One split of 100 test points is noisy, so average over n_datasets fresh circles datasets (400 training
    points each), each scored on 5,000 new points from the same distribution.
    Returns {learning_rate: (mean train curve, mean test curve)} over stages, and {depth: (train, test)} for 50 trees."""
    from joblib import Parallel, delayed

    def one(s):
        Xa, ya = make_circles(n_samples=400, factor=0.1, noise=0.35, random_state=s)
        Xb, yb = make_circles(n_samples=5000, factor=0.1, noise=0.35, random_state=1000 + s)
        curves = {}
        for lr in learning_rates:
            m = AdaBoostClassifier(n_estimators=n_estimators, learning_rate=lr, random_state=s).fit(Xa, ya)
            pad = lambda a: np.pad(a, (0, n_estimators - len(a)), mode="edge")   # early stop: hold the last score
            curves[lr] = (pad(np.array(list(m.staged_score(Xa, ya)))), pad(np.array(list(m.staged_score(Xb, yb)))))
        deep = {d: (m.score(Xa, ya), m.score(Xb, yb)) for d in depths
                for m in [AdaBoostClassifier(DecisionTreeClassifier(max_depth=d), n_estimators=50,
                                             random_state=s).fit(Xa, ya)]}
        return curves, deep

    runs = Parallel(n_jobs=-1)(delayed(one)(s) for s in range(n_datasets))
    curves = {lr: tuple(np.mean([r[0][lr][k] for r in runs], axis=0) for k in (0, 1)) for lr in learning_rates}
    deep = {d: tuple(np.mean([r[1][d][k] for r in runs]) for k in (0, 1)) for d in depths}
    return curves, deep


def traces(model, show_legend=False):
    """Decision regions (predicted class on a grid of points, as in the KNN Note) plus the training points."""
    XX, YY = np.meshgrid(xs, ys)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    out = [go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    for cls in (0, 1):
        m = y_train == cls
        out.append(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                              showlegend=show_legend, legendgroup=str(cls),
                              marker=dict(color=COLOURS[cls], size=6, line=dict(color="white", width=0.5))))
    return out


def figure(panels, cols=2):
    """panels: list of (title, model)."""
    rows = -(-len(panels) // cols)
    fig = make_subplots(rows, cols, subplot_titles=[t for t, _ in panels], horizontal_spacing=0.03,
                        vertical_spacing=0.08)
    for i, (_, model) in enumerate(panels):
        for t in traces(model, show_legend=(i == 0)):
            fig.add_trace(t, i // cols + 1, i % cols + 1)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
    fig.update_layout(template="simple_white", height=430 * rows, margin=dict(l=20, r=20, t=60, b=50),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.03))
    return fig


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "700px"}, children=[
    html.H3("AdaBoost classifier"),
    html.Div(["n_estimators", dcc.Slider(1, 1500, 1, value=50, id="n",
                                         marks={v: str(v) for v in (1, 50, 150, 500, 1000, 1500)}, **slider)]),
    html.Div(["learning_rate", dcc.Dropdown([0.01, 0.1, 0.5, 1.0, 2.0], 1.0, id="lr", clearable=False)]),
    html.Div(["max_depth of each tree", dcc.Slider(1, 5, 1, value=1, id="depth", **slider)]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("n", "value"), Input("lr", "value"), Input("depth", "value"))
def update(n, lr, depth):
    model, title = fit(n, lr, depth)
    return figure([(title, model)], cols=1)


if __name__ == "__main__":
    app.run(debug=False)
