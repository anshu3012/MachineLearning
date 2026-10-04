"""Bias² and variance of a degree-15 Ridge model against alpha: 15 fixed training x, fresh noise each draw,
measured against the true curve (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
f = lambda x: 0.7 * x ** 2 - 2 * x + 3                 # the true curve
SD = 2.0                                               # noise standard deviation
x_train = np.linspace(-2, 3, 15)[:, None]              # 15 fixed training x
x_test = (x_train[1:] + x_train[:-1]) / 2              # 14 test x between them

def decompose(alpha, draws=300):
    """Expected test error, bias² and variance over 300 fresh training sets (new noise each time)."""
    r = np.random.default_rng(1)
    preds = []
    for _ in range(draws):
        y = f(x_train[:, 0]) + SD * r.standard_normal(len(x_train))
        model = make_pipeline(PolynomialFeatures(degree=15), StandardScaler(), Ridge(alpha=alpha))
        preds.append(model.fit(x_train, y).predict(x_test))
    preds = np.array(preds)
    bias2 = ((preds.mean(0) - f(x_test[:, 0])) ** 2).mean()
    var = preds.var(0).mean()
    return bias2 + var + SD ** 2, bias2, var

alphas = np.logspace(-4, 3, 50)
res = np.array([decompose(a) for a in alphas])
for a in (0.0001, 0.01, 1, 10, 100, 1000):
    l, b, v = decompose(a); print(a, round(l, 2), round(b, 3), round(v, 2))
best = alphas[res[:, 0].argmin()]; print("best", best, res[:, 0].min())

x = alphas
fig = go.Figure()
for k, (name, col) in enumerate((("expected test error", "#4C78A8"), ("bias²", "#E45756"), ("variance", "#F58518"))):
    fig.add_trace(go.Scatter(x=x, y=res[:, k], mode="lines", name=name, line=dict(color=col, width=4)))
fig.add_trace(go.Scatter(x=[best], y=[res[:, 0].min()], mode="markers+text", marker=dict(size=13, color="#4C78A8"),
                         text=[f"lowest at alpha ≈ {best:.2g}"], textposition="top center", showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=480, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=70, r=30, t=60, b=60), legend=dict(x=0.02, y=0.5),
                  title=dict(text="Degree-15 polynomial with Ridge: more alpha, less variance, more bias", x=0.5),
                  xaxis=dict(type="log", title="alpha (log scale)", exponentformat="power", dtick=1),
                  yaxis=dict(title="mean squared error (log scale)", type="log"))
fig.write_image(here / "bias_variance.png", scale=2)
fig.write_image(here / "bias_variance.pdf")
