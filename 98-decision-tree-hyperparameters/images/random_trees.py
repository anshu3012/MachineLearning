"""Randomness on one tree and on many (Plotly), moons data (500 points, noise 0.3, random_state 42, the Notebook's
split). Left three panels: fully grown trees with max_features=1 and three different random_state values: the
surfaces differ. Right: the average vote of 50 such trees is smoother. Test accuracy in each title."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
X, y = make_moons(n_samples=500, noise=0.3, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=42)
assert len(Xtr) == 375
trees = [DecisionTreeClassifier(max_features=1, random_state=s).fit(Xtr, ytr) for s in range(50)]
g1, g2 = np.linspace(-2, 3, 250), np.linspace(-1.6, 2.1, 200)
G1, G2 = np.meshgrid(g1, g2)
grid = np.c_[G1.ravel(), G2.ravel()]
vote_grid = np.mean([t.predict(grid) for t in trees], 0)
vote_te = np.mean([t.predict(Xte) for t in trees], 0) >= 0.5
single = [t.score(Xte, yte) for t in trees[:3]]
avg_acc = (vote_te == yte).mean()
mean_single = np.mean([t.score(Xte, yte) for t in trees])
assert avg_acc > mean_single
titles = [f"tree {s + 1}: test {a:.3f}" for s, a in enumerate(single)] + [f"average of 50 trees: test {avg_acc:.3f}"]
fig = make_subplots(1, 4, horizontal_spacing=0.03, subplot_titles=titles)
fig.update_annotations(font_size=19)
for col in range(4):
    z = trees[col].predict(grid).reshape(G1.shape) if col < 3 else vote_grid.reshape(G1.shape)
    fig.add_trace(go.Heatmap(x=g1, y=g2, z=z, colorscale=[[0, ORANGE], [1, BLUE]], zmin=0, zmax=1, showscale=False, opacity=0.35), 1, col + 1)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        k = ytr == cls
        fig.add_trace(go.Scatter(x=Xtr[k, 0], y=Xtr[k, 1], mode="markers", marker=dict(size=4, color=c, line=dict(color="white", width=0.5))), 1, col + 1)
    fig.update_xaxes(showticklabels=False, row=1, col=col + 1)
    fig.update_yaxes(showticklabels=False, row=1, col=col + 1)
fig.update_layout(template="simple_white", width=1500, height=430, font=FONT, showlegend=False, margin=dict(l=20, r=20, t=60, b=20))
fig.write_image(here / "random_trees.png", scale=2)
assert round(mean_single, 3) == 0.856 and round(avg_acc, 3) == 0.888
