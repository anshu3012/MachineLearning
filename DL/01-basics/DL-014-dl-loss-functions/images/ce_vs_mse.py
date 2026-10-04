"""Cross-entropy against squared error on one probability (Plotly frames). p is the probability the network gives the
true class; it slides from 0.99 down to 0.01. Each curve carries its tangent line, and the slopes are printed:
-1/p for cross-entropy -ln p, and -2(1 - p) for the squared error (1 - p)^2. The slope is what pushes the weights.
Run: python ce_vs_mse.py -> ce_vs_mse.gif, ce_vs_mse_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, GREY, save_gif

HERE = Path(__file__).parent
ps = np.r_[0.99, np.arange(0.95, 0.04, -0.05), 0.03, 0.01]
ce, se = lambda p: -np.log(p), lambda p: (1 - p) ** 2
dce, dse = lambda p: -1 / p, lambda p: -2 * (1 - p)
assert round(ce(0.73), 3) == 0.315                                   # student 1 of the Note
assert abs(dse(0.01)) < 2 and abs(dce(0.01)) == 100                  # badly wrong: squared error pushes < 2, cross-entropy 100
grid = np.linspace(0.005, 1, 400)


def frame(p):
    fig = go.Figure()
    for f, d, col, name in ((ce, dce, RED, "cross-entropy  −ln p"), (se, dse, BLUE, "squared error  (1 − p)²")):
        fig.add_trace(go.Scatter(x=grid, y=f(grid), mode="lines", line=dict(color=col, width=4), name=name))
        t = np.array([p - 0.12, p + 0.12])
        fig.add_trace(go.Scatter(x=t, y=f(p) + d(p) * (t - p), mode="lines", line=dict(color=col, width=3, dash="dot"), showlegend=False))
        fig.add_trace(go.Scatter(x=[p], y=[f(p)], mode="markers", marker=dict(color=col, size=16), showlegend=False))
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"probability given to the true class: p = <b>{p:.2f}</b><br>"
                                      f"<span style='color:{RED}'>cross-entropy slope −{abs(dce(p)):.1f}</span>"
                                      f"   <span style='color:{BLUE}'>squared-error slope −{abs(dse(p)):.2f}</span>", x=0.5),
                      xaxis=dict(title="p, predicted probability of the true class", range=[0, 1.02]),
                      yaxis=dict(title="loss", range=[-0.2, 5]), legend=dict(x=0.55, y=0.95), margin=dict(l=80, r=20, t=120, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(p) for p in ps], "ce_vs_mse", [0, 6, 14, len(ps) - 1], HERE, fps=4, hold=10)
    for p in (0.99, 0.73, 0.25, 0.01):
        print(p, "CE", round(ce(p), 3), "slope", round(dce(p), 2), "| SE", round(se(p), 3), "slope", round(dse(p), 2))
