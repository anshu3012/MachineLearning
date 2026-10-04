"""Gradient descent with two inputs on very different scales vs the same inputs standardised (Plotly).
Made-up data, fixed seed; same number of steps, largest learning rate that does not blow up for each."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
rng = np.random.default_rng(0)
n = 200
x1 = rng.normal(0, 1, n)                  # small scale
x2 = rng.normal(0, 8, n)                  # 8 times larger scale
y = 3 * x1 + 0.5 * x2 + rng.normal(0, 1, n)


def run(A, lr, steps=40, w0=(-4.0, -4.0)):
    w = np.array(w0, float); path = [w.copy()]
    for _ in range(steps):
        grad = -2 / n * A.T @ (y - A @ w)
        w = w - lr * grad; path.append(w.copy())
    return np.array(path)


A_raw = np.c_[x1, x2]
A_std = (A_raw - A_raw.mean(0)) / A_raw.std(0)
cases = [(A_raw, 0.0075, "Unscaled inputs: a long, narrow valley"), (A_std, 0.1, "Standardised inputs: round contours")]
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=[c[2] for c in cases])
for col, (A, lr, _) in enumerate(cases, start=1):
    best = np.linalg.lstsq(A, y, rcond=None)[0]
    g = np.linspace(-6, 6, 120)
    W1, W2 = np.meshgrid(best[0] + g, best[1] + g)
    Z = np.array([[np.mean((y - A @ np.array([a, b])) ** 2) for a, b in zip(r1, r2)] for r1, r2 in zip(W1, W2)])
    path = run(A, lr, w0=(best[0] - 5, best[1] + 5))
    fig.add_trace(go.Contour(x=best[0] + g, y=best[1] + g, z=np.log(Z), colorscale="Blues", reversescale=True,
                             showscale=False, ncontours=20, line=dict(width=0.5)), 1, col)
    fig.add_trace(go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines+markers", line=dict(color=ORANGE, width=2.5),
                             marker=dict(size=5, color=ORANGE)), 1, col)
    fig.add_trace(go.Scatter(x=[best[0]], y=[best[1]], mode="markers", marker=dict(size=12, color=GREEN, symbol="x")), 1, col)
    fig.update_xaxes(title="weight of input 1", row=1, col=col)
    fig.update_yaxes(title="weight of input 2", scaleanchor=f"x{'' if col == 1 else 2}", row=1, col=col)
    print(_, "distance to best after 40 steps:", round(float(np.linalg.norm(path[-1] - best)), 3))
fig.update_layout(template="simple_white", width=1050, height=500, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
fig.write_image(here / "scaling_effect.png", scale=2)
fig.write_image(here / "scaling_effect.pdf")
