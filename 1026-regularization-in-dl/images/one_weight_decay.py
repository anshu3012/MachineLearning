"""Weight decay on one weight, from the update rule w <- (1 - eta*lam) w - eta dL/dw (section 6).
Left: the penalty alone (no data gradient): w = 2 * 0.95^t shrinks towards 0.
Right: penalty plus a data loss L = (w - 2)^2 / 2 that pulls w to 2: without the penalty w reaches 2, with it w
settles at 2 / (1 + lam) = 1.33. eta = 0.1, lam = 0.5 (large, so the decay shows in 60 steps).
Plotly frames: curves change over the update steps. Run: python one_weight_decay.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY
from frames import save

ETA, LAM, T = 0.1, 0.5, 60
FONT = dict(family="Latin Modern Roman", size=22)
alone = [2.0]
plain, decayed = [0.2], [0.2]
for _ in range(T):
    alone.append((1 - ETA * LAM) * alone[-1])
    plain.append(plain[-1] - ETA * (plain[-1] - 2))
    decayed.append((1 - ETA * LAM) * decayed[-1] - ETA * (decayed[-1] - 2))
assert abs(alone[1] - 1.9) < 1e-9 and abs(decayed[-1] - 2 / (1 + LAM)) < 0.01 and abs(plain[-1] - 2) < 0.01


def frame(t):
    s = np.arange(t + 1)
    fig = make_subplots(1, 2, subplot_titles=("penalty only: w × 0.95 each step", "penalty + data pulling w to 2"),
                        horizontal_spacing=0.12)
    fig.add_trace(go.Scatter(x=s, y=alone[:t + 1], mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[t], y=[alone[t]], mode="markers+text", marker=dict(color=ORANGE, size=14),
                             text=[f"{alone[t]:.2f}"], textposition="top right"), 1, 1)
    for w, c, lab in ((plain, BLUE, "no penalty"), (decayed, ORANGE, "L2")):
        fig.add_trace(go.Scatter(x=s, y=w[:t + 1], mode="lines", line=dict(color=c, width=4)), 1, 2)
        fig.add_trace(go.Scatter(x=[t], y=[w[t]], mode="markers+text", marker=dict(color=c, size=14),
                                 text=[f"{lab}: {w[t]:.2f}"], textposition="bottom right" if c == ORANGE else "top right"),
                      1, 2)
    fig.add_hline(y=2, line=dict(color=GREY, dash="dot", width=1.5), row=1, col=2)
    fig.add_hline(y=2 / (1 + LAM), line=dict(color=ORANGE, dash="dot", width=1.5), row=1, col=2)
    fig.update_xaxes(title="update step", range=[0, T + 48])
    fig.update_yaxes(title="weight w", range=[0, 2.4], col=1)
    fig.update_yaxes(range=[0, 2.4], col=2)
    fig.update_annotations(font=dict(size=22))
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"update step {t}", x=0.5, y=0.98), margin=dict(l=80, r=20, t=90, b=70))
    return fig


if __name__ == "__main__":
    steps = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 26, 30, 35, 40, 45, 50, 55, 60]
    figs = [frame(t) for t in steps]
    seq = [0] * 4 + list(range(len(steps))) + [len(steps) - 1] * 10
    save("one_weight_decay", figs, seq, [0, 5, 12, len(steps) - 1], Path(__file__).parent, fps=5)
