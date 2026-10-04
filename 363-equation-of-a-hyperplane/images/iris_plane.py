"""A hyperplane in 3D separating real data: iris setosa and versicolor by sepal length, petal length and petal width,
with the plane w.x + w0 = 0 found by a linear SVM (scikit-learn LinearSVC). Every flower lies on its own side."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.svm import LinearSVC

here = Path(__file__).parent
d = load_iris()
m = d.target < 2
X, y = d.data[m][:, [0, 2, 3]], d.target[m]
clf = LinearSVC(C=1.0, random_state=0, max_iter=10000).fit(X, y)
w, w0 = clf.coef_[0], clf.intercept_[0]
assert (clf.predict(X) == y).all()
g1, g2 = np.meshgrid(np.linspace(4, 7.2, 200), np.linspace(1, 5.2, 200))
z = -(w[0] * g1 + w[1] * g2 + w0) / w[2]                      # solve w.x + w0 = 0 for petal width
z = np.where((z >= 0) & (z <= 2.2), z, np.nan)
fig = go.Figure()
fig.add_surface(x=g1, y=g2, z=z, opacity=0.45, showscale=False, colorscale=[[0, "#9a9a9a"], [1, "#9a9a9a"]])
for k, c, n in ((0, "#4C78A8", "setosa"), (1, "#F58518", "versicolor")):
    fig.add_scatter3d(x=X[y == k, 0], y=X[y == k, 1], z=X[y == k, 2], mode="markers", marker=dict(size=4, color=c), name=n)
fig.update_layout(width=1000, height=760, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text=f"A plane in 3D: {w[0]:.2f}x₁ + {w[1]:.2f}x₂ + {w[2]:.2f}x₃ − {-w0:.2f} = 0", x=0.5),
                  scene=dict(xaxis=dict(title="sepal length x₁", tickfont=dict(size=12)),
                             yaxis=dict(title="petal length x₂", tickfont=dict(size=12)),
                             zaxis=dict(title="petal width x₃", range=[0, 2.2], tickfont=dict(size=12)),
                             aspectmode="cube", camera=dict(eye=dict(x=1.9, y=-1.6, z=0.8))),
                  legend=dict(x=0.02, y=0.9), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "iris_plane.png", scale=2)
