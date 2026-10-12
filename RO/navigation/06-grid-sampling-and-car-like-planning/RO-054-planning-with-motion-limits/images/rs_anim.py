"""Animation: the shortest way to move 0.5 m sideways (RO-001 6.2's move, from (2, 1) facing 30 degrees to
(1.75, 1.433) facing 30 degrees) for a vehicle whose tightest circle is 0.5 m. Left, forward only (Dubins): LSL,
a quarter turn left, 0.5 m straight and three quarters of a turn left, 3.642 m. Right, with reverse (Reeds-Shepp):
R+ L- R- L+, right forward, left in reverse, right in reverse, left forward, 1.318 m with 2 reversals (red dots).
Both robots move at 0.5 m/s, one frame per 0.25 s: the Reeds-Shepp robot arrives after 2.64 s of driving, the Dubins
robot after 7.28 s. Run -> rs_anim.gif, rs_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

import carpaths as cp
import drawkit as k
import motionkit as m
from gifkit import GREEN, PURPLE, RED, make_gif

here = Path(__file__).parent
S = m.START
G = (S[0] - 0.5 * math.sin(S[2]), S[1] + 0.5 * math.cos(S[2]), S[2])
RS = cp.reeds_shepp(S, G, m.RHO)
_, DB = cp.dubins(S, G, m.RHO)
assert round(G[0], 3) == 1.75 and round(G[1], 3) == 1.433
assert cp.word(RS) == "R+ L- R- L+" and round(cp.length(RS), 3) == 1.318 and cp.cusps(RS) == 2
assert [k_ for k_, _ in DB] == ["L", "S", "L"] and round(cp.length(DB), 3) == 3.642
assert round(cp.length(RS) / m.V_CRUISE, 2) == 2.64 and round(cp.length(DB) / m.V_CRUISE, 2) == 7.28


def pose_at(path, dist):
    """Pose after driving `dist` metres along the path (|segment lengths| add up), and the cusp points passed."""
    p = S
    left = dist
    cusps = []
    for i, (kind, s) in enumerate(path):
        if left <= abs(s):
            return cp.step(p, kind, math.copysign(left, s), m.RHO), cusps
        p = cp.step(p, kind, s, m.RHO)
        left -= abs(s)
        if i + 1 < len(path) and (path[i + 1][1] > 0) != (s > 0):
            cusps.append(p)
    return p, cusps


def trail(path, dist, n=80):
    return np.array([pose_at(path, d)[0] for d in np.linspace(0, dist, n)])


def frame(t, final=False):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                        subplot_titles=["forward only (Dubins): LSL, 3.642 m",
                                        "with reverse (Reeds-Shepp): R+ L− R− L+, 1.318 m"])
    for col, path, colour in ((1, DB, PURPLE), (2, RS, GREEN)):
        d = min(t * m.V_CRUISE, cp.length(path))
        k.disk(fig, *G, row=1, col=col, color="#AAAAAA", width=2, body=False)
        k.arrow(fig, G[0], G[1], G[2], length=0.3, color="#AAAAAA", width=3, row=1, col=col)
        k.text(fig, G[0] - 0.3, G[1] + 0.3, "goal: 0.5 m to the left", color="#777777", size=16, row=1, col=col)
        k.point(fig, S[0], S[1], "black", size=9, row=1, col=col)
        k.text(fig, S[0] + 0.05, S[1] - 0.12, "start", size=16, row=1, col=col, xanchor="left", bg="rgba(0,0,0,0)")
        tr = trail(path, d)
        k.line(fig, tr[:, 0], tr[:, 1], color=colour, width=5, row=1, col=col)
        p, cus = pose_at(path, d)
        for c in cus:
            k.point(fig, c[0], c[1], RED, size=13, row=1, col=col)
        k.disk(fig, *p, row=1, col=col)
        done = d >= cp.length(path) - 1e-9
        k.text(fig, 1.15, 0.72, (f"arrived after {cp.length(path) / m.V_CRUISE:.2f} s" if done else
                                 f"driven {d:.2f} m"), color=colour, size=18, row=1, col=col, xanchor="left")
        k.room_axes(fig, 1, col, xr=(0.85, 2.75), yr=(0.6, 2.55), anchor="x" if col == 1 else "x2")
    title = ("same start, same goal: reversing makes the path 2.8 times shorter, with two stops" if final else
             f"both at 0.5 m/s, time {t:.2f} s; red dots: where the robot reverses")
    k.layout(fig, 1300, 700, title, margin=dict(l=70, r=30, t=100, b=60), size=21)
    for s in ("forward only (Dubins): LSL, 3.642 m", "with reverse (Reeds-Shepp): R+ L− R− L+, 1.318 m"):
        fig.update_annotations(font_size=20, selector=dict(text=s))
    return fig


assert round(cp.length(DB) / cp.length(RS), 1) == 2.8
times = list(np.arange(0, 7.26, 0.25)) + [7.3]
figs = [frame(t) for t in times] + [frame(times[-1], final=True)]
holds = [6] + [2] * (len(times) - 1) + [26]
make_gif(figs, here / "rs_anim", fps=5, holds=holds, keys=[0, 4, 11, len(figs) - 1], cols=2, width=1000)
