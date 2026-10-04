"""Gradient descent on the Ridge loss for one input, λ = 0 and λ = 100: contours and paths (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
ms, bs = np.linspace(-10, 40, 200), np.linspace(-30, 25, 200)
M, B = np.meshgrid(ms, bs)

def loss(m, b, lam):
    return 0.5 * (((y[:, None, None] - m * x[:, None, None] - b) ** 2).sum(0) + lam * m ** 2)

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=("λ = 0 (linear regression)", "λ = 100 (Ridge)"))
for col, lam in ((1, 0), (2, 100)):
    m, b, lr, path = -5.0, 20.0, 0.005, [(-5.0, 20.0)]
    for _ in range(60):
        err = y - m * x - b
        dm, db = -(err * x).sum() + lam * m, -err.sum()
        m, b = m - lr * dm, b - lr * db
        path.append((m, b))
    print(lam, path[-1])
    Z = loss(M, B, lam)
    fig.add_trace(go.Contour(x=ms, y=bs, z=np.log(Z), showscale=False, colorscale="Blues", reversescale=True,
                             contours=dict(coloring="lines", start=np.log(Z.min()) + 0.05, end=np.log(Z.max()), size=0.25),
                             line=dict(width=1.5)), 1, col)
    pm, pb = zip(*path)
    fig.add_trace(go.Scatter(x=pm, y=pb, mode="lines+markers", line=dict(color="#F58518", width=3), marker=dict(size=5)), 1, col)
    fig.add_trace(go.Scatter(x=[pm[-1]], y=[pb[-1]], mode="markers", marker=dict(size=14, color="#E45756", symbol="star")), 1, col)
    fig.add_annotation(x=pm[-1], y=pb[-1] - 6, text=f"m = {pm[-1]:.1f}, b = {pb[-1]:.1f}".replace("-", "−"), showarrow=False,
                       font=dict(size=15, color="#E45756"), bgcolor="white", row=1, col=col)
fig.update_xaxes(title="slope m", range=[-10, 40])
fig.update_yaxes(title="intercept b", range=[-30, 25])
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=30, t=60, b=60))
fig.write_image(here / "paths.png", scale=2)
fig.write_image(here / "paths.pdf")
