"""Polynomial regression on y = 0.8x^2 + 0.9x + 2 + noise. Left: degree 1, 2 and 15 fitted to 25 training points.
Right: training and test R2 against the degree (Plotly). Fixed seed."""
from pathlib import Path
import warnings
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

warnings.simplefilter("ignore")
here = Path(__file__).parent
rng = np.random.default_rng(42)
f = lambda x: 0.8 * x ** 2 + 0.9 * x + 2
X_tr = 6 * rng.random((25, 1)) - 3; y_tr = f(X_tr).ravel() + rng.standard_normal(25)
X_te = 6 * rng.random((200, 1)) - 3; y_te = f(X_te).ravel() + rng.standard_normal(200)
model = lambda d: make_pipeline(PolynomialFeatures(d, include_bias=False), StandardScaler(), LinearRegression()).fit(X_tr, y_tr)
fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                    subplot_titles=("Fits of degree 1, 2 and 15 on 25 training points", "R² against degree"))
xs = np.linspace(-3, 3, 400).reshape(-1, 1)
fig.add_trace(go.Scatter(x=X_te.ravel(), y=y_te, mode="markers", name="test points", marker=dict(size=5, color="#BBBBBB")), 1, 1)
fig.add_trace(go.Scatter(x=X_tr.ravel(), y=y_tr, mode="markers", name="training points", marker=dict(size=8, color="#4C78A8")), 1, 1)
for d, colour in ((1, "#E45756"), (2, "#54A24B"), (15, "#F58518")):
    m = model(d)
    fig.add_trace(go.Scatter(x=xs.ravel(), y=np.clip(m.predict(xs), -5, 15), mode="lines",
                             name=f"degree {d}: test R² {m.score(X_te, y_te):.2f}", line=dict(color=colour, width=3)), 1, 1)
degs = list(range(1, 17))
tr = [model(d).score(X_tr, y_tr) for d in degs]; te = [model(d).score(X_te, y_te) for d in degs]
fig.add_trace(go.Scatter(x=degs, y=tr, mode="lines+markers", name="training R²", line=dict(color="#4C78A8", width=3)), 1, 2)
fig.add_trace(go.Scatter(x=degs, y=np.clip(te, -1, 1), mode="lines+markers", name="test R²", line=dict(color="#F58518", width=3)), 1, 2)
fig.update_xaxes(title="x", row=1, col=1); fig.update_yaxes(title="y", range=[-5, 15], row=1, col=1)
fig.update_xaxes(title="degree", row=1, col=2); fig.update_yaxes(title="R²", range=[-1, 1.02], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), margin=dict(l=60, r=20, t=50, b=100))
fig.update_annotations(font_size=16)
for d in (1, 2, 3, 6, 10, 15):
    print(d, round(tr[d - 1], 3), round(te[d - 1], 3))
fig.write_image(here / "degrees.png", scale=2)
fig.write_image(here / "degrees.pdf")
