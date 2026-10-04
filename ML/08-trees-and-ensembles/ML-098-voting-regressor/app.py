"""Voting regressor playground: tick some base regressors and see each one's curve next to the voting regressor's,
with R² and MAE on held-out points.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

COLOURS = {"linear regression": "#54A24B", "SVR": "#E45756", "decision tree": "#B279A2"}

# A noisy sine wave: 80 points, every fifth one pushed up or down
rng = np.random.RandomState(1)
X = np.sort(5 * rng.rand(80, 1), axis=0)
y = np.sin(X).ravel()
y[::5] += 3 * (0.5 - rng.rand(16))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=8)
X_line = np.arange(0.0, 5.0, 0.01)[:, None]           # where each curve is drawn


def base_models(names):
    makers = {"linear regression": LinearRegression, "SVR": SVR,
              "decision tree": lambda: DecisionTreeRegressor(max_depth=5, random_state=0)}
    return [(n, makers[n]()) for n in names]


def run(names):
    """Fit each base model and the voting regressor; return [(name, model, R², MAE)], voting first."""
    vr = VotingRegressor(base_models(names)).fit(X_train, y_train)
    out = [("voting regressor", vr)] + [(n, m.fit(X_train, y_train)) for n, m in base_models(names)]
    return [(n, m, r2_score(y_test, m.predict(X_test)), mean_absolute_error(y_test, m.predict(X_test))) for n, m in out]


def figure(results):
    fig = go.Figure(go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points",
                               marker=dict(color="#FFD24C", size=9, line=dict(color="black", width=1))))
    fig.add_trace(go.Scatter(x=X_test.ravel(), y=y_test, mode="markers", name="test points",
                             marker=dict(color="white", size=9, symbol="diamond", line=dict(color="black", width=1.5))))
    for name, model, r2, mae in results[1:]:
        fig.add_trace(go.Scatter(x=X_line.ravel(), y=model.predict(X_line), mode="lines",
                                 line=dict(color=COLOURS[name], width=2, dash="dashdot"),
                                 name=f"{name}: R² {r2:.2f}, MAE {mae:.2f}"))
    name, model, r2, mae = results[0]
    fig.add_trace(go.Scatter(x=X_line.ravel(), y=model.predict(X_line), mode="lines", line=dict(color="#4C78A8", width=4),
                             name=f"{name}: R² {r2:.2f}, MAE {mae:.2f}"))
    fig.update_layout(template="simple_white", height=520, xaxis_title="x", yaxis_title="y",
                      margin=dict(l=60, r=20, t=30, b=50))
    return fig


app = Dash(__name__)
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "1100px"}, children=[
    html.H3("Voting regressor"),
    dcc.Checklist(list(COLOURS), ["linear regression", "SVR"], id="models", inline=True),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("models", "value"))
def update(models):
    if not models:
        return go.Figure().update_layout(title="pick at least one base model")
    return figure(run(models))


if __name__ == "__main__":
    app.run(debug=False)
