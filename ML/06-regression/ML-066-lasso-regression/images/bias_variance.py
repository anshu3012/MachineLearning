"""Bias and variance of Lasso (Plotly frames -> GIF), the Notebook's experiment: y = 0.7x^2 - 2x + 3 plus noise
(sd 2), 20 fixed training x, a degree-16 polynomial (standardised), 200 fresh noise draws (seed 1). Left: 30 of the
200 fitted curves and their average against the true curve, for each alpha. Right: bias^2, variance and expected
test error against alpha; the error is lowest at alpha 0.1."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import Lasso
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

warnings.simplefilter("ignore")
here = Path(__file__).parent
f = lambda x: 0.7 * x ** 2 - 2 * x + 3
SD = 2.0
x_train = np.linspace(-2, 3, 20)[:, None]
x_test = (x_train[1:] + x_train[:-1]) / 2
grid = np.linspace(-2, 3, 200)[:, None]
ALPHAS = [0.001, 0.01, 0.1, 0.3, 1, 3]
WANT = {0.001: (0.009, 1.44), 0.01: (0.009, 0.95), 0.1: (0.04, 0.62), 0.3: (0.34, 0.54), 1: (2.52, 0.38), 3: (5.20, 0.19)}
res, curves = {}, {}
for a in ALPHAS:
    r = np.random.default_rng(1)
    pt, pg = [], []
    for _ in range(200):
        yy = f(x_train[:, 0]) + SD * r.standard_normal(len(x_train))
        m = make_pipeline(PolynomialFeatures(degree=16, include_bias=False), StandardScaler(),
                          Lasso(alpha=a, max_iter=100000)).fit(x_train, yy)
        pt.append(m.predict(x_test)); pg.append(m.predict(grid))
    pt = np.array(pt)
    b2, v = ((pt.mean(0) - f(x_test[:, 0])) ** 2).mean(), pt.var(0).mean()
    res[a] = (b2, v, b2 + v + SD ** 2)
    curves[a] = np.array(pg)
    wb, wv = WANT[a]
    assert abs(b2 - wb) < 0.006 and abs(v - wv) < 0.006, (a, b2, v)
assert min(res, key=lambda a: res[a][2]) == 0.1


def frame(k):
    a = ALPHAS[k]
    fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=[f"alpha = {a}: 30 of 200 fits", "bias², variance and error"])
    fig.update_annotations(font_size=21)
    for c in curves[a][:30]:
        fig.add_trace(go.Scatter(x=grid[:, 0], y=c, mode="lines", line=dict(color=BLUE, width=1), opacity=0.35), 1, 1)
    fig.add_trace(go.Scatter(x=grid[:, 0], y=f(grid[:, 0]), mode="lines", line=dict(color="black", width=4, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=grid[:, 0], y=curves[a].mean(0), mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    al = ALPHAS[:k + 1]
    for i, (c, n) in enumerate(((RED, "bias²"), (GREEN, "variance"), (GREY, "expected test error"))):
        fig.add_trace(go.Scatter(x=al, y=[res[x][i] for x in al], mode="lines+markers", line=dict(color=c, width=3),
                                 marker=dict(size=9), name=n, showlegend=True), 1, 2)
    fig.update_xaxes(title="x", row=1, col=1)
    fig.update_yaxes(title="y", range=[-4, 12], row=1, col=1)
    fig.update_xaxes(title="alpha (log scale)", type="log", range=[-3.2, 0.7], row=1, col=2)
    fig.update_yaxes(range=[0, 10], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.75, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=120))
    for tr in fig.data:
        if tr.name is None:
            tr.showlegend = False
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(len(ALPHAS))], here / "bias_variance", fps=1, holds=[2, 2, 3, 2, 2, 4], keys=[0, 5], cols=1)
