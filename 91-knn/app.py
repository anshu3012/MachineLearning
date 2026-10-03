"""KNN playground: move the k slider and watch the decision surface change.
Data: the first two columns of the breast cancer data (mean radius, mean texture).

Run:  python app.py   then open http://127.0.0.1:8050
"""
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

COLOURS = {0: "#F58518", 1: "#4C78A8"}            # 0 = malignant (orange), 1 = benign (blue)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
NAMES = {0: "malignant", 1: "benign"}

data = load_breast_cancer()
X, y = data.data[:, :2], data.target              # mean radius, mean texture
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
xs = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 300)
ys = np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 300)


def surface(k):
    """Train KNN with k neighbours; return the predicted class at every grid point and the test accuracy."""
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_train, y_train)
    XX, YY = np.meshgrid(xs, ys)                  # every point of the plotting area
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    return Z, model.score(X_test, y_test)


def traces(k, show_legend=True):
    """Heatmap of the decision regions plus the training points."""
    Z, acc = surface(k)
    out = [go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    for cls in (0, 1):
        m = y_train == cls
        out.append(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"{NAMES[cls]} (training)",
                              showlegend=show_legend, legendgroup=str(cls),
                              marker=dict(color=COLOURS[cls], size=6, line=dict(color="white", width=0.5))))
    return out, acc


def figure_for(k):
    data_traces, acc = traces(k)
    fig = go.Figure(data_traces)
    fig.update_layout(template="simple_white", height=560, margin=dict(l=60, r=20, t=60, b=50),
                      title=f"k = {k}   |   test accuracy {acc:.3f}",
                      xaxis=dict(title="mean radius", range=[xs[0], xs[-1]]),
                      yaxis=dict(title="mean texture", range=[ys[0], ys[-1]]))
    return fig


app = Dash(__name__)
app.layout = html.Div(style={"fontFamily": "sans-serif", "padding": "16px", "maxWidth": "900px"}, children=[
    html.H3("K-nearest neighbours: choose k"),
    dcc.Slider(1, len(X_train), 1, value=5, id="k", marks={v: str(v) for v in (1, 5, 20, 50, 100, 200, 300, len(X_train))},
               tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Graph(id="plot"),
])


@app.callback(Output("plot", "figure"), Input("k", "value"))
def update(k):
    return figure_for(k)


if __name__ == "__main__":
    app.run(debug=False)
