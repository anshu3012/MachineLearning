"""Animation: the system simulator building the three motion primitives. From (2, 1) facing 30 degrees at 0.5 m/s,
each primitive holds one turn rate (left +1, straight 0, right -1 rad/s) for 0.75 s. The simulator takes Euler steps
of 0.01 s (RO-001 5.3); one frame shows 5 more steps (0.05 s), so the dots appear 0.025 m apart. Last frame: the three
end poses, (2.230, 1.285) at 73 degrees, (2.325, 1.187) at 30 degrees and (2.362, 1.056) at -13 degrees.
Run -> simulate_anim.gif, simulate_anim_frames.png"""
import math
from pathlib import Path

import plotly.graph_objects as go

import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, PURPLE, make_gif

here = Path(__file__).parent
COL = {"left": BLUE, "straight": GREEN, "right": PURPLE}
TR = {name: m.simulate(m.START, m.V_CRUISE, om, m.DT_PRIM) for name, om in m.PRIMS.items()}
ENDS = {name: tr[-1] for name, tr in TR.items()}
assert [round(v, 3) for v in ENDS["left"][:2]] == [2.23, 1.285] and round(math.degrees(ENDS["left"][2])) == 73
assert [round(v, 3) for v in ENDS["straight"][:2]] == [2.325, 1.187]
assert [round(v, 3) for v in ENDS["right"][:2]] == [2.362, 1.056] and round(math.degrees(ENDS["right"][2])) == -13
assert len(TR["left"]) == 76


def frame(n, final=False):
    fig = go.Figure()
    k.disk(fig, *m.START, color="#222222", width=2, body=False)
    k.point(fig, m.START[0], m.START[1], "#222222", size=10)
    for name, tr in TR.items():
        k.line(fig, tr[:n + 1, 0], tr[:n + 1, 1], color=COL[name], width=3)
        idx = list(range(0, n + 1, 5))
        k.line(fig, tr[idx, 0], tr[idx, 1], color=COL[name], mode="markers", width=1)
        fig.data[-1].marker = dict(size=8, color=COL[name])
        x, y, th = tr[n]
        k.arrow(fig, x, y, th, length=0.07, color=COL[name], width=3, size=11)
        if final:
            off = {"left": (-0.02, 0.1, "right"), "straight": (0.06, 0.03, "left"), "right": (0.05, -0.05, "left")}[name]
            k.text(fig, x + off[0], y + off[1], f"{name}: ({x:.3f}, {y:.3f}), {math.degrees(th):.0f}°",
                   color=COL[name], size=17, xanchor=off[2], bg="rgba(255,255,255,0.85)")
    k.room_axes(fig, xr=(1.72, 2.72), yr=(0.72, 1.42))
    fig.update_xaxes(dtick=0.1)
    fig.update_yaxes(dtick=0.1)
    t = n * m.H_STEP
    title = ("three primitives, 0.75 s each: 75 Euler steps of 0.01 s" if final else
             f"t = {t:.2f} s: {n} Euler steps of 0.01 s from (2, 1) facing 30°, at 0.5 m/s")
    return k.layout(fig, 1000, 720, title, margin=dict(l=80, r=30, t=70, b=60), size=20)


steps = list(range(0, 76, 5))
figs = [frame(n) for n in steps] + [frame(75, final=True)]
holds = [6] + [2] * (len(steps) - 1) + [26]
make_gif(figs, here / "simulate_anim", fps=5, holds=holds, keys=[0, 5, 10, len(figs) - 1], cols=2, width=900)
