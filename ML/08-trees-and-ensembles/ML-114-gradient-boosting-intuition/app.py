"""Gradient boosting playground: choose the number of trees, the learning rate and the leaves per tree; see the
ensemble's curve on the noisy quadratic data and its training and test error.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.tree import DecisionTreeRegressor

# 100 training points on y = 3x^2 plus a little noise (the same recipe as the reference code), and 100 test points
rng = np.random.RandomState(42)
X = rng.rand(100, 1) - 0.5
y = 3 * X[:, 0] ** 2 + 0.05 * rng.randn(100)
X_test = rng.rand(100, 1) - 0.5
y_test = 3 * X_test[:, 0] ** 2 + 0.05 * rng.randn(100)
GRID = np.linspace(-0.5, 0.5, 500).reshape(-1, 1)
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=18)


def boost(n_trees=3, learning_rate=1.0, max_leaf_nodes=8):
    """Gradient boosting for squared error, written out: start at the mean, then each tree fits the residuals."""
    f0 = y.mean()                                   # stage 1: the mean of the target
    pred = np.full(len(y), f0)                      # current prediction for every training row
    trees = []
    for _ in range(n_trees):
        residual = y - pred                         # pseudo-residual: actual minus predicted
        tree = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=42).fit(X, residual)
        pred = pred + learning_rate * tree.predict(X)   # add the tree's correction, scaled by the learning rate
        trees.append(tree)
    return f0, trees


def predict(f0, trees, learning_rate, X_new):
    """F0 + learning_rate * (tree 1 + tree 2 + ...)."""
    return f0 + learning_rate * sum((t.predict(X_new) for t in trees), np.zeros(len(X_new)))


def mse(a, b):
    return float(np.mean((a - b) ** 2))


def figure(n_trees=3, learning_rate=1.0, max_leaf_nodes=8):
    f0, trees = boost(n_trees, learning_rate, max_leaf_nodes)
    train = mse(y, predict(f0, trees, learning_rate, X))
    test = mse(y_test, predict(f0, trees, learning_rate, X_test))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X[:, 0], y=y, mode="markers", name="training data", marker=dict(color=BLUE, size=7)))
    fig.add_trace(go.Scatter(x=GRID[:, 0], y=predict(f0, trees, learning_rate, GRID), mode="lines",
                             name="ensemble", line=dict(color=RED, width=3)))
    fig.update_layout(template="simple_white", font=FONT, height=480, margin=dict(l=60, r=20, t=60, b=50),
                      title=f"{n_trees} trees: training MSE {train:.4f}, test MSE {test:.4f}",
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15))
    fig.update_xaxes(title="x")
    fig.update_yaxes(title="y", range=[-0.2, 0.9])
    return fig


app = Dash(__name__)
slider = dict(tooltip={"placement": "bottom", "always_visible": True})
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "760px"}, children=[
    html.H3("Gradient boosting regression"),
    html.Div(["number of trees", dcc.Slider(0, 100, 1, value=3, id="n",
                                            marks={v: str(v) for v in (0, 1, 2, 5, 10, 25, 50, 100)}, **slider)]),
    html.Div(["learning rate", dcc.Dropdown([0.05, 0.1, 0.3, 0.5, 1.0], 1.0, id="lr", clearable=False)]),
    html.Div(["max_leaf_nodes of each tree", dcc.Slider(2, 32, 1, value=8, id="leaves",
                                                         marks={v: str(v) for v in (2, 8, 16, 32)}, **slider)]),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("n", "value"), Input("lr", "value"), Input("leaves", "value"))
def update(n, lr, leaves):
    return figure(n, lr, leaves)


if __name__ == "__main__":
    app.run(debug=False)
