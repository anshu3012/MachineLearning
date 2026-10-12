"""Animation: why speed is part of the state. Two robots stand at the same place on RO-037's line, s = 2.8 m, 0.317 m
short of the closed door, and both brake at once at 0.5 m/s^2. Robot A moves at 0.3 m/s and stops at s = 2.89 m.
Robot B moves at 0.6 m/s, needs 0.36 m, and meets the door at s = 3.117 m still at 0.21 m/s. Left: the two runs in the
room. Right: the phase plane, position s across and speed v up; each robot is one point, and braking moves it down
and to the right along a curve. Run -> two_speeds.gif, two_speeds_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, PURPLE, RED, make_gif

here = Path(__file__).parent
S0 = 2.8
RUNS = {"A": (0.3, GREEN), "B": (0.6, PURPLE)}
TRUNS = {n: m.brake_run(S0, v) for n, (v, _) in RUNS.items()}
assert round(TRUNS["A"][1][-1], 2) == 2.89 and TRUNS["A"][2][-1] <= 1e-9
assert round(m.S_DOOR - S0, 3) == 0.317
v_hit = math.sqrt(0.6 ** 2 - 2 * m.A_MAX * (m.S_DOOR - S0))
assert round(v_hit, 2) == 0.21


def at(name, t):
    tt, s, v = TRUNS[name]
    i = min(int(np.searchsorted(tt, t)), len(tt) - 1)
    return s[i], v[i], i


def frame(t, final=False):
    fig = make_subplots(rows=2, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1, vertical_spacing=0.14,
                        specs=[[{}, {"rowspan": 2}], [{}, None]],
                        subplot_titles=["robot A: 0.3 m/s", "the phase plane: one point per robot",
                                        "robot B: 0.6 m/s"])
    for r, name in ((1, "A"), (2, "B")):
        v0, col = RUNS[name]
        k.room(fig, r, 1)
        x0, y0 = m.on_line(2.2)
        x1, y1 = m.on_line(m.LINE_LEN)
        k.line(fig, [x0, x1], [y0, y1], color="black", width=1.5, dash="dot", row=r, col=1)
        s, v, i = at(name, t)
        hit = s >= m.S_DOOR - 1e-9 and v > 0
        px, py = m.on_line(s)
        tx, ty = zip(*[m.on_line(u) for u in np.linspace(S0, s, 20)])
        k.line(fig, tx, ty, color=RED if hit else col, width=4, row=r, col=1)
        k.disk(fig, px, py, m.LINE_HEADING, row=r, col=1, color=RED if hit else k.FOOT)
        msg = (f"hits the door<br>at {v:.2f} m/s" if hit else f"stopped at<br>s = {s:.2f} m" if v <= 1e-9 else
               f"s = {s:.2f} m<br>v = {v:.2f} m/s")
        k.text(fig, 2.45, 3.62, msg, color=RED if hit else col, size=17, row=r, col=1, xanchor="left")
        k.room_axes(fig, r, 1, xr=(2.4, 4.3), yr=(2.85, 4.25), anchor="x" if r == 1 else "x3")
        if r == 1:
            fig.update_xaxes(title=None, row=1, col=1)
    # phase plane
    k.phase_regions(fig, 1, 2, ics=False)
    for name, (v0, col) in RUNS.items():
        tt, s, v = TRUNS[name]
        i = at(name, t)[2]
        k.line(fig, s[:i + 1], v[:i + 1], color=col, width=4, row=1, col=2)
        k.point(fig, s[i], v[i], RED if (s[i] >= m.S_DOOR - 1e-9 and v[i] > 0) else col, size=16, row=1, col=2)
        k.text(fig, S0 - 0.06, v0 + 0.03, name, color=col, size=20, row=1, col=2, xanchor="right", bg="rgba(0,0,0,0)")
    k.text(fig, (m.S_DOOR + k.S_MAX) / 2, 0.66, "door", color=k.DOOR, size=18, row=1, col=2)
    k.text(fig, 2.3, m.V_TOP + 0.03, "top speed 0.6 m/s", color="#6B6B6B", size=16, row=1, col=2)
    k.phase_axes(fig, 1, 2, xr=(2.0, k.S_MAX))
    title = ("same place, s = 2.8 m: robot A stops, robot B cannot" if final else
             f"both brake at 0.5 m/s² from s = 2.8 m, time {t:.1f} s")
    k.layout(fig, 1300, 820, title, margin=dict(l=70, r=30, t=100, b=70))
    for s_ in ("robot A: 0.3 m/s", "robot B: 0.6 m/s", "the phase plane: one point per robot"):
        fig.update_annotations(font_size=20, selector=dict(text=s_))
    return fig


times = list(np.round(np.arange(0, 0.71, 0.1), 2)) + [0.78, 0.85]
figs = [frame(t) for t in times] + [frame(times[-1], final=True)]
holds = [8] + [3] * (len(times) - 1) + [26]
make_gif(figs, here / "two_speeds", fps=5, holds=holds, keys=[0, 3, 6, len(figs) - 1], cols=2, width=1000)
