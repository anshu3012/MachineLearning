"""SVM kernel playground: choose the data, the kernel, C, gamma and degree, and watch the decision regions.

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.datasets import make_circles, make_moons
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

COLOURS = ["#4C78A8", "#E45756"]          # class 0 blue, class 1 red
REGION = ["#DCE6F2", "#F9DCDC"]


def make_data(name):
    if name == "moons":
        return make_moons(n_samples=200, noise=0.2, random_state=5)
    return make_circles(n_samples=100, factor=0.1, noise=0.1, random_state=5)


def traces(model, X, y, showlegend=True):
    """Decision regions of a fitted model, the points, and rings around the support vectors."""
    pad = 0.4
    xs = np.linspace(X[:, 0].min() - pad, X[:, 0].max() + pad, 250)
    ys = np.linspace(X[:, 1].min() - pad, X[:, 1].max() + pad, 250)
    XX, YY = np.meshgrid(xs, ys)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    out = [go.Heatmap(x=xs, y=ys, z=Z, showscale=False, hoverinfo="skip", zmin=0, zmax=1,
                      colorscale=[[0, REGION[0]], [1, REGION[1]]])]
    for cls in (0, 1):
        out.append(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", name=f"class {cls}",
                              showlegend=showlegend,
                              marker=dict(color=COLOURS[cls], size=8, line=dict(color="white", width=0.5))))
    sv = model.support_vectors_
    out.append(go.Scatter(x=sv[:, 0], y=sv[:, 1], mode="markers", name="support vectors", showlegend=showlegend,
                          marker=dict(size=14, color="rgba(0,0,0,0)", line=dict(color="black", width=1.5))))
    return out


def figure_for(dataset, kernel, C_exp, gamma_exp, degree):
    X, y = make_data(dataset)
    a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=0)
    model = SVC(kernel=kernel, C=10.0 ** C_exp, gamma=10.0 ** gamma_exp, degree=degree).fit(a, c)
    fig = go.Figure(traces(model, X, y))
    fig.update_layout(template="simple_white", height=560, margin=dict(l=40, r=20, t=60, b=40),
                      yaxis=dict(scaleanchor="x"),
                      title=f"{kernel}: test accuracy {model.score(b, d):.2f}, "
                            f"{len(model.support_vectors_)} support vectors")
    return fig


app = Dash(__name__)
control = {"marginBottom": "14px"}
app.layout = html.Div(style={"fontFamily": "sans-serif", "display": "flex", "gap": "20px", "padding": "16px"}, children=[
    html.Div(style={"width": "270px"}, children=[
        html.H3("SVM kernels"),
        html.Label("Dataset"), dcc.RadioItems(["circles", "moons"], "circles", id="dataset", style=control),
        html.Label("Kernel"), dcc.RadioItems(["linear", "rbf", "poly", "sigmoid"], "rbf", id="kernel", style=control),
        html.Label("C = 10 to the power ..."), dcc.Slider(-3, 3, 0.5, value=0, id="C", marks={i: str(i) for i in range(-3, 4)}),
        html.Label("gamma = 10 to the power ... (rbf, poly, sigmoid)"),
        dcc.Slider(-3, 2, 0.5, value=0, id="gamma", marks={i: str(i) for i in range(-3, 3)}),
        html.Label("degree (poly only)"), dcc.Slider(1, 6, 1, value=3, id="degree"),
    ]),
    dcc.Graph(id="plot", style={"flex": "1"}),
])


@app.callback(Output("plot", "figure"), Input("dataset", "value"), Input("kernel", "value"), Input("C", "value"),
              Input("gamma", "value"), Input("degree", "value"))
def update(dataset, kernel, C_exp, gamma_exp, degree):
    return figure_for(dataset, kernel, C_exp, gamma_exp, degree)


if __name__ == "__main__":
    app.run(debug=False)
