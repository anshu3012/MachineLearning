"""Section 6: mean test R² of linear regression, RidgeCV, LassoCV and ElasticNetCV on the diabetes data, 40 random
splits, with 80 training observations and with the full 353 (Plotly dot plot). Same experiment as the notebook:
every penalty tuned by 5-fold CV on the training part only. Takes a few minutes (40 x 2 x ElasticNetCV)."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import ElasticNetCV, LassoCV, LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split

warnings.simplefilter("ignore")
here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
alphas = np.logspace(-4, 1, 40)
NAMES = ["Linear regression", "Ridge", "Lasso", "Elastic Net"]


def compare(n_train, n_splits=40):
    scores = {k: [] for k in NAMES}
    for s in range(n_splits):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, train_size=n_train, random_state=s)
        models = [LinearRegression(), RidgeCV(alphas=alphas), LassoCV(alphas=alphas, cv=5),
                  ElasticNetCV(l1_ratio=[0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1], alphas=alphas, cv=5)]
        for k, m in zip(NAMES, models):
            scores[k].append(m.fit(X_tr, y_tr).score(X_te, y_te))
    return [float(np.mean(scores[k])) for k in NAMES]


small, full = compare(80), compare(353)
print("80:", np.round(small, 3), "353:", np.round(full, 3))
assert list(np.round(small, 3)) == [0.412, 0.440, 0.431, 0.437]      # the Note's table
assert list(np.round(full, 3)) == [0.455, 0.455, 0.456, 0.457]       # the Note's Extra
fig = go.Figure()
for vals, name, color, sym in [(small, "80 training observations", "#E45756", "circle"),
                               (full, "353 training observations", "#4C78A8", "diamond")]:
    fig.add_trace(go.Scatter(x=vals, y=NAMES, mode="markers+text", name=name, text=[f"{v:.3f}" for v in vals],
                             textposition="top center", textfont=dict(color=color, size=20),
                             marker=dict(size=20, color=color, symbol=sym)))
for k, a, b in zip(NAMES, small, full):
    fig.add_shape(type="line", x0=a, x1=b, y0=k, y1=k, line=dict(color="#CCCCCC", width=3), layer="below")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="mean test R² over 40 splits", range=[0.40, 0.47]),
                  yaxis=dict(range=[3.4, -0.75]), margin=dict(l=190, r=30, t=60, b=150),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.3))
fig.write_image(here / "small_data.png", scale=2)
fig.write_image(here / "small_data.pdf")
