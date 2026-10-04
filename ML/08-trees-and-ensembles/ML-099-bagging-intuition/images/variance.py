"""Why bagging works: one fully grown tree per training set swings a lot (high variance); a bagged ensemble of
100 trees per training set barely moves (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
truth = lambda x: np.sin(x)
x_line = np.linspace(0, 6, 400)[:, None]


def training_set(n=60):
    x = rng.uniform(0, 6, n)
    return x[:, None], truth(x) + rng.normal(0, 0.4, n)


sets = [training_set() for _ in range(20)]
tree_preds = np.array([DecisionTreeRegressor(random_state=0).fit(X, y).predict(x_line) for X, y in sets])
bag_preds = np.array([BaggingRegressor(DecisionTreeRegressor(), n_estimators=100, random_state=0).fit(X, y).predict(x_line)
                      for X, y in sets])
for name, P in (("single tree", tree_preds), ("bagging", bag_preds)):
    var = P.var(axis=0).mean()
    bias2 = ((P.mean(axis=0) - truth(x_line.ravel())) ** 2).mean()
    print(f"{name}: variance {var:.3f}, bias² {bias2:.3f}")
stats = {n: (P.var(axis=0).mean(), ((P.mean(axis=0) - truth(x_line.ravel())) ** 2).mean())
         for n, P in (("tree", tree_preds), ("bag", bag_preds))}

fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.04, subplot_titles=(
    f"(a) one fully grown tree per training set<br>variance {stats['tree'][0]:.3f}, bias² {stats['tree'][1]:.3f}",
    f"(b) bagging, 100 trees per training set<br>variance {stats['bag'][0]:.3f}, bias² {stats['bag'][1]:.3f}"))
for col, P in ((1, tree_preds), (2, bag_preds)):
    for p in P:
        fig.add_trace(go.Scatter(x=x_line.ravel(), y=p, mode="lines", line=dict(color="#F58518", width=1),
                                 opacity=0.45, showlegend=False), 1, col)
    fig.add_trace(go.Scatter(x=x_line.ravel(), y=P.mean(axis=0), mode="lines", line=dict(color="#4C78A8", width=4),
                             name="average of the 20 models", showlegend=(col == 1)), 1, col)
    fig.add_trace(go.Scatter(x=x_line.ravel(), y=truth(x_line.ravel()), mode="lines",
                             line=dict(color="black", width=3, dash="dash"), name="true curve", showlegend=(col == 1)), 1, col)
fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line=dict(color="#F58518", width=2),
                         name="one model per training set (20 sets)"))
fig.update_xaxes(title="x")
fig.update_yaxes(title="y", range=[-2.2, 2.2], col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1300, height=620, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=70, r=20, t=90, b=120))
fig.write_image(HERE / "variance.png", scale=2)
fig.write_image(HERE / "variance.pdf")
