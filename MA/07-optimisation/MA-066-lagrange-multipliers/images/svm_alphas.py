"""The SVM dual on real data (Plotly): Iris setosa against versicolor, petal length and petal width (100 flowers).
A hard-margin linear SVC (C = 1e6). Each flower's dual multiplier alpha_i is drawn as the size of a ring: only the
support vectors on the margin have alpha > 0; every other flower has alpha = 0 and does not enter w."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE

here = Path(__file__).parent
iris = load_iris()
m = iris.target < 2
X, y = iris.data[m][:, 2:], np.where(iris.target[m] == 0, -1, 1)
svm = SVC(kernel="linear", C=1e6).fit(X, y)
alpha = np.zeros(len(X)); alpha[svm.support_] = np.abs(svm.dual_coef_[0])
w = (svm.dual_coef_[0] @ X[svm.support_])
assert np.allclose(w, svm.coef_[0]) and len(svm.support_) <= 3 and (alpha > 0).sum() == len(svm.support_)
assert abs((alpha * y).sum()) < 1e-6
b = svm.intercept_[0]
xs = np.linspace(0.8, 5.3, 2)
fig = go.Figure()
for off, dash, name in ((0, "solid", "decision boundary"), (1, "dash", "margin"), (-1, "dash", None)):
    fig.add_scatter(x=xs, y=(off - b - w[0] * xs) / w[1], mode="lines", line=dict(color=GREY, width=3 if off == 0 else 2, dash=dash),
                    name=name, showlegend=name is not None)
for cls, c, name in ((-1, BLUE, "setosa (α = 0 unless ringed)"), (1, ORANGE, "versicolor (α = 0 unless ringed)")):
    k = y == cls
    fig.add_scatter(x=X[k, 0], y=X[k, 1], mode="markers", marker=dict(size=9, color=c, opacity=0.7), name=name)
sv = svm.support_
fig.add_scatter(x=X[sv, 0], y=X[sv, 1], mode="markers+text", text=[f"α = {a:.2f}" for a in alpha[sv]],
                textposition="middle right", textfont=dict(size=19, color=GREEN),
                marker=dict(size=14 + 30 * alpha[sv] / alpha.max(), color="rgba(0,0,0,0)", line=dict(color=GREEN, width=3)),
                name="support vectors (α > 0)")
fig.update_layout(template="simple_white", width=1000, height=700, font=FONT,
                  xaxis=dict(title="petal length (cm)", range=[0.8, 5.3]), yaxis=dict(title="petal width (cm)", range=[0, 2]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=70, r=30, t=20, b=150))
fig.write_image(here / "svm_alphas.png", scale=2)
assert len(sv) == 2 and np.allclose(alpha[sv], 1.1765, atol=1e-3)
