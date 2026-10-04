"""min_samples_leaf from 1 to 150 on the moons training data (Plotly frames -> GIF), the Notebook's split. Left: the
decision surface; right: number of leaves, training and test accuracy so far. A bigger minimum leaf size means
fewer, bigger leaves: the surface smooths out, then becomes too coarse."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif

here = Path(__file__).parent
X, y = make_moons(n_samples=500, noise=0.3, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=42)
L = [1, 2, 5, 10, 20, 40, 70, 100, 150]
M = {l: DecisionTreeClassifier(min_samples_leaf=l, random_state=42).fit(Xtr, ytr) for l in L}
assert M[100].get_n_leaves() == 3 and M[20].get_n_leaves() == 11 and M[1].get_n_leaves() == 43
g1, g2 = np.linspace(-2, 3, 250), np.linspace(-1.6, 2.1, 200)
G1, G2 = np.meshgrid(g1, g2)
grid = np.c_[G1.ravel(), G2.ravel()]
tr = [M[l].score(Xtr, ytr) for l in L]; te = [M[l].score(Xte, yte) for l in L]; nl = [M[l].get_n_leaves() for l in L]


def frame(i):
    l = L[i]
    fig = make_subplots(1, 2, horizontal_spacing=0.1, specs=[[{}, {"secondary_y": True}]],
                        subplot_titles=[f"min_samples_leaf = {l}: {nl[i]} leaves", "accuracy and number of leaves"])
    fig.update_annotations(font_size=21)
    fig.add_trace(go.Heatmap(x=g1, y=g2, z=M[l].predict(grid).reshape(G1.shape), colorscale=[[0, ORANGE], [1, BLUE]],
                             showscale=False, opacity=0.35), 1, 1)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        k = ytr == cls
        fig.add_trace(go.Scatter(x=Xtr[k, 0], y=Xtr[k, 1], mode="markers", marker=dict(size=5, color=c), showlegend=False), 1, 1)
    xs = [str(v) for v in L[:i + 1]]
    fig.add_trace(go.Scatter(x=xs, y=tr[:i + 1], mode="lines+markers", name="train accuracy", line=dict(color=BLUE, width=3)), 1, 2)
    fig.add_trace(go.Scatter(x=xs, y=te[:i + 1], mode="lines+markers", name="test accuracy", line=dict(color=ORANGE, width=3)), 1, 2)
    fig.add_trace(go.Bar(x=xs, y=nl[:i + 1], name="leaves", marker_color=GREEN, opacity=0.3), 1, 2, secondary_y=True)
    fig.update_xaxes(categoryorder="array", categoryarray=[str(v) for v in L], title="min_samples_leaf", row=1, col=2)
    fig.update_yaxes(range=[0.75, 1.01], title="accuracy", row=1, col=2, secondary_y=False)
    fig.update_yaxes(range=[0, 50], dtick=10, title="leaves", row=1, col=2, secondary_y=True)
    fig.update_xaxes(showticklabels=False, row=1, col=1); fig.update_yaxes(showticklabels=False, row=1, col=1)
    fig.update_layout(template="simple_white", width=1200, height=540, font=FONT,
                      legend=dict(orientation="h", x=0.75, xanchor="center", y=-0.18), margin=dict(l=40, r=60, t=60, b=110))
    return fig


if __name__ == "__main__":
    make_gif([frame(i) for i in range(len(L))], here / "leaf_sweep", fps=1, holds=[2] + [1] * (len(L) - 2) + [4], keys=[len(L) - 1], cols=1)

