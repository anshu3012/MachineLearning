"""Bagging regressor playground: pick a base regressor and the bagging settings; see the single model's curve next to
the bagging regressor's, with test R². Data: two Gaussian bumps plus noise, 150 training and 100 test points.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.ensemble import BaggingRegressor
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

rng = np.random.RandomState(0)


def generate(n, noise=0.1):
    """x between -5 and 5; y = two Gaussian bumps (at 0 and at 2) plus noise."""
    x = np.sort(rng.rand(n) * 10 - 5)
    y = np.exp(-x ** 2) + 1.5 * np.exp(-(x - 2) ** 2) + rng.normal(0.0, noise, n)
    return x[:, None], y


X_train, y_train = generate(150)
X_test, y_test = generate(100)
X_line = np.linspace(-5, 5, 500)[:, None]
BASE = {"decision tree": lambda: DecisionTreeRegressor(random_state=0), "SVR": SVR, "KNN": KNeighborsRegressor}


def fit(base, n_estimators=50, max_samples=25, bootstrap=True):
    """Train the single base model and a bagging regressor built from it; return both with test R²."""
    single = BASE[base]().fit(X_train, y_train)
    bag = BaggingRegressor(BASE[base](), n_estimators=n_estimators, max_samples=max_samples, bootstrap=bootstrap,
                           random_state=0).fit(X_train, y_train)
    return (single, r2_score(y_test, single.predict(X_test))), (bag, r2_score(y_test, bag.predict(X_test)))


def figure(panels):
    """panels: list of (title, model, colour), one subplot each."""
    fig = make_subplots(1, len(panels), shared_yaxes=True, horizontal_spacing=0.04,
                        subplot_titles=[t for t, _, _ in panels])
    for i, (_, model, colour) in enumerate(panels, start=1):
        fig.add_trace(go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points",
                                 showlegend=(i == 1), marker=dict(color="#FFD24C", size=7, line=dict(color="black", width=1))),
                      1, i)
        fig.add_trace(go.Scatter(x=X_line.ravel(), y=model.predict(X_line), mode="lines", showlegend=False,
                                 line=dict(color=colour, width=3)), 1, i)
    fig.update_xaxes(title="x")
    fig.update_yaxes(title="y", col=1)
    fig.update_layout(template="simple_white", height=480, margin=dict(l=60, r=20, t=60, b=50))
    return fig


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "1100px"}, children=[
    html.H3("Bagging regressor"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px 32px"}, children=[
        html.Div(["base model", dcc.Dropdown(list(BASE), "decision tree", id="base", clearable=False)]),
        html.Div(["n_estimators", dcc.Slider(1, 500, value=50, id="n", marks={v: str(v) for v in (1, 50, 100, 250, 500)},
                                             **slider)]),
        html.Div(["max_samples (rows per model)", dcc.Slider(25, 150, 25, value=25, id="rows", **slider)]),
        html.Div(["bootstrap (rows with replacement)", dcc.RadioItems(["True", "False"], "True", id="boot", inline=True)]),
    ]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("base", "value"), Input("n", "value"), Input("rows", "value"),
              Input("boot", "value"))
def update(base, n, rows, boot):
    (single, r1), (bag, r2) = fit(base, n, rows, boot == "True")
    return figure([(f"single {base}: test R² {r1:.2f}", single, "#E45756"),
                   (f"bagging: test R² {r2:.2f}", bag, "#4C78A8")])


if __name__ == "__main__":
    app.run(debug=False)
