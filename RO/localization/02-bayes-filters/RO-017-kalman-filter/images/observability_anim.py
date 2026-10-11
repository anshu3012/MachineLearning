"""Observability in numbers, step by step. The variance of the position estimate over
ten steps for two filters: one reads position (H = [1, 0]), one reads only speed (H = [0, 1]). Each predict raises
the variance (a slanted line up), each update lowers it (a drop): a sawtooth. With the position sensor it ends at
0.066 m², falling after each update; with only the speed sensor the variance after each update climbs
every step, to 2.68 m².
Run: python observability_anim.py -> observability_anim.gif, observability_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED, make_gif
from kfsim import kf2d

here = Path(__file__).parent
SENSORS = [("reads position: H = [1, 0]", BLUE, kf2d()),
           ("reads speed only: H = [0, 1]", RED, kf2d(z=np.full(10, 0.5), Hm=np.array([[0.0, 1.0]])))]
pa = np.array([r["P"][0, 0] for r in SENSORS[0][2]])
pb = np.array([r["P"][0, 0] for r in SENSORS[1][2]])
assert abs(pa[-1] - 0.066) < 5e-4 and abs(pb[-1] - 2.68) < 5e-3
assert np.all(np.diff(np.r_[1.0, pb]) > 0)                 # speed sensor: the variance after each update climbs
assert np.all(np.diff(pa) < 0)                            # position sensor: it falls every step
for _, _, rows in SENSORS:                                # predict raises, update lowers, every step
    assert all(r["P_pred"][0, 0] > r["P"][0, 0] for r in rows)
    assert all(b["P_pred"][0, 0] > a["P"][0, 0] for a, b in zip(rows, rows[1:]))


def path(rows, t, stage):
    """The sawtooth up to step t: slant up to the prediction at x = t, then (after the update) drop at x = t."""
    xs, ys = [0], [1.0]
    for i in range(t):
        xs.append(i + 1)
        ys.append(rows[i]["P_pred"][0, 0])
        if i < t - 1 or stage == "update":
            xs.append(i + 1)
            ys.append(rows[i]["P"][0, 0])
    return xs, ys


def frame(t, stage):
    fig = go.Figure()
    now = []
    for name, col, rows in SENSORS:
        xs, ys = path(rows, t, stage)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=4), name=name))
        done = t if stage == "update" else t - 1          # updates finished
        fig.add_trace(go.Scatter(x=np.r_[0, np.arange(1, done + 1)], y=np.r_[1.0, [r["P"][0, 0] for r in rows[:done]]],
                                 mode="markers", marker=dict(color=col, size=12), showlegend=False))
        now.append(f"<span style='color:{col}'>{ys[-1]:.3f} m²</span>")
    if t == 10 and stage == "update":
        for v, col in ((pa[-1], BLUE), (pb[-1], RED)):
            fig.add_annotation(x=10, y=v, text=f"{v:.3f}" if v < 1 else f"{v:.2f}", showarrow=False, xanchor="left",
                               xshift=10, font=dict(size=19, color=col))
    title = ("start: variance 1 m² for both" if t == 0 else
             f"step {t}: predict, the variance grows" if stage == "predict" else
             f"step {t}: update, the reading lowers it")
    if t:
        title += f"<br><span style='font-size:19px'>now: {now[0]}   {now[1]}</span>"
    fig.update_layout(template="simple_white", font=FONT, width=950, height=600, margin=dict(l=90, r=70, t=110, b=70),
                      legend=dict(x=0.01, y=0.99, font=dict(size=18)), title=dict(x=0.5, y=0.96, text=title),
                      xaxis=dict(title="step", dtick=1, range=[-0.3, 10.6]),
                      yaxis=dict(title="variance of the position estimate (m²)", range=[0, 3.1]))
    return fig


figs, holds = [frame(0, "update")], [3]
for t in range(1, 11):
    figs += [frame(t, "predict"), frame(t, "update")]
    holds += [2, 2] if t <= 2 else [1, 1]
holds[-1] = 8
make_gif(figs, here / "observability_anim", fps=1, holds=holds, keys=[1, 2, 10, 20], cols=2, width=850)
