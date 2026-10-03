"""Batch vs stochastic gradient descent on the 100-point example (m and b): paths on the loss contours,
and a close-up near the minimum with a constant learning rate vs a decreasing learning schedule (Plotly).
Fixed random seed so the paths repeat."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1, noise=20, random_state=13)
x = X.ravel()
n = len(x)
best_m, best_b = np.polyfit(x, y, 1)


def batch(epochs, lr=0.5, m=-127.82, b=150.0):
    path = [(m, b)]
    for _ in range(epochs):
        err = y - m * x - b
        m, b = m + lr * 2 * np.mean(err * x), b + lr * 2 * np.mean(err)
        path.append((m, b))
    return np.array(path)


def sgd(epochs, lr_fn, seed=1, m=-127.82, b=150.0):
    rng = np.random.default_rng(seed); path = [(m, b)]; t = 0
    for _ in range(epochs):
        for _ in range(n):
            i = rng.integers(n); err = y[i] - m * x[i] - b; lr = lr_fn(t); t += 1
            m, b = m + lr * 2 * err * x[i], b + lr * 2 * err
            path.append((m, b))
    return np.array(path)


pb = batch(10)
ps_const = sgd(5, lambda t: 0.05)
ps_sched = sgd(5, lambda t: 5 / (t + 50))
mg, bg = np.linspace(-150, 150, 120), np.linspace(-150, 170, 120)
Z = np.array([[np.mean((y - mm * x - bb) ** 2) for mm in mg] for bb in bg])
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=(
    "10 batch updates vs 1 epoch of SGD (100 updates)", "Near the minimum: constant vs decreasing learning rate"))
fig.add_trace(go.Contour(x=mg, y=bg, z=Z, colorscale="Blues", reversescale=True, showscale=False, ncontours=25,
                         line=dict(width=0.5)), 1, 1)
fig.add_trace(go.Scatter(x=ps_const[:101, 0], y=ps_const[:101, 1], mode="lines", name="stochastic, constant rate 0.05",
                         line=dict(color=ORANGE, width=2)), 1, 1)
fig.add_trace(go.Scatter(x=pb[:, 0], y=pb[:, 1], mode="lines+markers", name="batch, 10 epochs",
                         line=dict(color=RED, width=3), marker=dict(size=7)), 1, 1)
z = 12
mz, bz = np.linspace(best_m - z, best_m + z, 80), np.linspace(best_b - z, best_b + z, 80)
Zz = np.array([[np.mean((y - mm * x - bb) ** 2) for mm in mz] for bb in bz])
fig.add_trace(go.Contour(x=mz, y=bz, z=Zz, colorscale="Blues", reversescale=True, showscale=False, ncontours=15,
                         line=dict(width=0.5)), 1, 2)
tail = slice(200, None)
fig.add_trace(go.Scatter(x=ps_const[tail, 0], y=ps_const[tail, 1], mode="lines", name="constant rate 0.05", showlegend=False,
                         line=dict(color=ORANGE, width=1.5)), 1, 2)
fig.add_trace(go.Scatter(x=ps_sched[tail, 0], y=ps_sched[tail, 1], mode="lines", name="stochastic, schedule 5/(t+50)",
                         line=dict(color=GREEN, width=2.5)), 1, 2)
fig.add_trace(go.Scatter(x=[best_m], y=[best_b], mode="markers", name="minimum (OLS)",
                         marker=dict(size=13, color="black", symbol="x")), 1, 2)
fig.update_xaxes(title="m", row=1, col=1); fig.update_yaxes(title="b", row=1, col=1)
fig.update_xaxes(title="m", range=[best_m - z, best_m + z], row=1, col=2)
fig.update_yaxes(range=[best_b - z, best_b + z], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=520, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"), margin=dict(l=60, r=20, t=50, b=90))
fig.update_annotations(font_size=16)
spread = lambda p: float(np.mean(np.hypot(p[300:, 0] - best_m, p[300:, 1] - best_b)))
print("best", round(best_m, 2), round(best_b, 2), "batch end", pb[-1].round(2),
      "avg distance last 200 updates: const", round(spread(ps_const), 2), "schedule", round(spread(ps_sched), 2))
fig.write_image(here / "paths.png", scale=2)
fig.write_image(here / "paths.pdf")
