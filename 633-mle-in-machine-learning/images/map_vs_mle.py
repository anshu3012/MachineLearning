"""MLE versus MAP for a degree-9 polynomial on the 10 points of overfit.py. MAP uses a Gaussian prior N(0, 0.1^2)
on every coefficient and noise sigma = 0.2, so lambda = sigma^2 / b^2 = 4: the ridge solution (Phi^T Phi + 4 I)^-1 Phi^T y."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(4)                                 # same data as overfit.py
truth = lambda x: -np.sin(x / 5) + np.cos(x)
x = np.linspace(-4.5, 4.5, 10) + rng.uniform(-0.3, 0.3, 10)
y = truth(x) + rng.normal(0, 0.2, 10)
xt = np.linspace(-4.5, 4.5, 200)
yt = truth(xt) + rng.normal(0, 0.2, 200)
phi = lambda v: np.vander(v, 10, increasing=True)
LAM = 0.2 ** 2 / 0.1 ** 2
mle = np.linalg.lstsq(phi(x), y, rcond=None)[0]
map_ = np.linalg.solve(phi(x).T @ phi(x) + LAM * np.eye(10), phi(x).T @ y)
rm = lambda th: np.sqrt(np.mean((phi(xt) @ th - yt) ** 2))
assert LAM == 4 and rm(map_) < rm(mle) / 2

g = np.linspace(-4.7, 4.7, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=g, y=truth(g), mode="lines", line=dict(color=GREY, width=2, dash="dash"), name="true function"))
fig.add_trace(go.Scatter(x=g, y=phi(g) @ mle, mode="lines", line=dict(color=BLUE, width=4),
                         name=f"MLE (test RMSE {rm(mle):.2f})"))
fig.add_trace(go.Scatter(x=g, y=phi(g) @ map_, mode="lines", line=dict(color=ORANGE, width=4),
                         name=f"MAP, Gaussian prior (test RMSE {rm(map_):.2f})"))
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=12, color="black"), name="training data"))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="x"), yaxis=dict(title="y", range=[-3, 3]),
                  legend=dict(orientation="h", x=0, y=-0.2), margin=dict(l=70, r=20, t=20, b=150))
fig.write_image(HERE / "map_vs_mle.png", scale=2)
fig.write_image(HERE / "map_vs_mle.pdf")
print("MLE", rm(mle), "MAP", rm(map_), np.abs(mle).max(), np.abs(map_).max())
