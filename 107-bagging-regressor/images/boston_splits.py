"""Section 4: test R² of five regressors on the Boston housing data over the same 100 random 404/102 splits.
Each dot is one split; the box shows the middle half; the number is the mean. (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
boston = pd.read_csv(HERE.parent / "data" / "boston.csv")
X, y = boston.drop(columns="MEDV"), boston["MEDV"]
splits = [train_test_split(X, y, test_size=0.2, random_state=s) for s in range(100)]     # as in the Notebook
makers = {"linear regression": LinearRegression, "decision tree": lambda: DecisionTreeRegressor(random_state=1),
          "KNN": KNeighborsRegressor, "bagging, default": lambda: BaggingRegressor(random_state=1),
          "bagging, tuned": lambda: BaggingRegressor(n_estimators=50, random_state=1)}
scores = {n: np.array([m().fit(a, c).score(b, d) for a, b, c, d in splits]) for n, m in makers.items()}
means = [round(s.mean(), 3) for s in scores.values()]
assert means == [0.708, 0.716, 0.504, 0.841, 0.857], means
assert int((scores["bagging, tuned"] > scores["bagging, default"]).sum()) == 79
t = scores["bagging, tuned"]
assert round(t.min(), 2) == 0.63 and round(t.max(), 2) == 0.94
print(means, {n: (round(s.min(), 2), round(s.max(), 2)) for n, s in scores.items()})

COL = ["#6B6B6B", "#E45756", "#B279A2", "#4C78A8", "#54A24B"]
fig = go.Figure()
for (n, s), c, m in zip(scores.items(), COL, means):
    fig.add_trace(go.Box(y=s, name=n, boxpoints="all", jitter=0.5, pointpos=0, marker=dict(color=c, size=5, opacity=0.6),
                         line=dict(color=c, width=2), fillcolor="rgba(0,0,0,0)", showlegend=False))
    fig.add_annotation(x=n, y=1.04, text=f"mean {m:.2f}", showarrow=False, font=dict(size=21, color=c))
fig.update_yaxes(title="test R² (one dot = one split)", range=[-0.05, 1.09])
fig.update_layout(template="simple_white", width=1200, height=620, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=90, r=20, t=20, b=60))
fig.write_image(HERE / "boston_splits.png", scale=2)
fig.write_image(HERE / "boston_splits.pdf")
