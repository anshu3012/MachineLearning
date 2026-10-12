"""Refine once: two drives from rest at (2.0, 1.0) facing 30 degrees to rest at the door pose (3.6, 3.5) facing
90 degrees, past the table, within the robot's limits, one frame per 0.2 s. Grey: the A* route (dashed) driven by
stopping and turning at each of its corners: 11.81 s. Blue: the least-time trajectory that collocation finds once,
starting from that route (its controls replayed in small simulation steps): 6.18 s. Each robot is a disk of radius
0.25 m with a line for its heading; the dotted band round the table is where the disk's centre may not go.
Run -> refine_once.gif, refine_once_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import trajkit as tk
from gifkit import BLUE, FONT, GREY, make_gif

here = Path(__file__).parent
S = tk.solutions()
sol = S["time"]
T = sol["T"]
ts, xs = tk.drive_controls(sol["X"], sol["U"], T)
st = tk.stop_and_turn()
assert round(st["T"], 2) == 11.81 and round(T, 2) == 6.18
assert np.hypot(*(xs[-1, :2] - tk.GOAL[:2])) < 0.01 and abs(xs[-1, 2] - tk.GOAL[2]) < 0.02
assert xs[:, 3].max() < 0.6025                    # the replayed speed stays at the limit, 0.60 m/s


def blue_at(t):
    i = min(np.searchsorted(ts, t), len(ts) - 1)
    return xs[i]


def frame(t):
    fig = go.Figure()
    rd.room(fig)
    g = np.array([st["sample"](u) for u in np.linspace(0, min(t, st["T"]), 200)])
    b = xs[ts <= t + 1e-9]
    fig.add_trace(go.Scatter(x=tk.ROUTE_PTS[:, 0], y=tk.ROUTE_PTS[:, 1], mode="lines",
                             line=dict(color="#BBBBBB", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=g[:, 0], y=g[:, 1], mode="lines", line=dict(color=GREY, width=4)))
    fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="lines", line=dict(color=BLUE, width=5)))
    rd.robot(fig, tk.GOAL[0], tk.GOAL[1], tk.GOAL[2], "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    gx = st["sample"](min(t, st["T"]))
    rd.robot(fig, gx[0], gx[1], gx[2], GREY)
    bx = blue_at(min(t, T))
    rd.robot(fig, bx[0], bx[1], bx[2], BLUE)
    lines = [f"<b>t = {t:.2f} s</b>",
             f"<span style='color:{BLUE}'>refined once: " + (f"arrived at {T:.2f} s" if t >= T - 1e-9 else
                                                            f"{bx[3]:.2f} m/s") + "</span>",
             f"<span style='color:{GREY}'>stop and turn: " + (f"arrived at {st['T']:.2f} s" if t >= st["T"] - 1e-9 else
                                                                 f"{gx[3]:.2f} m/s") + "</span>"]
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=21), bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=2.0, y=0.62, text="start", showarrow=False, font=dict(size=18, color="#555555"))
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


times = sorted(set(np.round(np.arange(0, 11.8 + 1e-9, 0.2), 1)) | {T, st["T"]})
figs = [frame(t) for t in times]
holds = [4] + [1] * (len(figs) - 2) + [14]
k_blue = times.index(T)
make_gif(figs, here / "refine_once", fps=5, holds=holds, keys=[0, 15, k_blue, len(figs) - 1], cols=2,
         width=560)
