"""Huber loss with a growing delta on the Note's 40 points (25% outliers, data/outlier_fit.npz) (Plotly frames).
For each delta the line is refitted by minimising the Huber cost. Small delta: the line sits with MAE's.
From delta = 6 on, every error is inside delta and the line is MSE's.
Run: python huber_delta.py -> huber_delta.gif, huber_delta_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize
from common import BLUE, ORANGE, GREEN, RED, GREY, save_gif

HERE = Path(__file__).parent
d = np.load(HERE.parent / "data" / "outlier_fit.npz")
x, y, out = d["x"], d["y"], d["is_out"]
DELTAS = [0.25, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 10, 12, 16]


def huber_fit(delta):
    def cost(w):
        e = np.abs(y - (w[0] * x + w[1]))
        return np.where(e <= delta, 0.5 * e ** 2, delta * (e - 0.5 * delta)).mean()
    return minimize(cost, d["MAE"], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-12, maxiter=5000)).x


FITS = {k: huber_fit(k) for k in DELTAS}
assert np.allclose(FITS[1], d["Huber"], atol=0.02)                       # delta = 1 reproduces the Note's Huber line
assert np.allclose(FITS[16], d["MSE"], atol=0.02)                        # a large delta gives the MSE line
lift = [np.polyval(FITS[k], 5) for k in DELTAS]
assert all(a <= b + 1e-6 for a, b in zip(lift, lift[1:]))                # the line only moves up, towards the outliers


def frame(delta):
    m, b = FITS[delta]
    xs = np.array([0, 10])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x[~out], y=y[~out], mode="markers", name="75% of points", marker=dict(color=GREY, size=10)))
    fig.add_trace(go.Scatter(x=x[out], y=y[out], mode="markers", name="25% outliers", marker=dict(color=RED, size=11, symbol="diamond")))
    for name, c in (("MSE", BLUE), ("MAE", ORANGE)):
        fig.add_trace(go.Scatter(x=xs, y=d[name][0] * xs + d[name][1], mode="lines", name=name, line=dict(color=c, width=3, dash="dash")))
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", name="Huber", line=dict(color=GREEN, width=6)))
    fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"Huber loss with δ = <b>{delta:g}</b>:  ŷ = {m:.2f}x + {b:.2f}", x=0.5),
                      xaxis=dict(title="x"), yaxis=dict(title="y", range=[0, 32]), legend=dict(x=0.02, y=0.98),
                      margin=dict(l=70, r=20, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in DELTAS], "huber_delta", [0, DELTAS.index(4), DELTAS.index(8), len(DELTAS) - 1], HERE, fps=2, hold=5)
    for k in DELTAS:
        print(k, FITS[k].round(2))
