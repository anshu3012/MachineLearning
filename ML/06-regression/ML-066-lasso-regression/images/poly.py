"""Degree-16 polynomial with Lasso on curved data: alpha 0 overfits, a middle alpha follows the curve, a large alpha underfits (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
rng = np.random.default_rng(42)
x = 5 * rng.random((100, 1)) - 2
y = 0.7 * x[:, 0] ** 2 - 2 * x[:, 0] + 3 + rng.standard_normal(100)
xs = np.linspace(x.min(), x.max(), 400)[:, None]
fig = go.Figure(go.Scatter(x=x[:, 0], y=y, mode="markers", marker=dict(color="#BBBBBB", size=7), name="data"))
for a, c in ((0, "#E45756"), (0.1, "#54A24B"), (2, "#4C78A8")):
    model = make_pipeline(PolynomialFeatures(degree=16, include_bias=False), StandardScaler(),
                          LinearRegression() if a == 0 else Lasso(alpha=a, max_iter=200000))
    model.fit(x, y)
    coef = model[-1].coef_
    print(a, "non-zero", (coef != 0).sum(), "of", coef.size)
    fig.add_trace(go.Scatter(x=xs[:, 0], y=model.predict(xs), mode="lines", line=dict(color=c, width=4),
                             name=f"alpha {a}: {(coef != 0).sum()} of 16 coefficients non-zero"))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=70, r=30, t=40, b=60), legend=dict(x=0.35, y=0.98),
                  xaxis=dict(title="x"), yaxis=dict(title="y", range=[-1, 14]))
fig.write_image(here / "poly.png", scale=2)
fig.write_image(here / "poly.pdf")
