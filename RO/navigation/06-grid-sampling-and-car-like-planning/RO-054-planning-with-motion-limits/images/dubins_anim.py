"""Animation: building the Dubins path from the start, (2, 1) facing 30 degrees, to the pose in front of the door,
(3.6, 3.5) facing 90 degrees, for the robot at 0.5 m/s, whose tightest circle has radius 0.5 m. First the four
circles of radius 0.5 m that touch the two poses (left and right of each). Then each word: LSL 2.992 m, RSR 9.227 m,
LSR 6.107 m, RSL 6.119 m; LRL and RLR are impossible because the matching circles are 2.469 m and 3.468 m apart,
more than 4 x 0.5 = 2 m. The shortest, LSL, is drawn thick. Last frame: the room's obstacles grown by 0.25 m (orange)
are added; LSL passes through the grown table, the disk overlapping the table by up to 0.142 m, because Dubins paths
ignore obstacles. Run -> dubins_anim.gif, dubins_anim_frames.png"""
import math
from pathlib import Path

import numpy as np

import carpaths as cp
import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, ORANGE, PURPLE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
S, G, RHO = m.START, m.DOOR_POSE, m.RHO
WORDS = cp.dubins_words(S, G, RHO)
LEN = {w: cp.length(p) for w, p in WORDS.items()}
assert {w: round(v, 3) for w, v in LEN.items()} == {"LSL": 2.992, "RSR": 9.227, "LSR": 6.107, "RSL": 6.119}
C0, C1 = cp.circles(S, RHO), cp.circles(G, RHO)
dLL, dRR = math.dist(C0["L"], C1["L"]), math.dist(C0["R"], C1["R"])
assert round(dLL, 3) == 2.469 and round(dRR, 3) == 3.468
BEST = min(LEN, key=LEN.get)
PTS = cp.sample(S, WORDS[BEST], RHO, ds=0.01)
CLR = [m.clearance(x, y) for x, y, _ in PTS]
i_worst = int(np.argmin(CLR))
assert BEST == "LSL" and round(-min(CLR), 3) == 0.142
COL = {"LSL": GREEN, "RSR": PURPLE, "LSR": BLUE, "RSL": ORANGE}
ORDER = ["LSL", "RSR", "LSR", "RSL"]


def circle(c, n=100):
    a = np.linspace(0, 2 * math.pi, n)
    return c[0] + RHO * np.cos(a), c[1] + RHO * np.sin(a)


def frame(stage, final=False):
    fig = make_subplots(rows=1, cols=1)
    k.room(fig, grown=final)
    for p, lab in ((S, "start"), (G, "goal")):
        k.disk(fig, *p, color="#222222", width=2, body=False)
        k.arrow(fig, p[0], p[1], p[2], length=0.4, color="black", width=4, size=14)
    k.text(fig, S[0] - 0.75, S[1] - 0.12, "start: (2, 1), 30°", size=17, xanchor="right", bg="rgba(255,255,255,0.9)")
    k.text(fig, G[0] + 0.62, G[1] - 0.05, "goal: (3.6, 3.5), 90°", size=17, xanchor="left")
    if stage >= 1:
        for c, nm in ((C0["L"], "L"), (C0["R"], "R"), (C1["L"], "L"), (C1["R"], "R")):
            cx, cy = circle(c)
            k.line(fig, cx, cy, color="#888888", width=1.5, dash="dot")
            k.point(fig, c[0], c[1], "#888888", size=7)
    shown = ORDER[:max(0, stage - 1)] if not final else ORDER
    current = ORDER[stage - 2] if 2 <= stage <= 5 else BEST
    for w in shown:
        pts = cp.sample(S, WORDS[w], RHO, ds=0.02)
        thick = w == current
        k.line(fig, pts[:, 0], pts[:, 1], color=COL[w], width=6 if thick else 2, opacity=1.0 if thick else 0.45)
    spots = [(3.0, 0.66), (4.65, 0.66), (3.0, 0.4), (4.65, 0.4)]
    for (x, y), w in zip(spots, shown):
        k.text(fig, x, y, f"{w}: {LEN[w]:.3f} m", color=COL[w], size=19, xanchor="left", bg="rgba(255,255,255,0.9)")
    if stage >= 6 or final:
        k.text(fig, 3.0, 0.15, "LRL, RLR: their circles are too far apart", color="#555555", size=17, xanchor="left",
               bg="rgba(255,255,255,0.9)")
    if final:
        x, y, _ = PTS[i_worst]
        k.point(fig, x, y, RED, size=12)
        k.text(fig, x - 0.15, y + 0.3, "disk 0.142 m into<br>the table", color=RED, size=17, xanchor="right",
               bg="rgba(255,255,255,0.85)")
    k.room_axes(fig, xr=(0.85, 6.3), yr=(-0.2, 4.35))
    titles = {0: "the start and the goal pose",
              1: "the circles of radius 0.5 m that touch each pose, one on each side",
              2: "LSL: left on a start circle, straight, left on a goal circle",
              3: "RSR: right, straight, right",
              4: "LSR: left, straight, right",
              5: "RSL: right, straight, left",
              6: "the shortest word is LSL, 2.992 m"}
    title = "but LSL runs through the grown table: Dubins paths ignore obstacles" if final else titles[stage]
    return k.layout(fig, 1100, 860, title, margin=dict(l=70, r=30, t=70, b=60), size=21)


figs = [frame(s) for s in range(7)] + [frame(6, final=True)]
holds = [6, 8, 9, 9, 9, 9, 12, 28]
make_gif(figs, here / "dubins_anim", fps=3, holds=holds, keys=[1, 3, 6, 7], cols=2, width=1000)
