"""Bagging helps unstable models most. The setup of Figure 3 (variance.py): 20 training sets of 60 noisy points from
a sine curve, seed 0. For a fully grown decision tree (unstable) and a 5-nearest-neighbour regressor (stable), the
variance of one model per set and of a bagged ensemble of 100 per set. Plotly bar chart."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import BaggingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
rng = np.random.default_rng(0)                          # same draws as variance.py
x_line = np.linspace(0, 6, 400)[:, None]


def training_set(n=60):
    x = rng.uniform(0, 6, n)
    return x[:, None], np.sin(x) + rng.normal(0, 0.4, n)


sets = [training_set() for _ in range(20)]
var = lambda P: P.var(axis=0).mean()
V = {}
for name, m in (("fully grown tree", DecisionTreeRegressor(random_state=0)), ("5-nearest neighbours", KNeighborsRegressor(5))):
    single = np.array([m.fit(X, y).predict(x_line) for X, y in sets])
    bagged = np.array([BaggingRegressor(m, n_estimators=100, random_state=0).fit(X, y).predict(x_line) for X, y in sets])
    V[name] = (var(single), var(bagged))
assert [round(v, 3) for v in V["fully grown tree"]] == [0.160, 0.076]
assert [round(v, 3) for v in V["5-nearest neighbours"]] == [0.034, 0.025]

fig = go.Figure()
names = list(V)
fig.add_bar(x=names, y=[V[n][0] for n in names], name="one model per training set", marker_color="#F58518",
            text=[f"{V[n][0]:.3f}" for n in names], textposition="outside")
fig.add_bar(x=names, y=[V[n][1] for n in names], name="bagging, 100 models", marker_color="#4C78A8",
            text=[f"{V[n][1]:.3f}" for n in names], textposition="outside")
for i, n in enumerate(names):
    cut = 100 * (1 - V[n][1] / V[n][0])
    fig.add_annotation(x=i, y=V[n][0] + 0.03, text=f"<b>−{cut:.0f}%</b>", showarrow=False, font=dict(size=24))
fig.update_layout(template="simple_white", width=1000, height=620, barmode="group",
                  font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="Variance over 20 training sets: before and after bagging", x=0.5),
                  yaxis=dict(title="variance", range=[0, 0.21]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12), margin=dict(l=80, r=30, t=80, b=110))
fig.write_image(HERE / "unstable.png", scale=2)
print({n: [round(v, 3) for v in V[n]] for n in V})
