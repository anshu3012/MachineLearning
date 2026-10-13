"""Car-like set-up: RO-055's car (wheelbase 2.5 m, tightest circle 5 m) turns round, from (2, 0) facing 0 degrees to
(-2, 0) facing 180 degrees, on an empty floor (Roesmann et al. 2017, Table I, at our car's radius), with our Python
version of TEB's algorithm. Grey dashed: the shortest Reeds-Shepp path, 15.708 m. Orange: the band, one frame per
optimizeTEB call (4 passes of 5 steps); red dots: where it changes direction. Test A: the paper's start, 5 poses on
the straight line, no acceleration limit. Test B: the band starts from the Reeds-Shepp path (a car's global planner
gives such a path) with an acceleration limit of 0.5 m/s^2; the car is drawn at its start, its two reversals and its
goal. Run -> car_anim.gif, car_anim_frames.png"""
import math
from pathlib import Path

import carpaths as cp
import numpy as np
import plotly.graph_objects as go
import tebkit as tk
from gifkit import FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
C = tk.car_results()
RS = np.array(cp.sample(tuple(tk.CAR_START), cp.reeds_shepp(tuple(tk.CAR_START), tuple(tk.CAR_GOAL), 5.0), 5.0))
sA, sB = tk.band_shape(C["A"][-1]), tk.band_shape(C["B"][-1])
assert round(sA["length"], 3) == 15.687 and sA["reversals"] == 16 and round(sA["r_min"], 2) == 4.99
assert round(sB["length"], 2) == 15.68 and sB["reversals"] == 2 and round(sB["T"], 1) == 20.5
L_CAR, W_CAR, REAR = 4.0, 1.8, 0.75


def cusps(P):
    d = np.hypot(*np.diff(P[:, :2], axis=0).T)
    s = np.sign(np.diff(P[:, 0]) * np.cos(P[:-1, 2]) + np.diff(P[:, 1]) * np.sin(P[:-1, 2]))
    k = [i for i in range(1, len(s)) if d[i] > 1e-3 and d[i - 1] > 1e-3 and s[i] * s[i - 1] < 0]
    return P[k]


def car(fig, p, col):
    c, s = math.cos(p[2]), math.sin(p[2])
    pts = [(-REAR, -W_CAR / 2), (L_CAR - REAR, -W_CAR / 2), (L_CAR - REAR, W_CAR / 2), (-REAR, W_CAR / 2), (-REAR, -W_CAR / 2)]
    fig.add_trace(go.Scatter(x=[p[0] + c * a - s * b for a, b in pts], y=[p[1] + s * a + c * b for a, b in pts],
                             mode="lines", line=dict(color=col, width=2), fill="toself", fillcolor="rgba(0,0,0,0.04)"))


def frame(b, title, k, total, show_cars=False):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=RS[:, 0], y=RS[:, 1], mode="lines", line=dict(color=GREY, width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=b.P[:, 0], y=b.P[:, 1], mode="lines+markers", line=dict(color=ORANGE, width=3),
                             marker=dict(size=5, color=ORANGE)))
    cu = cusps(b.P)
    if len(cu):
        fig.add_trace(go.Scatter(x=cu[:, 0], y=cu[:, 1], mode="markers", marker=dict(size=12, color=RED)))
    car(fig, tk.CAR_START, "#4C78A8")
    car(fig, tk.CAR_GOAL, "#999999")
    if show_cars:
        for p in cu:
            car(fig, p, RED)
    s = tk.band_shape(b)
    lines = [f"<b>{title}</b>", f"optimizeTEB call {k} of {total}",
             f"length {s['length']:.2f} m (Reeds-Shepp 15.71 m)", f"{s['reversals']} reversal{'' if s['reversals'] == 1 else 's'}; time {s['T']:.1f} s",
             f"tightest turn: radius {s['r_min']:.2f} m (limit 5 m)"]
    fig.add_annotation(x=-5.9, y=-1.35, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.92)")
    fig.update_xaxes(range=[-6, 8.8], visible=False)
    fig.update_yaxes(range=[-5.6, 3.0], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", font=FONT, width=960, height=600, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ext = np.vstack([b.P[:, :2] for b in C["A"] + C["B"]] + [RS[:, :2]])
assert ext[:, 0].min() > -6 and ext[:, 0].max() < 8.8 and ext[:, 1].min() > -5.6 and ext[:, 1].max() < 3.0, ext.min(0)
nA, nB = len(C["A"]) - 1, len(C["B"]) - 1
figs = [frame(b, "A: straight start, no acceleration limit", k, nA) for k, b in enumerate(C["A"])]
ksB = [0, 1, 5, 10, nB]
figs += [frame(C["B"][k], "B: from the planner's path, 0.5 m/s²", k, nB, show_cars=(k == nB)) for k in ksB]
holds = [4] + [1] * (nA - 1) + [8] + [3, 2, 2, 2, 14]
make_gif(figs, here / "car_anim", fps=3, holds=holds, keys=[0, 2, 8, nA, nA + 1, len(figs) - 1], cols=2, width=640)
print("A:", {k: round(v, 3) for k, v in sA.items()}, "B:", {k: round(v, 3) for k, v in sB.items()})
