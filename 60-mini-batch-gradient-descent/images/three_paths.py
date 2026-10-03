"""Batch, stochastic and mini-batch (batch size 10) gradient descent on the 100-point example, 3 epochs each,
same learning rate 0.05 (Plotly). Fixed seed."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1, noise=20, random_state=13)
x = X.ravel(); n = len(x)
best_m, best_b = np.polyfit(x, y, 1)


def run(batch_size, epochs=3, lr=0.05, seed=2, m=-127.82, b=150.0):
    rng = np.random.default_rng(seed); path = [(m, b)]
    for _ in range(epochs):
        idx = rng.permutation(n)
        for s in range(0, n, batch_size):
            j = idx[s:s + batch_size]; err = y[j] - m * x[j] - b
            m, b = m + lr * 2 * np.mean(err * x[j]), b + lr * 2 * np.mean(err)
            path.append((m, b))
    return np.array(path)


cases = [(n, "Batch: 1 update per epoch", "#E45756"), (1, "Stochastic: 100 updates per epoch", "#F58518"),
         (10, "Mini-batch of 10: 10 updates per epoch", "#54A24B")]
mg, bg = np.linspace(-150, 150, 100), np.linspace(-150, 170, 100)
Z = np.array([[np.mean((y - mm * x - bb) ** 2) for mm in mg] for bb in bg])
fig = make_subplots(1, 3, horizontal_spacing=0.05, subplot_titles=[c[1] for c in cases])
for col, (bs, name, colour) in enumerate(cases, start=1):
    p = run(bs)
    fig.add_trace(go.Contour(x=mg, y=bg, z=Z, colorscale="Blues", reversescale=True, showscale=False, ncontours=20,
                             line=dict(width=0.4)), 1, col)
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines+markers", line=dict(color=colour, width=2.5),
                             marker=dict(size=4 if bs < n else 8, color=colour)), 1, col)
    fig.add_trace(go.Scatter(x=[best_m], y=[best_b], mode="markers", marker=dict(size=12, color="black", symbol="x")), 1, col)
    fig.update_xaxes(title="m", row=1, col=col)
    print(name, len(p) - 1, "updates, end", p[-1].round(2))
fig.update_yaxes(title="b", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=14), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=15)
fig.write_image(here / "three_paths.png", scale=2)
fig.write_image(here / "three_paths.pdf")
