"""Choosing Q: the error of three filters on one 50-step run where the real slip has variance 0.01. With Q = 0.0001
the filter trusts the commands and drifts with the slips; with Q = 1 it trusts each reading and jitters; Q = 0.01
sits between. Over 2000 runs (steps 11 to 50) the root-mean-square errors are 0.305, 0.187 and 0.353 m.
Run: python tuning.py -> tuning.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE, RED
from kfsim import kf1d

here = Path(__file__).parent


def sim(n, T=50):
    r = np.random.default_rng(n)
    xt, xs, zs = r.normal(0, 1), [], []
    for _ in range(T):
        xt += 0.5 + r.normal(0, 0.1)
        xs.append(xt)
        zs.append(xt + r.normal(0, 0.4))
    return np.array(xs), np.array(zs)


QS = [(1e-4, RED, "Q = 0.0001 (too small)"), (1e-2, BLUE, "Q = 0.01 (matches the slip)"), (1.0, GREEN, "Q = 1 (too big)")]
rmse = {}
for q, _, _ in QS:
    e = []
    for n in range(2000):
        xs, zs = sim(n)
        e.append((np.array([r["x"] for r in kf1d(z=zs, q=q)]) - xs)[10:])
    rmse[q] = np.sqrt(np.mean(np.square(e)))
print({q: round(v, 3) for q, v in rmse.items()})
xs, zs = sim(0)
t = np.arange(1, 51)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=zs - xs, mode="markers", marker=dict(color=ORANGE, size=8, symbol="x"),
                         name="reading error"))
for q, c, name in QS:
    fig.add_trace(go.Scatter(x=t, y=np.array([r["x"] for r in kf1d(z=zs, q=q)]) - xs, mode="lines",
                             line=dict(color=c, width=4), name=f"{name}: RMSE {rmse[q]:.3f} m (2000 runs)"))
fig.add_hline(y=0, line=dict(color="black", width=1))
fig.update_layout(template="simple_white", font=FONT, width=1050, height=560, margin=dict(l=90, r=30, t=110, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom", font=dict(size=17)),
                  xaxis=dict(title="step"), yaxis=dict(title="estimate minus truth (m)", range=[-1.4, 1.4]))
fig.write_image(here / "tuning.png")
