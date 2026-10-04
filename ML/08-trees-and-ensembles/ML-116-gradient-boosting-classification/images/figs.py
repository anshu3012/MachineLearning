"""Gradient boosting classification on the two-Gaussians data (Plotly):
surfaces.png - predicted probability of class 1 after 0, 1, 2, 10, 30 and 100 trees (learning rate 0.5, 4 leaves);
view3d.png   - the data lifted to height 0 or 1, with the model's probability surface after 1 tree."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from gbc import boost, log_odds, sigmoid, two_gaussians  # noqa: E402

FONT = dict(family="Latin Modern Roman", size=19)
COLOURS = {0: "#F58518", 1: "#4C78A8"}
PROB = [[0, "#FBC99A"], [0.5, "#FFFFFF"], [1, "#AFC6E2"]]
LR = 0.5
X, y = two_gaussians()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
f0, stages = boost(X_train, y_train, 100, LR, 4)
xs = np.linspace(X[:, 0].min() - 0.3, X[:, 0].max() + 0.3, 200)
ys = np.linspace(X[:, 1].min() - 0.3, X[:, 1].max() + 0.3, 200)
XX, YY = np.meshgrid(xs, ys)
G = np.c_[XX.ravel(), YY.ravel()]


def acc(Xs, ys_, m):
    return ((sigmoid(log_odds(f0, stages, LR, Xs, m)) > 0.5) == ys_).mean()


counts = [0, 1, 2, 10, 30, 100]
titles = [f"{m} tree{'s' * (m != 1)}: train {acc(X_train, y_train, m):.2f}, test {acc(X_test, y_test, m):.2f}" for m in counts]
fig = make_subplots(2, 3, subplot_titles=titles, horizontal_spacing=0.03, vertical_spacing=0.08)
for i, m in enumerate(counts):
    r, c = i // 3 + 1, i % 3 + 1
    Z = sigmoid(log_odds(f0, stages, LR, G, m)).reshape(XX.shape)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=PROB, showscale=i == 0,
                             colorbar=dict(title="P(class 1)", len=0.5, y=0.5), hoverinfo="skip"), r, c)
    for cls in (0, 1):
        mk = y_train == cls
        fig.add_trace(go.Scatter(x=X_train[mk, 0], y=X_train[mk, 1], mode="markers", name=f"class {cls}",
                                 showlegend=i == 0, marker=dict(color=COLOURS[cls], size=4)), r, c)
    print(titles[i])
fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1500, height=1000, font=FONT, margin=dict(l=20, r=20, t=50, b=50),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.03, font_size=20, itemsizing="constant"))
fig.write_image(HERE / "surfaces.png", scale=2)
fig.write_image(HERE / "surfaces.pdf")

# 3D view: points at height y (0 or 1), probability surface after 3 trees
xs3, ys3 = np.linspace(xs[0], xs[-1], 80), np.linspace(ys[0], ys[-1], 80)
X3, Y3 = np.meshgrid(xs3, ys3)
Z3 = sigmoid(log_odds(f0, stages, LR, np.c_[X3.ravel(), Y3.ravel()], 1)).reshape(X3.shape)
fig = go.Figure()
fig.add_trace(go.Surface(x=xs3, y=ys3, z=Z3, colorscale=[[0, "#F58518"], [1, "#4C78A8"]], opacity=0.7,
                         showscale=False, cmin=0, cmax=1))
for cls in (0, 1):
    mk = y_train == cls
    fig.add_trace(go.Scatter3d(x=X_train[mk, 0], y=X_train[mk, 1], z=np.full(mk.sum(), cls), mode="markers",
                               name=f"class {cls} (height {cls})", marker=dict(color=COLOURS[cls], size=2.5)))
fig.update_layout(width=1100, height=800, font=FONT, margin=dict(l=0, r=0, t=0, b=0),
                  legend=dict(x=0.02, y=0.95, font_size=20, itemsizing="constant"),
                  scene=dict(xaxis_title="x1", yaxis_title="x2", zaxis_title="P(class 1)",
                             xaxis=dict(dtick=4, tickfont_size=15), yaxis=dict(dtick=4, tickfont_size=15),
                             zaxis=dict(range=[0, 1], dtick=0.5, tickfont_size=15),
                             camera=dict(eye=dict(x=1.6, y=-1.5, z=0.8))))
fig.write_image(HERE / "view3d.png", scale=2)
fig.write_image(HERE / "view3d.pdf")
