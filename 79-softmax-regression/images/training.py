"""Training softmax regression by gradient descent (Plotly frames -> GIF), on the Note's iris setup (sepal length and
petal length, split test size 0.2, random state 2). All nine weights start at 0 and are updated together on the
categorical cross entropy (full batch, learning rate 0.1, features standardised on the training set). Left: the
decision regions as the weights change. Right: the loss per epoch, falling from log 3 = 1.10."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif

here = Path(__file__).parent
iris = load_iris()
X, y = iris.data[:, [0, 2]], iris.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)
mu, sd = Xtr.mean(0), Xtr.std(0)
A = np.c_[np.ones(len(Xtr)), (Xtr - mu) / sd]
Y = np.eye(3)[ytr]


def softmax(Z):
    E = np.exp(Z - Z.max(1, keepdims=True)); return E / E.sum(1, keepdims=True)


W, hist = np.zeros((3, 3)), []
for e in range(501):
    P = softmax(A @ W)
    hist.append((W.copy(), -np.mean(np.sum(Y * np.log(P), 1))))
    W -= 0.1 * A.T @ (P - Y) / len(A)
acc = lambda W: (softmax(np.c_[np.ones(len(Xte)), (Xte - mu) / sd] @ W).argmax(1) == yte).mean()
assert abs(hist[0][1] - np.log(3)) < 1e-12 and round(hist[-1][1], 2) == 0.31 and round(acc(hist[-1][0]), 3) == 0.933
g1, g2 = np.linspace(4, 8.2, 220), np.linspace(0.8, 7.2, 220)
G1, G2 = np.meshgrid(g1, g2)
GA = np.c_[np.ones(G1.size), (np.c_[G1.ravel(), G2.ravel()] - mu) / sd]
COLS = [BLUE, ORANGE, GREEN]
EP = [0, 1, 3, 10, 30, 100, 250, 500]
loss = np.array([h[1] for h in hist])


def frame(e):
    W = hist[e][0]
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=[f"epoch {e}: test accuracy {acc(W):.3f}", "categorical cross entropy"])
    fig.update_annotations(font_size=21)
    reg = softmax(GA @ W).argmax(1).reshape(G1.shape) if e > 0 else np.full(G1.shape, np.nan)
    fig.add_trace(go.Heatmap(x=g1, y=g2, z=reg, colorscale=[[0, BLUE], [0.5, ORANGE], [1, GREEN]], zmin=0, zmax=2,
                             showscale=False, opacity=0.2), 1, 1)
    for k, n in enumerate(iris.target_names):
        m = ytr == k
        fig.add_trace(go.Scatter(x=Xtr[m, 0], y=Xtr[m, 1], mode="markers", marker=dict(size=7, color=COLS[k]), name=n), 1, 1)
    fig.add_trace(go.Scatter(x=np.arange(e + 1), y=loss[:e + 1], mode="lines", line=dict(color="black", width=3), showlegend=False), 1, 2)
    fig.update_xaxes(title="sepal length (cm)", row=1, col=1)
    fig.update_yaxes(title="petal length (cm)", row=1, col=1)
    fig.update_xaxes(title="epoch", range=[-10, 510], row=1, col=2)
    fig.update_yaxes(range=[0, 1.15], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.27, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=120))
    return fig


if __name__ == "__main__":
    make_gif([frame(e) for e in EP], here / "training", fps=2, holds=[2] + [1] * (len(EP) - 2) + [5], keys=[2, len(EP) - 1], cols=1)
