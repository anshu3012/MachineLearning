"""Serverless twin of ../app.py: precompute the KNN decision surface for a grid of k values and write ONE Plotly
HTML whose slider switches between the precomputed frames in the browser (no Dash, no callbacks).

Run: python knn_playground.py -> knn_playground.html
"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, NAMES, REGION, X, X_test, X_train, y_test, y_train  # noqa: E402

# ponytail: the Dash slider allows every k in 1..455 (455 frames); we keep every k up to 100, then every 5th.
KS = list(range(1, 101)) + list(range(105, len(X_train) + 1, 5))
N = 150                                            # grid cells per axis (app.py uses 300); size grows with N**2
xs = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, N)
ys = np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, N)
XX, YY = np.meshgrid(xs, ys)
GRID = np.c_[XX.ravel(), YY.ravel()]


def surface(k):
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_train, y_train)
    return model.predict(GRID).reshape(XX.shape).astype(np.int8), model.score(X_test, y_test)


def title(k, acc):
    return f"k = {k}   |   test accuracy {acc:.3f}"


frames, steps = [], []
for k in KS:
    Z, acc = surface(k)
    frames.append(go.Frame(name=str(k), data=[go.Heatmap(z=Z)], traces=[0], layout=dict(title=title(k, acc))))
    steps.append(dict(label=str(k), method="animate",
                      args=[[str(k)], dict(mode="immediate", frame=dict(duration=0, redraw=True),
                                           transition=dict(duration=0))]))

Z0, acc0 = surface(5)                                  # the app starts at k = 5
fig = go.Figure(
    data=[go.Heatmap(x=xs, y=ys, z=Z0, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    + [go.Scatter(x=X_train[y_train == c, 0], y=X_train[y_train == c, 1], mode="markers",
                  name=f"{NAMES[c]} (training)",
                  marker=dict(color=COLOURS[c], size=6, line=dict(color="white", width=0.5))) for c in (0, 1)],
    frames=frames)
fig.update_layout(template="simple_white", height=600, margin=dict(l=60, r=20, t=60, b=90),
                  title=title(5, acc0),
                  xaxis=dict(title="mean radius", range=[xs[0], xs[-1]]),
                  yaxis=dict(title="mean texture", range=[ys[0], ys[-1]]),
                  sliders=[dict(active=KS.index(5), currentvalue=dict(prefix="k = "), pad=dict(t=40),
                                steps=steps)])
out = HERE / "knn_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(KS)} frames, {N}x{N} grid")
