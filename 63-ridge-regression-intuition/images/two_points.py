"""Two training points: the least-squares line goes through both (loss 0, but steep); adding lambda*m^2 to the loss
prefers a flatter line that also fits the test points better (Plotly). Lambda = 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
xtr, ytr = np.array([1.0, 3.0]), np.array([2.0, 5.0])
rng = np.random.default_rng(3)
xte = rng.uniform(0, 4, 8); yte = 0.9 * xte + 1.7 + rng.normal(0, 0.5, 8)   # new data from a flatter pattern
lam = 1.0
def loss(m, b): return float(np.sum((ytr - m * xtr - b) ** 2)), lam * m ** 2
m1, b1 = 1.5, 0.5                            # through both points
m2 = 0.9; b2 = float(np.mean(ytr - m2 * xtr))  # best intercept for slope 0.9
xs = np.array([0, 4])
fig = go.Figure()
fig.add_trace(go.Scatter(x=xte, y=yte, mode="markers", name="test points", marker=dict(size=9, color="#BBBBBB")))
fig.add_trace(go.Scatter(x=xtr, y=ytr, mode="markers", name="training points", marker=dict(size=14, color="#4C78A8")))
for m, b, colour, name in ((m1, b1, "#E45756", "least squares"), (m2, b2, "#54A24B", "ridge-style")):
    sse, pen = loss(m, b)
    mse_te = float(np.mean((yte - m * xte - b) ** 2))
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=colour, width=4),
                             name=f"{name}: m = {m}, errors {sse:.2f} + λm² {pen:.2f} = {sse + pen:.2f}; test MSE {mse_te:.2f}"))
    print(name, m, round(b, 2), round(sse, 2), round(pen, 2), round(mse_te, 3))
fig.update_layout(template="simple_white", width=950, height=500, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=60, r=20, t=50, b=60),
                  title=dict(text="Two training points: a steep exact fit vs a flatter line (λ = 1)", x=0.5),
                  xaxis=dict(title="x", range=[0, 4]), yaxis=dict(title="y", range=[0, 7.5]))
fig.write_image(here / "two_points.png", scale=2)
fig.write_image(here / "two_points.pdf")
