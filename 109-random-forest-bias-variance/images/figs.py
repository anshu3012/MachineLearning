"""Random forest against one fully grown tree (Plotly):
circles.png  - decision surfaces on the concentric-circles data (500 points, 400 for training);
curves.png   - one tree, bagged trees and a random forest on the two-bumps regression data
               (150 training points, 1,000 test points)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.ensemble import BaggingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
COLOURS = {0: "#F58518", 1: "#4C78A8"}             # class 0 orange, class 1 blue (as in the KNN and bagging Notes)
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]

# ---- classification: concentric circles ----
X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
rf = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1).fit(X_train, y_train)
xs = np.linspace(X[:, 0].min() - 0.2, X[:, 0].max() + 0.2, 300)
ys = np.linspace(X[:, 1].min() - 0.2, X[:, 1].max() + 0.2, 300)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
titles = [f"(a) one fully grown tree: train {tree.score(X_train, y_train):.2f}, test {tree.score(X_test, y_test):.2f}",
          f"(b) random forest, 500 trees: train {rf.score(X_train, y_train):.2f}, test {rf.score(X_test, y_test):.2f}"]
print(titles)
fig = make_subplots(1, 2, subplot_titles=titles, horizontal_spacing=0.04)
for i, model in enumerate([tree, rf], start=1):
    Z = model.predict(grid).reshape(XX.shape)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False), 1, i)
    for cls in (0, 1):
        m = y_train == cls
        fig.add_trace(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                                 showlegend=(i == 1), marker=dict(color=COLOURS[cls], size=6,
                                                                  line=dict(color="white", width=0.5))), 1, i)
fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1300, height=660, font=FONT, margin=dict(l=20, r=20, t=60, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.04, font_size=20))
fig.write_image(HERE / "circles.png", scale=2)
fig.write_image(HERE / "circles.pdf")

# ---- regression: two Gaussian bumps plus noise (the data of the bagging regressor Note) ----
rng = np.random.RandomState(0)


def generate(n, noise=0.1):
    x = np.sort(rng.rand(n) * 10 - 5)
    return x[:, None], np.exp(-x ** 2) + 1.5 * np.exp(-(x - 2) ** 2) + rng.normal(0.0, noise, n)


Xr_train, yr_train = generate(150)
Xr_test, yr_test = generate(1000)
X_line = np.linspace(-5, 5, 800)[:, None]
truth = np.exp(-X_line.ravel() ** 2) + 1.5 * np.exp(-(X_line.ravel() - 2) ** 2)
dtr = DecisionTreeRegressor(random_state=0).fit(Xr_train, yr_train)
bgr = BaggingRegressor(DecisionTreeRegressor(), n_estimators=1000, random_state=0, n_jobs=-1).fit(Xr_train, yr_train)
rfr = RandomForestRegressor(n_estimators=1000, random_state=0, n_jobs=-1).fit(Xr_train, yr_train)
panels = []
for name, model, colour in [("(a) one fully grown tree", dtr, "#E45756"), ("(b) bagged trees, 1,000", bgr, "#54A24B"),
                            ("(c) random forest, 1,000 trees", rfr, "#4C78A8")]:
    m = mean_squared_error(yr_test, model.predict(Xr_test))
    panels.append((f"{name}<br>test MSE {m:.4f}", model, colour))
print([p[0] for p in panels])
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.03, subplot_titles=[p[0] for p in panels])
for i, (_, model, colour) in enumerate(panels, start=1):
    fig.add_trace(go.Scatter(x=Xr_train.ravel(), y=yr_train, mode="markers", name="training points", showlegend=(i == 1),
                             marker=dict(color="#FFD24C", size=7, line=dict(color="black", width=1))), 1, i)
    fig.add_trace(go.Scatter(x=X_line.ravel(), y=truth, mode="lines", name="true pattern", showlegend=(i == 1),
                             line=dict(color="#6B6B6B", width=2, dash="dash")), 1, i)
    fig.add_trace(go.Scatter(x=X_line.ravel(), y=model.predict(X_line), mode="lines", name="model",
                             showlegend=False, line=dict(color=colour, width=3)), 1, i)
fig.update_xaxes(title="x")
fig.update_yaxes(title="y", col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1500, height=560, font=FONT, margin=dict(l=60, r=20, t=90, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font_size=20))
fig.write_image(HERE / "curves.png", scale=2)
fig.write_image(HERE / "curves.pdf")
