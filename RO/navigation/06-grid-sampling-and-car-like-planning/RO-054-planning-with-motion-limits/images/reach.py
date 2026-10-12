"""Animation: the reachable set growing. The robot starts at (2, 1) facing 30 degrees, driving at 0.5 m/s, and may turn
at any rate between -1 and 1 rad/s. 403 trajectories (random turn rates held for random times, plus full left, straight
and full right) are drawn up to time T, which grows from 0 to 1.5 s; together they fill the positions reachable
within T, a fan bounded by the two tightest circles of radius 0.5 m. The plan's pose, still at (2, 1) but facing
61.9 degrees, never enters it: the first time the robot faces 61.9 degrees is after 0.557 s and 0.279 m of driving,
at (2.191, 1.198). Run -> reach.gif, reach_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as k
import motionkit as m
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent
TRAILS = m.reach_trails(T=1.5, n=400, seed=1, h=0.02)
H = 0.02
th_line = m.LINE_HEADING
t_face = (th_line - m.START[2]) / m.W_MAX
x_face = m.START[0] + m.RHO * (math.sin(th_line) - math.sin(m.START[2]))
y_face = m.START[1] - m.RHO * (math.cos(th_line) - math.cos(m.START[2]))
assert round(t_face, 3) == 0.557 and round(m.V_CRUISE * t_face, 3) == 0.279
assert (round(x_face, 3), round(y_face, 3)) == (2.191, 1.198)
assert len(TRAILS) == 403


def frame(T, final=False):
    fig = go.Figure()
    n = int(round(T / H))
    xs, ys = [], []
    for tr in TRAILS[3:]:
        xs += list(tr[:n + 1, 0]) + [None]
        ys += list(tr[:n + 1, 1]) + [None]
    k.line(fig, xs, ys, color="rgba(84,162,75,0.25)", width=2)
    for tr in TRAILS[:3]:
        k.line(fig, tr[:n + 1, 0], tr[:n + 1, 1], color=GREEN, width=4)
    # the two tightest circles, dotted
    for sgn in (1, -1):
        cx = m.START[0] - sgn * m.RHO * math.sin(m.START[2])
        cy = m.START[1] + sgn * m.RHO * math.cos(m.START[2])
        a = np.linspace(0, 2 * math.pi, 120)
        k.line(fig, cx + m.RHO * np.cos(a), cy + m.RHO * np.sin(a), color="#999999", width=1.5, dash="dot")
    k.ghost(fig, m.START[0], m.START[1], th_line)
    k.text(fig, 1.55, 1.22, "plan: still at (2, 1),<br>facing 61.9°", color="#777777", size=17)
    k.disk(fig, *m.START, color="#222222", width=2)
    if T >= t_face:
        k.arrow(fig, x_face, y_face, th_line, length=0.3, color=RED, width=4)
        k.point(fig, x_face, y_face, RED, size=11)
        k.text(fig, x_face - 0.1, y_face + 0.42, f"first faces 61.9°<br>after {t_face:.3f} s,<br>0.279 m from (2, 1)", color=RED, size=16,
               xanchor="right", bg="rgba(255,255,255,0.85)")
    k.text(fig, 2.9, 0.68, f"reachable within T = {T:.1f} s", color=GREEN, size=19)
    k.room_axes(fig, xr=(1.25, 3.3), yr=(0.55, 2.15))
    title = ("the plan's pose is never reached: the moving robot cannot turn on the spot" if final else
             f"0.5 m/s, turning at any rate up to 1 rad/s: where can the robot be by T = {T:.1f} s?")
    return k.layout(fig, 1000, 820, title, margin=dict(l=70, r=30, t=70, b=60), size=20)


times = [round(t, 1) for t in np.arange(0, 1.51, 0.1)]
figs = [frame(t) for t in times] + [frame(1.5, final=True)]
holds = [6] + [3] * (len(times) - 1) + [24]
make_gif(figs, here / "reach", fps=5, holds=holds, keys=[0, 5, 10, len(figs) - 1], cols=2, width=900)
