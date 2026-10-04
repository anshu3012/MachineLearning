"""Lasso on the diabetes data: coefficient bars at four alphas, and coefficient paths on a log alpha axis (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.model_selection import train_test_split
warnings.simplefilter("ignore")

here = Path(__file__).parent
d = load_diabetes()
names = d.feature_names
Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
fit = lambda a: (LinearRegression() if a == 0 else Lasso(alpha=a, max_iter=100000)).fit(Xtr, ytr)

fig = make_subplots(rows=2, cols=2, vertical_spacing=0.18, horizontal_spacing=0.1, subplot_titles=[" "] * 4)
for k, a in enumerate([0, 0.1, 1, 10]):
    r = fit(a); c = r.coef_
    fig.add_trace(go.Bar(x=names, y=c, marker_color=["#E45756" if v < 0 else "#4C78A8" for v in c]), k // 2 + 1, k % 2 + 1)
    zeros = [n for n, v in zip(names, c) if v == 0]
    fig.layout.annotations[k].text = (f"alpha = {a}: {len(zeros)} of 10 coefficients are 0, test R² {r.score(Xte, yte):.2f}").replace("-", "−")
    print(a, zeros)
fig.update_yaxes(range=[-950, 950])
fig.update_layout(template="simple_white", width=1100, height=700, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=60, r=30, t=50, b=40))
fig.write_image(here / "bars.png", scale=2)
fig.write_image(here / "bars.pdf")

grid = np.logspace(-3, 1, 200)
C = np.array([fit(a).coef_ for a in grid])
fig = go.Figure()
fig.add_trace(go.Scatter(x=[grid[0], grid[-1]], y=[0, 0], mode="lines", line=dict(color="black", width=3), showlegend=False))
strong = {"s1": "#E45756", "s5": "#4C78A8", "bmi": "#54A24B", "bp": "#F58518", "s2": "#B279A2"}
for j, n in enumerate(names):
    col = strong.get(n, "#BBBBBB")
    fig.add_trace(go.Scatter(x=grid, y=C[:, j], mode="lines", line=dict(color=col, width=4 if n in strong else 2), showlegend=False))
    last = np.nonzero(C[:, j])[0]
    gone = grid[last[-1] + 1] if len(last) and last[-1] + 1 < len(grid) else None
    fig.add_annotation(x=np.log10(grid[0]), y=C[0, j], text=n, showarrow=False, xanchor="right", xshift=-6, yshift={"s2": -9, "bmi": 7, "s3": 6, "s4": -5}.get(n, 0),
                       font=dict(color=col if n in strong else "#888888", size=14))
    print(n, "zero from alpha", None if gone is None else round(gone, 3))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=90, r=30, t=60, b=60),
                  title=dict(text="Lasso: coefficients hit 0 one by one; bmi and s5 survive longest", x=0.5),
                  xaxis=dict(title="alpha (log scale)", type="log", exponentformat="power", dtick=1),
                  yaxis=dict(title="coefficient"))
fig.write_image(here / "paths.png", scale=2)
fig.write_image(here / "paths.pdf")
