"""Same recipe, less noise: predicted vs actual target on the 20 test observations for noise 50, 25 and 0 (Plotly).
Points on the diagonal are perfect predictions."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
NOISE = (50, 25, 0)
res = []
for noise in NOISE:
    X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=noise, random_state=7)
    a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=3)
    p = LinearRegression().fit(a, c).predict(b)
    res.append((d, p, r2_score(d, p)))
assert [round(r, 2) for *_, r in res] == [0.61, 0.85, 1.0]           # the Note's numbers
fig = make_subplots(1, 3, horizontal_spacing=0.06, shared_yaxes=True,
                    subplot_titles=[f"noise = {n}: R² = {r:.2f}" for n, (*_, r) in zip(NOISE, res)])
for col, (d, p, _) in enumerate(res, 1):
    fig.add_trace(go.Scatter(x=[-250, 250], y=[-250, 250], mode="lines", line=dict(color="#6B6B6B", dash="dash")), 1, col)
    fig.add_trace(go.Scatter(x=d, y=p, mode="markers", marker=dict(size=10, color="#4C78A8")), 1, col)
    fig.update_xaxes(title="actual target", range=[-250, 250], dtick=200, row=1, col=col)
fig.update_yaxes(title="predicted target", range=[-250, 250], dtick=200, row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=80, r=20, t=60, b=60))
fig.update_annotations(font_size=20)
fig.write_image(here / "noise_fit.png", scale=2)
fig.write_image(here / "noise_fit.pdf")
