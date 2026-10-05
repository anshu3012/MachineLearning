"""The 2D density of petal length and sepal length (iris, 150 flowers) as a 3-D surface, then tilted to the top view,
which is the contour map of joint_kde.png. Run: python joint_kde_surface.py -> joint_kde_surface.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from sklearn.datasets import load_iris
from tilt import tilt_gif

here = Path(__file__).parent
d = load_iris().data
x, y = d[:, 2], d[:, 0]
kde = stats.gaussian_kde(np.vstack([x, y]))
X, Y = np.meshgrid(np.linspace(0, 8, 90), np.linspace(3.5, 8.5, 90))
Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
print("peak", Z.max(), "f(1.5, 5.0) =", kde([[1.5], [5.0]])[0])
scale = [[0, "white"], [0.1, "#DEEBF7"], [0.5, "#6BAED6"], [1, "#08306B"]]


def flowers(a):
    return [go.Scatter3d(x=x, y=y, z=kde(np.vstack([x, y])) + 0.004, mode="markers", marker=dict(size=2.5, color="#F58518"))]


tilt_gif(here / "joint_kde_surface", X, Y, Z, scale, (0.02, 0.22, 0.02), (0, 0.22),
         labels=("petal length (cm)", "sepal length (cm)", "density"), extra=flowers, aspect=0.6, opacity=0.9,
         titles=("Density of petal length and sepal length: two hills",
                 "Turn to the top view …",
                 "Seen from above: the contour map of Figure 6"))
