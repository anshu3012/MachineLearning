"""Animation: turning a route of straight pieces into a drivable path with Reeds-Shepp pieces (MR 13.3.3). The route
(black, dotted) runs from the start (2, 1) round the table's left side to the pose in front of the door; it is free,
but its corners cannot be driven. Each try joins two poses on the route with the shortest Reeds-Shepp path for the
0.5 m circle: red if it hits an obstacle grown by 0.25 m, green if free. A failed stretch is halved at its middle
pose (the route's point, facing along it) and both halves are tried. Five tries: start to goal fails (L+ S+ L+,
2.992 m, through the grown table), the first half succeeds, the second half fails and is halved again, and both
quarters succeed. Last frame: the drivable path, 3 pieces, 3.893 m, with 3 reversals
(counted over the whole path, including the switch where one piece ends in reverse and the next starts forward). Run -> subdivide_anim.gif,
subdivide_anim_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

import carpaths as cp
import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, RED, make_gif

here = Path(__file__).parent
TRIES, KEPT = m.subdivide()
assert len(TRIES) == 5 and [t[3] for t in TRIES] == [False, True, False, True, True] and len(KEPT) == 3
assert cp.word(TRIES[0][2]) == "L+ S+ L+" and round(cp.length(TRIES[0][2]), 3) == 2.992
TOTAL = sum(cp.length(p) for _, _, p in KEPT)
REV = cp.cusps([seg for _, _, p in KEPT for seg in p if abs(seg[1]) > 1e-9])   # whole path, joins included
assert round(TOTAL, 3) == 3.893 and REV == 3


def frame(n, final=False):
    """After n tries; the n-th try highlighted."""
    fig = make_subplots(rows=1, cols=1)
    k.room(fig, grown=True)
    rx, ry = zip(*m.ROUTE)
    k.line(fig, rx, ry, color="black", width=2, dash="dot")
    marks = sorted({f for t in TRIES[:max(n, 1)] for f in t[:2]})
    for f in marks:
        x, y, th = m.route_pose(f)
        k.arrow(fig, x, y, th, length=0.22, color="black", width=3, size=11)
        k.point(fig, x, y, "black", size=9)
    for i, (f0, f1, p, ok) in enumerate(TRIES[:n]):
        pts = cp.sample(m.route_pose(f0), p, m.RHO)
        cur = i == n - 1 and not final
        if final and not ok:
            continue
        if not ok and not cur:
            k.line(fig, pts[:, 0], pts[:, 1], color=RED, width=2, opacity=0.35)
            continue
        k.line(fig, pts[:, 0], pts[:, 1], color=(BLUE if final else GREEN if ok else RED), width=6 if cur or final else 3)
        if cur:
            k.text(fig, 4.4, 0.5, f"{cp.word(p)}, {cp.length(p):.3f} m: " + ("free, kept" if ok else "collides with an obstacle"),
                   color=GREEN if ok else RED, size=19, bg="rgba(255,255,255,0.9)")
    k.disk(fig, *m.START, color="#222222", width=2, body=False)
    k.disk(fig, *m.DOOR_POSE, color="#222222", width=2, body=False)
    k.room_axes(fig, xr=(0.9, 6.0), yr=(-0.2, 4.35))
    if final:
        title = f"a drivable path: {len(KEPT)} Reeds-Shepp pieces, {TOTAL:.3f} m, {REV} reversals"
    elif n == 0:
        title = "a free route of straight pieces (dotted); its corners cannot be driven"
    else:
        f0, f1 = TRIES[n - 1][:2]
        title = f"try {n}: join the route's poses at {f0:.2f} and {f1:.2f} of its length"
    return k.layout(fig, 1100, 820, title, margin=dict(l=70, r=30, t=70, b=60), size=21)


figs = [frame(n) for n in range(len(TRIES) + 1)] + [frame(len(TRIES), final=True)]
holds = [8] + [10] * len(TRIES) + [28]
make_gif(figs, here / "subdivide_anim", fps=3, holds=holds, keys=[1, 3, 5, len(figs) - 1], cols=2, width=1000)
