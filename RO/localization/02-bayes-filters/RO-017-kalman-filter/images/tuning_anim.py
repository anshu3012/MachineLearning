"""Choosing Q, step by step: three filters run through the same 50-step run
(seed 0, real slip variance 0.01), one step per frame. Each legend entry shows the filter's gain K at that step:
Q = 0.0001 starts like the others, is at 0.10 by step 10 and keeps falling, so it trusts the commands and lags;
Q = 1 settles at 0.88 and copies every jump of the readings; Q = 0.01 settles at 0.22 and stays closest to zero.
RMSE over 2000 runs (steps 11 to 50): 0.305, 0.187 and 0.353 m; the readings alone 0.399 m.
Run: python tuning_anim.py -> tuning_anim.gif, tuning_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif
from kfsim import kf1d

here = Path(__file__).parent
T = 50


def sim(n):
    r = np.random.default_rng(n)
    xt, xs, zs = r.normal(0, 1), [], []
    for _ in range(T):
        xt += 0.5 + r.normal(0, 0.1)
        xs.append(xt)
        zs.append(xt + r.normal(0, 0.4))
    return np.array(xs), np.array(zs)


QS = [(1e-4, RED, "Q = 0.0001 (too small)"), (1e-2, BLUE, "Q = 0.01 (matches the slip)"), (1.0, GREEN, "Q = 1 (too big)")]
err = {q: [] for q, _, _ in QS}
zerr = []
for n in range(2000):
    xs, zs = sim(n)
    zerr.append((zs - xs)[10:])
    for q, _, _ in QS:
        err[q].append((np.array([r["x"] for r in kf1d(z=zs, q=q)]) - xs)[10:])
rmse = {q: np.sqrt(np.mean(np.square(e))) for q, e in err.items()}
assert np.allclose([rmse[1e-4], rmse[1e-2], rmse[1.0], np.sqrt(np.mean(np.square(zerr)))],
                   [0.305, 0.187, 0.353, 0.399], atol=5e-4)
xs, zs = sim(0)
runs = {q: kf1d(z=zs, q=q) for q, _, _ in QS}
E = {q: np.array([r["x"] for r in rows]) - xs for q, rows in runs.items()}
G = {q: np.array([r["K"] for r in rows]) for q, rows in runs.items()}
assert abs(G[1e-4][9] - 0.10) < 5e-3 and np.all(np.diff(G[1e-4]) < 0)        # 0.10 at step 10, falling
assert abs(G[1e-2][-1] - 0.22) < 5e-3 and abs(G[1.0][-1] - 0.88) < 5e-3


def frame(t):
    s = np.arange(1, t + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s, y=(zs - xs)[:t], mode="markers", marker=dict(color=ORANGE, size=9, symbol="x"),
                             name="reading error"))
    for q, c, name in QS:
        fig.add_trace(go.Scatter(x=s, y=E[q][:t], mode="lines", line=dict(color=c, width=4),
                                 name=f"{name}: gain K = {G[q][t - 1]:.2f}, RMSE {rmse[q]:.3f} m (2000 runs)"))
        fig.add_trace(go.Scatter(x=[t], y=[E[q][t - 1]], mode="markers", marker=dict(color=c, size=14),
                                 showlegend=False))
    fig.add_hline(y=0, line=dict(color="black", width=1))
    fig.update_layout(template="simple_white", font=FONT, width=1050, height=640, margin=dict(l=90, r=30, t=170, b=70),
                      title=dict(x=0.5, y=0.97, text=f"step {t} of {T}"),
                      legend=dict(x=0.5, xanchor="center", y=1.02, yanchor="bottom", font=dict(size=17)),
                      xaxis=dict(title="step", range=[0, T + 1]),
                      yaxis=dict(title="estimate minus truth (m)", range=[-1.4, 1.4]))
    return fig


figs = [frame(t) for t in range(1, T + 1)]
make_gif(figs, here / "tuning_anim", fps=6, holds=[6] + [2] * (T - 2) + [16], keys=[9, 29, 49], cols=1, width=850)
