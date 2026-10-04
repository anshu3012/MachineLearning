"""A single neuron on linear and non-linear data (Plotly).
gates.png: scikit-learn's Perceptron on the 4-row AND, OR and XOR tables.
playground.png: one sigmoid neuron (logistic regression) on three TensorFlow-Playground-style datasets."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_blobs, make_circles
from sklearn.linear_model import LogisticRegression, Perceptron

here = Path(__file__).parent
GREEN, RED = "#54A24B", "#E45756"


def panels(data, model, lim, name, size, width):
    fig = make_subplots(rows=1, cols=len(data), horizontal_spacing=0.06,
                        subplot_titles=[f"{t}: accuracy {model().fit(X, y).score(X, y):.0%}" for t, (X, y) in data.items()])
    gx, gy = np.meshgrid(np.linspace(*lim, 300), np.linspace(*lim, 300))
    for c, (X, y) in enumerate(data.values(), start=1):
        m = model().fit(X, y)
        zz = m.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
        fig.add_trace(go.Heatmap(x=gx[0], y=gy[:, 0], z=zz, zmin=0, zmax=1, showscale=False, opacity=0.25,
                                 hoverinfo="skip", colorscale=[[0, RED], [1, GREEN]]), row=1, col=c)
        for label, colour, lab in [(1, GREEN, "output 1"), (0, RED, "output 0")]:
            k = y == label
            fig.add_trace(go.Scatter(x=X[k, 0], y=X[k, 1], mode="markers", name=lab, showlegend=c == 1,
                                     marker=dict(color=colour, size=size, line=dict(color="black", width=1))), row=1, col=c)
        fig.update_xaxes(range=lim, title_text="x1", row=1, col=c)
        fig.update_yaxes(range=lim, title_text="x2" if c == 1 else None, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
    fig.update_layout(template="simple_white", width=width, height=470, font=dict(family="Latin Modern Roman", size=18),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=60, r=20, t=50, b=100))
    fig.update_annotations(font_size=20)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
gates = {"AND": (X, np.array([0, 0, 0, 1])), "OR": (X, np.array([0, 1, 1, 1])), "XOR": (X, np.array([0, 1, 1, 0]))}
panels(gates, lambda: Perceptron(random_state=0), (-0.5, 1.5), "gates", 22, 1200)

rng = np.random.default_rng(0)
Xx = rng.uniform(-5, 5, (400, 2))
Xb, yb = make_blobs(400, centers=[(-2.5, -2.5), (2.5, 2.5)], random_state=0)
Xc, yc = make_circles(400, noise=0.1, factor=0.4, random_state=0)
play = {"Two blobs": (Xb, yb), "XOR quadrants": (Xx, (Xx[:, 0] * Xx[:, 1] > 0).astype(int)), "Circles": (Xc * 4.5, yc)}
panels(play, LogisticRegression, (-6, 6), "playground", 7, 1200)
