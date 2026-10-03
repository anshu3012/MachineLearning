"""Bias² and variance of a degree-15 Ridge model against alpha, by bootstrap resampling of the training set (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
rng = np.random.default_rng(42)
X = 5 * rng.random((100, 1)) - 2
y = 0.7 * X[:, 0] ** 2 - 2 * X[:, 0] + 3 + rng.standard_normal(100)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)

def decompose(alpha, rounds=200):
    r = np.random.default_rng(123)
    preds = []
    for _ in range(rounds):
        i = r.integers(0, len(ytr), len(ytr))          # bootstrap sample of the training rows
        model = make_pipeline(PolynomialFeatures(degree=15), StandardScaler(), Ridge(alpha=alpha))
        preds.append(model.fit(Xtr[i], ytr[i]).predict(Xte))
    preds = np.array(preds)
    loss = ((preds - yte) ** 2).mean()
    bias2 = ((preds.mean(0) - yte) ** 2).mean()
    var = preds.var(0).mean()
    return loss, bias2, var

alphas = np.logspace(-2, 3, 60)
res = np.array([decompose(a) for a in alphas])
for a in (0, 0.01, 0.1, 1, 10, 100, 1000):
    l, b, v = decompose(a); print(a, round(l, 2), round(b, 2), round(v, 2))
best = alphas[res[:, 0].argmin()]; print("best", best, res[:, 0].min())

x = alphas
fig = go.Figure()
for k, (name, col) in enumerate((("expected test error", "#4C78A8"), ("bias² (+ noise)", "#E45756"), ("variance", "#F58518"))):
    fig.add_trace(go.Scatter(x=x, y=res[:, k], mode="lines", name=name, line=dict(color=col, width=4)))
fig.add_trace(go.Scatter(x=[best], y=[res[:, 0].min()], mode="markers+text", marker=dict(size=13, color="#4C78A8"),
                         text=[f"lowest at alpha ≈ {best:.2g}"], textposition="top center", showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=480, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=70, r=30, t=60, b=60), legend=dict(x=0.72, y=0.98),
                  title=dict(text="Degree-15 polynomial with Ridge: more alpha, less variance, more bias", x=0.5),
                  xaxis=dict(type="log", title="alpha (log scale)", exponentformat="power", dtick=1),
                  yaxis=dict(title="mean squared error (log scale)", type="log", exponentformat="power", dtick=1))
fig.write_image(here / "bias_variance.png", scale=2)
fig.write_image(here / "bias_variance.pdf")
