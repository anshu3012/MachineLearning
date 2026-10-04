"""Lasso with one input: fitted lines for several alphas, and the slope against alpha hitting exactly 0 (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso, LinearRegression
warnings.simplefilter("ignore")

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Fitted lines", "Slope against alpha"))
fig.add_trace(go.Scatter(x=X.ravel(), y=y, mode="markers", marker=dict(color="#BBBBBB", size=7), showlegend=False), 1, 1)
xs = np.array([X.min(), X.max()])
cols = {0: "#E45756", 5: "#F58518", 10: "#54A24B", 20: "#4C78A8", 30: "#000000"}
for a, c in cols.items():
    m = (LinearRegression() if a == 0 else Lasso(alpha=a)).fit(X, y)
    fig.add_trace(go.Scatter(x=xs, y=m.coef_[0] * xs + m.intercept_, mode="lines", line=dict(color=c, width=3),
                             name=f"alpha {a}: slope {m.coef_[0]:.1f}"), 1, 1)
grid = np.linspace(0, 40, 401)
slopes = [(LinearRegression() if a == 0 else Lasso(alpha=a)).fit(X, y).coef_[0] for a in grid]
fig.add_trace(go.Scatter(x=grid, y=slopes, mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False), 1, 2)
xc, yc = X.ravel() - X.mean(), y - y.mean()
cut = (xc * yc).mean()          # slope reaches 0 when alpha equals this (sklearn scales the error by 1/2n)
print("first zero at", cut)
fig.add_trace(go.Scatter(x=[cut], y=[0], mode="markers", marker=dict(size=12, color="#E45756"), showlegend=False), 1, 2)
fig.add_annotation(x=cut + 1, y=3, text=f"slope = 0 from alpha = {cut:.1f}", showarrow=False, xanchor="left",
                   font=dict(color="#E45756"), row=1, col=2)
fig.update_xaxes(title="x", row=1, col=1)
fig.update_yaxes(title="y", row=1, col=1)
fig.update_xaxes(title="alpha", row=1, col=2)
fig.update_yaxes(title="slope", range=[-1, 30], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)", font=dict(size=13)),
                  margin=dict(l=70, r=30, t=60, b=60))
fig.write_image(here / "one_input.png", scale=2)
fig.write_image(here / "one_input.pdf")
