"""Two figures for the perceptron code (Plotly), from the Note's run: 100 points, learning rate 0.1, seed 0.
weights_trace.png (section 3): w0, w1, w2 after every one of the 1,000 loops. They change only on the 6 loops whose
  picked point was misclassified (1, 8, 31, 40, 44, 108) and never after loop 108.
line_from_weights.png (section 4): the final weights turned into a line: x2 = -(w1/w2) x1 - w0/w2."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_classification

here = Path(__file__).parent
BLUE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
font = dict(family="Latin Modern Roman", size=22)
X, y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=10)
Xb = np.insert(X, 0, 1, axis=1)
rng = np.random.default_rng(0)
w = np.ones(3); W = [w.copy()]; upd = []
for i in range(1000):
    j = rng.integers(0, 100)
    y_hat = 1 if Xb[j] @ w > 0 else 0
    if y[j] != y_hat:
        upd.append(i + 1)
    w = w + 0.1 * (y[j] - y_hat) * Xb[j]
    W.append(w.copy())
W = np.array(W)
assert upd == [1, 8, 31, 40, 44, 108]                                   # the Note's table
assert np.allclose(W[108].round(2), [1.00, 1.34, 0.19]) and np.allclose(W[108], W[-1])
assert all((Xb @ W[-1] > 0) == (y == 1))                               # no training point misclassified

# ---- weights after every loop ----
loops = np.arange(1001)
x_plot = np.where(loops == 0, 0.7, loops)                              # log axis: draw the start just left of loop 1
fig = go.Figure()
for k, (name, c) in enumerate([("w<sub>0</sub> (intercept)", GREY), ("w<sub>1</sub> (weight of x<sub>1</sub>)", RED), ("w<sub>2</sub> (weight of x<sub>2</sub>)", BLUE)]):
    fig.add_trace(go.Scatter(x=x_plot, y=W[:, k], mode="lines", line=dict(color=c, width=4, shape="hv"), name=name))
    fig.add_trace(go.Scatter(x=upd, y=W[upd, k], mode="markers", marker=dict(size=11, color=c), showlegend=False))
for u in upd:
    fig.add_vline(x=u, line=dict(color="#DDDDDD", width=2))
fig.add_annotation(x=np.log10(400), y=0.45, text="loops 109–1,000:<br>no misclassified point left,<br>no change",
                   showarrow=False, font=dict(size=20))
fig.update_layout(template="simple_white", width=1100, height=560, font=font,
                  xaxis=dict(title="loop (log scale); grey lines: the 6 updates", type="log",
                             tickvals=[0.7, 1, 8, 31, 108, 1000], ticktext=["start", "1", "8", "31", "108", "1000"],
                             range=[np.log10(0.6), np.log10(1100)]),
                  yaxis=dict(title="weight", range=[0, 1.5]), margin=dict(l=80, r=20, t=30, b=80),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12))
fig.write_image(here / "weights_trace.png", scale=2)
fig.write_image(here / "weights_trace.pdf")

# ---- from weights to a line ----
w0, w1, w2 = W[-1]
m, b = -w1 / w2, -w0 / w2
assert round(m, 2) == -7.02 and round(b, 2) == -5.23
fig = go.Figure()
for cls, c in [(0, BLUE), (1, GREEN)]:
    fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", name=f"class {cls}",
                             marker=dict(size=10, color=c)))
xs = np.array([-1.2, 0.2])
fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=RED, width=5),
                         name=f"line: x<sub>2</sub> = −{-m:.2f} x<sub>1</sub> − {-b:.2f}"))
fig.add_trace(go.Scatter(x=[0], y=[b], mode="markers", marker=dict(size=16, color=PURPLE, symbol="diamond"),
                         name=f"crosses x<sub>1</sub> = 0 at b = −w<sub>0</sub>/w<sub>2</sub> = −{-b:.2f}"))
fig.add_annotation(x=(-3.5 - b) / m, y=-3.5, text=f"slope m = −w<sub>1</sub>/w<sub>2</sub> = −{-m:.2f}:<br>steep, because w<sub>2</sub> is small",
                   showarrow=True, arrowhead=2, ax=-260, ay=60, font=dict(size=20), align="left")
fig.update_layout(template="simple_white", width=1000, height=640, font=font,
                  xaxis=dict(title="x<sub>1</sub>", zeroline=True), yaxis=dict(title="x<sub>2</sub>", range=[-6.2, 3], zeroline=True),
                  margin=dict(l=80, r=20, t=30, b=150), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.16))
fig.write_image(here / "line_from_weights.png", scale=2)
fig.write_image(here / "line_from_weights.pdf")
print("updates at loops", upd, "final w", W[-1].round(2), "m, b", round(m, 2), round(b, 2), "x1 range", X[:, 0].min().round(2), X[:, 0].max().round(2), "x2", X[:, 1].min().round(2), X[:, 1].max().round(2))
