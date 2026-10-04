"""Why a straight line fails on the curved data (Plotly): the best straight line on the 160 training points scores
test R2 0.38. Its residuals have a pattern: the points sit above the line at both ends and below it in the middle."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from data61 import X_test, X_train, y_test, y_train
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
lr = LinearRegression().fit(X_train, y_train)
assert round(lr.score(X_test, y_test), 2) == 0.38
x, y = X_train.ravel(), y_train
r = y - lr.predict(X_train)
mid = np.abs(x) < 1
assert r[~mid].mean() > 0 > r[mid].mean()
fig = go.Figure()
for m, c, name in ((r > 0, BLUE, "point above the line"), (r <= 0, RED, "point below the line")):
    sx, sy = [], []
    for xi, yi, ri in zip(x[m], y[m], r[m]):
        sx += [xi, xi, None]; sy += [yi, yi - ri, None]
    fig.add_scatter(x=sx, y=sy, mode="lines", line=dict(color=c, width=1.5), name=name)
fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=6, color=GREY), showlegend=False)
xs = np.array([-3, 3])
fig.add_scatter(x=xs, y=lr.predict(xs.reshape(-1, 1)), mode="lines", line=dict(color="black", width=4),
                name="best straight line (test R² 0.38)")
fig.update_layout(template="simple_white", width=950, height=560, font=FONT,
                  xaxis=dict(title="x", range=[-3.1, 3.1]), yaxis=dict(title="y", range=[-2.5, 12]),
                  legend=dict(x=0.3, y=0.99), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "line_misses.png", scale=2)
