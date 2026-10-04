"""Why multicollinearity makes coefficients unreliable (Plotly frames -> GIF). The model is refitted on 20
bootstrap resamples of the 140 training observations. Left: the Note's own features; feature1's coefficient
barely moves. Right: the same data plus a near-copy of feature1 (feature1 + small noise, VIF far above 5); the
coefficients of feature1 and its copy swing wildly in opposite directions, while their sum, the effect of the
pair, stays put. Data: data/data.csv, split as in common.py."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant
from common import X_train, y_train
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
rng = np.random.default_rng(0)
copy = X_train[:, 0] + rng.normal(scale=0.05 * X_train[:, 0].std(), size=len(X_train))
Xc = np.c_[X_train, copy]
VIF = variance_inflation_factor(add_constant(Xc), 1)
assert VIF > 100, VIF
N = 20
plain, coll = [], []
for _ in range(N):
    i = rng.integers(0, len(X_train), len(X_train))
    plain.append(LinearRegression().fit(X_train[i], y_train[i]).coef_[0])
    c = LinearRegression().fit(Xc[i], y_train[i]).coef_
    coll.append((c[0], c[3]))
plain, coll = np.array(plain), np.array(coll)
SUMS = coll.sum(1)
assert np.ptp(coll[:, 0]) > 5 * np.ptp(plain) and np.ptp(SUMS) < 1.5 * np.ptp(plain)
print(f"VIF {VIF:.0f}; plain feature1 {plain.min():.1f}..{plain.max():.1f}; collinear feature1 "
      f"{coll[:, 0].min():.1f}..{coll[:, 0].max():.1f}; sum {SUMS.min():.1f}..{SUMS.max():.1f}")
LO, HI = min(coll.min(), plain.min()) - 10, max(coll.max(), plain.max()) + 10


def frame(k):
    fig = make_subplots(1, 2, horizontal_spacing=0.1, shared_yaxes=True,
                        subplot_titles=["the Note's features (VIF 1.01)", f"plus a near-copy of feature1 (VIF {VIF:.0f})"])
    fig.update_annotations(font_size=22)
    r = np.arange(1, k + 1)
    fig.add_trace(go.Scatter(x=r, y=plain[:k], mode="lines+markers", name="feature1", line=dict(color=BLUE, width=3),
                             marker=dict(size=9)), 1, 1)
    fig.add_trace(go.Scatter(x=r, y=coll[:k, 0], mode="lines+markers", name="feature1", showlegend=False,
                             line=dict(color=BLUE, width=3), marker=dict(size=9)), 1, 2)
    fig.add_trace(go.Scatter(x=r, y=coll[:k, 1], mode="lines+markers", name="near-copy of feature1",
                             line=dict(color=ORANGE, width=3), marker=dict(size=9)), 1, 2)
    fig.add_trace(go.Scatter(x=r, y=SUMS[:k], mode="lines+markers", name="their sum",
                             line=dict(color=GREEN, width=3, dash="dash"), marker=dict(size=7)), 1, 2)
    fig.update_xaxes(title="resample of the training data", range=[0.5, N + 0.5])
    fig.update_yaxes(title="fitted coefficient", range=[LO, HI], row=1, col=1)
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
                      title=dict(text=f"refit {k} of {N}", x=0.02, y=0.97), margin=dict(l=80, r=30, t=80, b=130))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(1, N + 1)], here / "collinear_coefs", fps=3, holds=[1] * (N - 1) + [8],
             keys=[N - 1], cols=1, width=900)
