"""What the from-scratch class outputs (Plotly): on the 40 test students, MyLR's line and scikit-learn's line lie on
top of each other, and the first three test students get the same predictions 3.8911, 3.0932 and 2.3846."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import X_test, X_train, lr, y_test, y_train
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent


class MyLR:                                          # the class of Section 6
    def fit(self, X, y):
        x_bar, y_bar = X.mean(), y.mean()
        self.m = ((X - x_bar) * (y - y_bar)).sum() / ((X - x_bar) ** 2).sum()
        self.b = y_bar - self.m * x_bar
        return self

    def predict(self, X):
        return self.m * X + self.b


xt, yt = X_test["cgpa"].to_numpy(), y_test.to_numpy()
mine = MyLR().fit(X_train["cgpa"].to_numpy(), y_train.to_numpy())
p3, s3 = mine.predict(xt[:3]), lr.predict(X_test[:3])
assert np.allclose(p3, s3) and [round(v, 4) for v in p3] == [3.8911, 3.0932, 2.3846]
xs = np.array([4, 10])
fig = go.Figure([
    go.Scatter(x=xt, y=yt, mode="markers", name="test students", marker=dict(size=9, color=GREY, opacity=0.6)),
    go.Scatter(x=xs, y=lr.predict(pd.DataFrame({"cgpa": xs})),
               mode="lines", name="scikit-learn LinearRegression", line=dict(color=ORANGE, width=12)),
    go.Scatter(x=xs, y=mine.predict(xs), mode="lines", name="our MyLR", line=dict(color=BLUE, width=4, dash="dash")),
    go.Scatter(x=xt[:3], y=p3, mode="markers+text", name="first three predictions",
               text=[f"{v:.4f}" for v in p3], textposition="bottom right", textfont=dict(size=22),
               marker=dict(size=16, color=BLUE, symbol="diamond", line=dict(color="white", width=2)))])
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  xaxis=dict(title="CGPA", range=[4, 10]), yaxis=dict(title="package", range=[0.8, 5]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "my_vs_sklearn.png", scale=2)
