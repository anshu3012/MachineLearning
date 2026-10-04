"""Two figures for the Lasso slope formula (Plotly).
cases_derivative.png (section 3): the derivative of the loss L = D m^2 - 2 S m + 2 lambda |m| (constant dropped), with
  S = 100, D = 50, for lambda = 50, 100, 150. Each side of m = 0 has its own straight line (case m > 0, case m < 0).
  Where a line crosses 0 on its own side, that is the slope; when the jump at m = 0 straddles 0, the slope is 0.
sklearn_check.png (section 6): the formula against scikit-learn's Lasso on the 100-observation example (alpha = lambda / n)."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso

warnings.simplefilter("ignore")
here = Path(__file__).parent
RED, BLUE, GREY, GREEN = "#E45756", "#4C78A8", "#9A9A9A", "#54A24B"
font = dict(family="Latin Modern Roman", size=20)


def lasso_slope(S, D, lam):
    return (S - lam) / D if S > lam else (S + lam) / D if S < -lam else 0.0


# ---- Figure: the two cases of the derivative ----
S, D = 100.0, 50.0
pos = lambda m, lam: 2 * (D * m - S + lam)       # dL/dm for m > 0
neg = lambda m, lam: 2 * (D * m - S - lam)       # dL/dm for m < 0
lams = [50, 100, 150]
assert [lasso_slope(S, D, l) for l in lams] == [1.0, 0.0, 0.0]
assert pos(1.0, 50) == 0 and pos(0, 150) == 100 and neg(0, 150) == -500   # lambda = 150: jump from -500 to +100 spans 0
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=[f"λ = {l}: slope {lasso_slope(S, D, l):g}" for l in lams])
mp, mn = np.linspace(0, 2.5, 50), np.linspace(-1.5, 0, 50)
for c, lam in enumerate(lams, start=1):
    fig.add_trace(go.Scatter(x=mn, y=neg(mn, lam), mode="lines", line=dict(color=BLUE, width=5),
                             name="case m < 0: 2(Dm − S − λ)", showlegend=c == 1), 1, c)
    fig.add_trace(go.Scatter(x=mp, y=pos(mp, lam), mode="lines", line=dict(color=RED, width=5),
                             name="case m > 0: 2(Dm − S + λ)", showlegend=c == 1), 1, c)
    fig.add_trace(go.Scatter(x=[0, 0], y=[neg(0, lam), pos(0, lam)], mode="lines", line=dict(color=GREY, width=3, dash="dot"),
                             name="jump at the corner m = 0", showlegend=c == 1), 1, c)
    m = lasso_slope(S, D, lam)
    fig.add_trace(go.Scatter(x=[m], y=[0], mode="markers", marker=dict(size=18, color=GREEN, symbol="star"),
                             name="lowest loss: derivative changes sign", showlegend=c == 1), 1, c)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=c)
    fig.update_xaxes(title="slope m", range=[-1.5, 2.5], row=1, col=c)
fig.update_yaxes(title="dL/dm", range=[-560, 360], row=1, col=1)
fig.update_layout(template="simple_white", width=1300, height=560, font=font, margin=dict(l=80, r=20, t=60, b=160),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25))
fig.update_annotations(font_size=22)
fig.write_image(here / "cases_derivative.png", scale=2)
fig.write_image(here / "cases_derivative.pdf")

# ---- Figure: formula against scikit-learn ----
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
S, D = ((x - x.mean()) * (y - y.mean())).sum(), ((x - x.mean()) ** 2).sum()
assert round(S, 2) == 2416.73 and round(D, 2) == 86.85
grid = np.linspace(0, 3200, 321)
check = np.array([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2416.73, 2750, 3000])
sk = np.array([Lasso(alpha=l / len(x), tol=1e-10, max_iter=100000).fit(X, y).coef_[0] if l else
               lasso_slope(S, D, 0) for l in check])
form = np.array([lasso_slope(S, D, l) for l in check])
assert np.allclose(sk, form, atol=1e-3), np.c_[check, sk, form]
for l, v in [(500, 22.071), (1000, 16.313), (2000, 4.799)]:
    assert round(lasso_slope(S, D, l), 3) == v
fig = go.Figure()
fig.add_trace(go.Scatter(x=grid, y=[lasso_slope(S, D, l) for l in grid], mode="lines", line=dict(color=RED, width=5),
                         name="formula (S − λ) / D, or 0"))
fig.add_trace(go.Scatter(x=check[1:], y=sk[1:], mode="markers", name="scikit-learn Lasso, alpha = λ / 100",
                         marker=dict(size=15, color="white", line=dict(color="black", width=3))))
fig.add_annotation(x=S, y=0, text="λ = S = 2416.73: slope 0", showarrow=True, arrowhead=2, ax=40, ay=-90, font=dict(size=20))
fig.update_layout(template="simple_white", width=1000, height=560, font=font, xaxis=dict(title="λ"),
                  yaxis=dict(title="slope m", range=[-2, 30]), margin=dict(l=80, r=20, t=30, b=90),
                  legend=dict(x=0.45, y=0.98))
fig.write_image(here / "sklearn_check.png", scale=2)
fig.write_image(here / "sklearn_check.pdf")
print("OLS slope", round(S / D, 3), "max |formula - sklearn|", float(np.abs(sk - form).max()))
