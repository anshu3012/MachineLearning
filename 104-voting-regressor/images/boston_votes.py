"""VotingRegressor on the Boston housing data (Plotly), three bar charts, same models and folds as the notebook:
boston_members.png: the three base models, their vote and the best weights (2, 3, 1);
boston_trees.png: five trees of different depth and their vote;
boston_folds.png: shuffled folds against folds in order (the notebook's older unscaled SVR for the in-order run)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
boston = pd.read_csv(HERE.parent / "data" / "boston.csv")
X, y = boston.drop(columns="MEDV"), boston["MEDV"]
cv = RepeatedKFold(n_splits=10, n_repeats=5, random_state=0)
r2 = lambda m, c=cv: cross_val_score(m, X, y, scoring="r2", cv=c, n_jobs=-1).mean()
est = [("lr", LinearRegression()), ("dt", DecisionTreeRegressor(random_state=0)),
       ("svr", make_pipeline(StandardScaler(), SVR()))]
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, GREEN, ORANGE, GREY = "#4C78A8", "#54A24B", "#F58518", "#6B6B6B"


def bars(names, vals, cols, path, yrange, digits=2):
    fig = go.Figure(go.Bar(x=names, y=vals, marker_color=cols, text=[f"{v:.{digits}f}" for v in vals],
                           textposition="outside"))
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, bargap=0.3,
                      yaxis=dict(title="mean R² (10-fold, 5 shuffles)", range=yrange), margin=dict(l=100, r=20, t=30, b=100))
    fig.write_image(HERE / f"{path}.png", scale=2); fig.write_image(HERE / f"{path}.pdf")


# 1. members, vote, weighted vote
m = [r2(e) for _, e in est] + [r2(VotingRegressor(est)), r2(VotingRegressor(est, weights=[2, 3, 1]))]
print("members", np.round(m, 3))
assert np.allclose(np.round(m[:4], 2), [0.71, 0.73, 0.67, 0.81]) and round(m[4], 3) == 0.820       # sections 4.1-4.3
bars(["linear<br>regression", "decision<br>tree", "SVR", "vote", "vote, weights<br>2, 3, 1"], m,
     [BLUE] * 3 + [GREEN, GREEN], "boston_members", [0, 0.92])

# 2. five trees and their vote
trees = [(f"dt{d}", DecisionTreeRegressor(max_depth=d, random_state=0)) for d in [1, 3, 5, 7, None]]
t = [r2(e) for _, e in trees] + [r2(VotingRegressor(trees))]
print("trees", np.round(t, 3))
assert np.allclose(np.round(t, 2), [0.35, 0.67, 0.74, 0.74, 0.73, 0.76])                         # section 4.4
bars(["depth 1", "depth 3", "depth 5", "depth 7", "no limit", "vote of<br>all five"], t, [BLUE] * 5 + [GREEN],
     "boston_trees", [0, 0.88])

# 3. shuffled against in order
plain = [("lr", LinearRegression()), ("dt", DecisionTreeRegressor(random_state=0)), ("svr", SVR())]
order = [r2(e, 10) for _, e in plain] + [r2(VotingRegressor(plain), 10)]
print("in order", np.round(order, 3))
assert np.allclose(np.round(order, 2), [0.20, -0.07, -0.41, 0.43])                               # section 4.5
names = ["linear regression", "decision tree", "SVR", "vote"]
fig = go.Figure([go.Bar(x=names, y=m[:4], name="shuffled folds (scaled SVR)", marker_color=BLUE,
                        text=[f"{v:.2f}" for v in m[:4]], textposition="outside"),
                 go.Bar(x=names, y=order, name="folds in order (unscaled SVR)", marker_color=ORANGE,
                        text=[f"{v:.2f}" for v in order], textposition="outside")])
fig.add_hline(y=0, line=dict(color="black", width=1.5))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, bargap=0.25,
                  yaxis=dict(title="mean R²", range=[-0.55, 1.0]), legend=dict(x=0.01, y=1.0, orientation="h"),
                  margin=dict(l=100, r=20, t=30, b=60))
fig.write_image(HERE / "boston_folds.png", scale=2); fig.write_image(HERE / "boston_folds.pdf")
