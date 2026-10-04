"""Left: one input, alpha 0 / 10 / 100: the slope shrinks. Right: degree-16 polynomial with alpha 0 / 20 / 200 (Plotly)."""
from pathlib import Path
import warnings
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

warnings.simplefilter("ignore")
here = Path(__file__).parent
colours = ["#E45756", "#54A24B", "#F58518"]
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
rng = np.random.default_rng(0)
x1 = 5 * rng.random((100, 1)) - 2
x2 = (0.7 * x1 ** 2 - 2 * x1 + 3 + rng.standard_normal((100, 1))).ravel()
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=("One input: larger α, flatter line", "Degree 16: α = 0 overfits, α = 200 underfits"))
fig.add_trace(go.Scatter(x=X.ravel(), y=y, mode="markers", marker=dict(size=6, color="#4C78A8", opacity=0.6),
                         showlegend=False), 1, 1)
xs = np.linspace(X.min(), X.max(), 2).reshape(-1, 1)
for a, c in zip([0, 10, 100], colours):
    m = (LinearRegression() if a == 0 else Ridge(alpha=a)).fit(X, y)
    fig.add_trace(go.Scatter(x=xs.ravel(), y=m.predict(xs), mode="lines", line=dict(color=c, width=3),
                             name=f"α = {a}: slope {m.coef_[0]:.1f}", legendgroup="a"), 1, 1)
fig.add_trace(go.Scatter(x=x1.ravel(), y=x2, mode="markers", marker=dict(size=6, color="#4C78A8", opacity=0.6),
                         showlegend=False), 1, 2)
grid = np.linspace(-2, 3, 400).reshape(-1, 1)
for a, c in zip([0, 20, 200], colours):
    p = make_pipeline(PolynomialFeatures(16), Ridge(alpha=a, solver="svd") if a else LinearRegression()).fit(x1, x2)
    fig.add_trace(go.Scatter(x=grid.ravel(), y=np.clip(p.predict(grid), -2, 16), mode="lines", line=dict(color=c, width=3),
                             name=f"degree 16, α = {a}", legendgroup="b"), 1, 2)
fig.update_xaxes(title="x", row=1, col=1); fig.update_yaxes(title="y", row=1, col=1)
fig.update_xaxes(title="x", row=1, col=2); fig.update_yaxes(range=[-1, 16], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=480, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), margin=dict(l=60, r=20, t=50, b=100))
fig.update_annotations(font_size=16)
fig.write_image(here / "alpha_effects.png", scale=2)
fig.write_image(here / "alpha_effects.pdf")
