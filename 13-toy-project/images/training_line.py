"""Section 8, what fit does: gradient descent on logistic regression's own objective (log loss plus scikit-learn's
default L2 penalty, C = 1) on the 90 scaled training students. Each frame draws the current lines where the predicted
probability is 0.5 (solid) and 0.1 or 0.9 (dashed); the dashed lines close in as the weights grow, and the 0.5 line it settles on the line of the fitted model, which the script checks against scikit-learn.
Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from toy_model import load
from gifkit import save_gif

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
df, X_train, X_test, y_train, y_test, scaler, clf = load()
Z = scaler.transform(X_train)
y = y_train.values
w, b, lr = np.zeros(2), 0.0, 0.05
snaps = {}
for it in range(3001):
    if it in (0, 1, 3, 10, 30, 100, 3000):
        snaps[it] = (w.copy(), b)
    p = 1 / (1 + np.exp(-(Z @ w + b)))
    gw = Z.T @ (p - y) + w                      # gradient of sum(log loss) + 0.5 ||w||^2  (C = 1)
    gb = (p - y).sum()
    w, b = w - lr * gw / len(y), b - lr * gb / len(y)
assert np.allclose(snaps[3000][0], clf.coef_[0], atol=0.02) and abs(snaps[3000][1] - clf.intercept_[0]) < 0.02
mu, sd = scaler.mean_, scaler.scale_


def frame(it):
    wv, bv = snaps[it]
    acc = ((Z @ wv + bv > 0).astype(int) == y).mean()
    fig = go.Figure()
    for label, colour, name in [(1, "#54A24B", "placed"), (0, "#E45756", "not placed")]:
        m = y == label
        fig.add_scatter(x=X_train.cgpa[m], y=X_train.iq[m], mode="markers", name=name, marker=dict(color=colour, size=9, opacity=0.7))
    if np.abs(wv).sum() > 0:
        cg = np.linspace(3, 9, 50)                # w1 (cg - mu1)/sd1 + w2 (iq - mu2)/sd2 + b = t, solved for iq
        for t, dash, name in ((0.0, "solid", "probability 0.5"), (np.log(9), "dash", "probability 0.9 / 0.1"), (-np.log(9), "dash", None)):
            iq = mu[1] - sd[1] / wv[1] * (wv[0] * (cg - mu[0]) / sd[0] + bv - t)
            fig.add_scatter(x=cg, y=iq, mode="lines", line=dict(color="black", width=4 if t == 0 else 2, dash=dash),
                            name=name, showlegend=name is not None)
    title = "start: all weights 0, no line yet" if it == 0 else f"after {it:,} gradient step{'s' if it > 1 else ''}"
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                      title=dict(text=f"{title} · training accuracy {acc:.0%}", x=0.5),
                      xaxis=dict(title="CGPA", range=[3, 9]), yaxis=dict(title="IQ", range=[30, 240]),
                      legend=dict(x=1.01, y=1), margin=dict(l=70, r=20, t=70, b=60))
    return fig


if __name__ == "__main__":
    its = sorted(snaps)
    save_gif([frame(i) for i in its], "training_line", HERE, keys=[1, 4, 5, 6], fps=1, holds=[1] * (len(its) - 1) + [4])
