"""Ridge lines on the Note's 100-observation example (make_regression, noise 20, random_state 13) (Plotly): the OLS
line (lambda = 0, slope 27.83) and the Ridge lines for lambda = 10 (24.95) and 100 (12.93). Every line passes through
the point of means, because b = y-bar - m x-bar; only the slope changes."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
num, den = ((x - x.mean()) * (y - y.mean())).sum(), ((x - x.mean()) ** 2).sum()
fit = lambda l: (num / (den + l), y.mean() - num / (den + l) * x.mean())
assert [round(fit(l)[0], 2) for l in (0, 10, 100)] == [27.83, 24.95, 12.93]
xs = np.array([x.min() - 0.2, x.max() + 0.2])
fig = go.Figure(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=7, color=GREY, opacity=0.6), name="100 observations"))
for l, c in ((0, RED), (10, GREEN), (100, ORANGE)):
    m, b = fit(l)
    fig.add_scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=c, width=4),
                    name=f"λ = {l}{' (OLS)' if l == 0 else ''}: slope {m:.2f}")
fig.add_scatter(x=[x.mean()], y=[y.mean()], mode="markers", marker=dict(size=14, color="black"), name="point of means")
fig.update_layout(template="simple_white", width=950, height=580, font=FONT, xaxis=dict(title="feature x"),
                  yaxis=dict(title="target y"), legend=dict(x=0.01, y=0.99), margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "ridge_lines.png", scale=2)
