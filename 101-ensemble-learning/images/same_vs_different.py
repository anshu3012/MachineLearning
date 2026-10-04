"""Section 3.1: base models must differ. Same two-moons split as why_it_works.py.
Left: three copies of the same depth-3 tree on the same data: one boundary, so the vote is the tree (0.875).
Right: three different algorithms (logistic regression, depth-3 tree, KNN k = 5): the vote scores 0.890.
Run: python same_vs_different.py  -> same_vs_different.png (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"
X, y = make_moons(n_samples=400, noise=0.35, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
tree = lambda: DecisionTreeClassifier(max_depth=3, random_state=0)
crowds = {"three copies of one tree": [tree().fit(X_tr, y_tr) for _ in range(3)],
          "three different algorithms": [m.fit(X_tr, y_tr) for m in (LogisticRegression(), tree(),
                                                                     KNeighborsClassifier(5))]}
xs, ys = np.linspace(-2, 3, 300), np.linspace(-1.6, 2.1, 300)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
vote_acc = {k: ((sum(m.predict(X_te) for m in ms) >= 2) == y_te).mean() for k, ms in crowds.items()}
assert round(vote_acc["three copies of one tree"], 3) == 0.875 and round(vote_acc["three different algorithms"], 3) == 0.89
print(vote_acc)

fig = make_subplots(1, 2, horizontal_spacing=0.06, subplot_titles=[
    f"{k}: vote scores {v:.3f}" for k, v in vote_acc.items()])
for col, (name, ms) in enumerate(crowds.items(), 1):
    Zs = [m.predict(grid).reshape(XX.shape) for m in ms]
    vote = (sum(Zs) >= 2).astype(int)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=vote, colorscale=[[0, "#FDE5CC"], [1, "#DCE6F2"]], showscale=False,
                             hoverinfo="skip"), 1, col)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        m = y_tr == cls
        fig.add_trace(go.Scatter(x=X_tr[m, 0], y=X_tr[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=c, size=6, line=dict(color="white", width=0.5))), 1, col)
    for Z, c, w in zip(Zs, (GREEN, RED, PURPLE), (9, 6, 3)):                  # copies: lines stack on each other
        fig.add_trace(go.Contour(x=xs, y=ys, z=Z, contours=dict(start=0.5, end=0.5, coloring="none"),
                                 showscale=False, line=dict(color=c, width=w), showlegend=False,
                                 hoverinfo="skip"), 1, col)
    fig.add_trace(go.Contour(x=xs, y=ys, z=vote, contours=dict(start=0.5, end=0.5, coloring="none"),
                             showscale=False, line=dict(color="black", width=3, dash="dash"), showlegend=False,
                             hoverinfo="skip"), 1, col)
fig.add_annotation(x=2.95, xanchor="right", y=-1.4, xref="x1", yref="y1", text="one boundary, drawn 3 times", showarrow=False,
                   bgcolor="white", font_size=18)
fig.add_annotation(x=2.95, xanchor="right", y=-1.4, xref="x2", yref="y2", text="3 boundaries, vote in black", showarrow=False,
                   bgcolor="white", font_size=18)
fig.update_xaxes(range=[xs[0], xs[-1]], title="x1")
fig.update_yaxes(range=[ys[0], ys[-1]], title="x2", col=1)
fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False, col=2)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(HERE / "same_vs_different.png", scale=2)
fig.write_image(HERE / "same_vs_different.pdf")
