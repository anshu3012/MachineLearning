"""Logistic regression on polynomial features of moon-shaped data: decision regions for six degrees (Plotly).
Weak regularisation (C = 10,000) so the effect of the degree shows; 10-fold cross-validated accuracy in each title."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
X, y = make_moons(n_samples=200, noise=0.25, random_state=0)
degrees = [1, 2, 3, 4, 10, 25]
xs, ys = np.linspace(-2, 3, 220), np.linspace(-1.6, 2.0, 180)
XX, YY = np.meshgrid(xs, ys)
fig = make_subplots(rows=2, cols=3, horizontal_spacing=0.05, vertical_spacing=0.12, subplot_titles=[" "] * 6)
for k, d in enumerate(degrees):
    model = make_pipeline(PolynomialFeatures(degree=d, include_bias=False), StandardScaler(),
                          LogisticRegression(C=1e4, max_iter=100000))
    cv = cross_val_score(model, X, y, cv=10).mean()
    model.fit(X, y)
    Z = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    r, c = k // 3 + 1, k % 3 + 1
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, colorscale=[[0, "#DCE6F2"], [1, "#FDE5CC"]], showscale=False, hoverinfo="skip"), r, c)
    for cls, col in ((0, "#4C78A8"), (1, "#F58518")):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", marker=dict(color=col, size=5),
                                 showlegend=False), r, c)
    n_cols = model[0].n_output_features_
    fig.layout.annotations[k].text = f"degree {d} ({n_cols} columns): CV accuracy {cv:.3f}"
    print(d, n_cols, round(cv, 3), "train", model.score(X, y))
fig.update_xaxes(range=[-2, 3], showticklabels=False)
fig.update_yaxes(range=[-1.6, 2.0], showticklabels=False)
fig.update_layout(template="simple_white", width=1150, height=700, font=dict(family="Latin Modern Roman", size=15),
                  margin=dict(l=20, r=20, t=50, b=20))
fig.write_image(here / "degrees.png", scale=2); fig.write_image(here / "degrees.pdf")
