"""Why log odds: 40 readings of 'open', then one 'closed', run two ways (the notebook's run). Left: the probability
that the door is open, updated with Bayes' theorem in ordinary floating-point numbers, with every digit the computer
stores; from reading 34 on it is exactly 1.0 (orange), and the 'closed' reading leaves it at 1.0. Right: the log odds,
which climb by ln 3 = 1.0986 per reading to 43.94 and drop by ln 0.5 = -0.69 to 43.25 at the 'closed' reading.
Run: python round_off.py -> round_off.gif, round_off_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
K = 40
ps = [0.5]
for _ in range(K):                                # the notebook's update, in ordinary probabilities
    ps.append(0.6 * ps[-1] / (0.6 * ps[-1] + 0.2 * (1 - ps[-1])))
p_closed = 0.4 * ps[-1] / (0.4 * ps[-1] + 0.8 * (1 - ps[-1]))
ls = [k * np.log(3) for k in range(K + 1)]
l_closed = ls[-1] + np.log(0.5)
FREEZE = next(k for k, p in enumerate(ps) if p == 1.0)
assert FREEZE == 34 and all(p == 1.0 for p in ps[FREEZE:]) and p_closed == 1.0
assert round(ls[-1], 2) == 43.94 and round(l_closed, 2) == 43.25 and round(43.94 - 0.69, 2) == 43.25
assert round(np.log(3), 4) == 1.0986 and round(np.log(0.5), 2) == -0.69
X = list(range(K + 2))                            # x = K + 1 is the 'closed' reading


def frame(k, closed=False):
    """k: readings of 'open' so far; closed: the 'closed' reading has come after the 40th."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                        subplot_titles=["p(open) in ordinary probabilities", "log odds l"])
    n = k + 1
    xs, pv, lv = X[:n], ps[:n], ls[:n]
    if closed:
        xs, pv, lv = X, ps + [p_closed], ls + [l_closed]
    colors = [ORANGE if p == 1.0 else BLUE for p in pv]
    fig.add_scatter(x=xs, y=pv, mode="lines+markers", line=dict(color=GREY, width=1.5),
                    marker=dict(size=9, color=colors), row=1, col=1)
    fig.add_scatter(x=xs[:k + 1], y=lv[:k + 1], mode="lines+markers", line=dict(color=BLUE, width=2.5),
                    marker=dict(size=7, color=BLUE), row=1, col=2)
    if closed:                                    # the 'closed' reading: red on both sides
        fig.add_scatter(x=[K + 1], y=[p_closed], mode="markers", marker=dict(size=15, color=ORANGE,
                        line=dict(color=RED, width=3)), row=1, col=1)
        fig.add_scatter(x=[K, K + 1], y=[ls[-1], l_closed], mode="lines", line=dict(color=RED, width=4), row=1, col=2)
        fig.add_scatter(x=[K + 1], y=[l_closed], mode="markers", marker=dict(size=11, color=RED), row=1, col=2)
    p_now = p_closed if closed else ps[k]
    lines = [(f"after {k} reading{'' if k == 1 else 's'} of 'open'" if not closed else "then one reading of 'closed'", "black", 21),
             (f"stored: {p_now!r}", ORANGE if p_now == 1.0 else BLUE, 24)]
    if closed:
        lines += [("0.4 × 1.0 / (0.4 × 1.0 + 0.8 × 0.0) = 1.0", RED, 18), ("the reading changes nothing", RED, 18)]
    elif p_now == 1.0:
        lines += [(f"exactly 1.0, from reading {FREEZE} on", ORANGE, 18)]
    elif k:
        lines += [("every digit the computer keeps", GREY, 18)]
    for i, (s, c, size) in enumerate(lines):
        fig.add_annotation(x=7, y=0.85 - 0.075 * i, text=s, showarrow=False, xanchor="left",
                           font=dict(size=size, color=c), row=1, col=1)
    rl = [(f"l = {k} × ln 3 = {ls[k]:.2f}", BLUE, 21), ("each 'open' adds ln 3 = 1.0986", GREY, 18)]
    if closed:
        rl = [(f"l = 40 × ln 3 = {ls[-1]:.2f}", BLUE, 21), (f"43.94 − 0.69 = {l_closed:.2f}", RED, 21),
              ("the reading still counts", RED, 18)]
    for i, (s, c, size) in enumerate(rl):
        fig.add_annotation(x=1, y=47 - 4.5 * i, text=s, showarrow=False, xanchor="left", font=dict(size=size, color=c),
                           row=1, col=2)
    ticks = dict(tickvals=[0, 10, 20, 30, K, K + 1], ticktext=["0", "10", "20", "30", "40", "<br>closed"],
                 range=[-1, K + 2.5], tickangle=0, title="readings")
    fig.update_xaxes(**ticks, row=1, col=1)
    fig.update_xaxes(**ticks, row=1, col=2)
    fig.update_yaxes(title="p(open)", range=[0.45, 1.05], dtick=0.1, row=1, col=1)
    fig.update_yaxes(title="log odds l", range=[-2, 50], dtick=10, row=1, col=2)
    fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=70, b=90))
    fig.update_annotations(selector=dict(xref="paper"), font_size=21)
    return fig


figs = [frame(k) for k in range(K + 1)] + [frame(K, closed=True)]
holds = [5] + [1] * (K - 1) + [3]
holds[1] = holds[2] = 3                            # the first readings slowly
holds[FREEZE - 1], holds[FREEZE] = 5, 10           # the last stored doubt, then exactly 1.0
holds += [26]
make_gif(figs, here / "round_off", fps=5, holds=holds, keys=[2, FREEZE - 1, FREEZE, K + 1], cols=1, width=950)
