"""Animation: the two sampling strategies for narrow passages, draw by draw, in the C-space of the robot carrying the
0.8 m tray (obstacles grown by 0.4 m, orange). Part 1, Gaussian sampling (sigma 0.1 m, seed 22): a uniform
configuration q1 and a second one q2 near it; if exactly one of the two is free, the free one becomes a milestone.
Part 2, the bridge test (sigma 0.3 m, seed 2): q1 must collide, q2 near it must collide too, and the midpoint m of
the two must be free; then m becomes a milestone. Green: free; red: in collision; blue: kept as a milestone.
Run -> pairs.gif, pairs_frames.png"""
from pathlib import Path

import numpy as np

import prm
import prmdraw as pd
from gifkit import BLUE, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
w = prm.World(0.4)
col = lambda q: GREEN if w.free(q, False) else RED

# ---- part 1: Gaussian sampling
rng = np.random.default_rng(22)
G = []
while sum(k is not None for k, _, _ in G) < 20:
    G.append(prm.gaussian_sample(w, rng, 0.1))
nG = len(G)
first8 = G[:8]
assert sum(k is not None for k, _, _ in first8) == 2
# ---- part 2: the bridge test
rng = np.random.default_rng(2)
B = []
while sum(m is not None for m, _, _, _ in B) < 10:
    B.append(prm.bridge_sample(w, rng, 0.3))
nB = len(B)
assert B[3][0] is not None and all(b[0] is None for b in B[:3]) and nB == 460, nB


def frame(title, kept, pair, lines):
    fig = pd.base(w)
    pd.dots(fig, kept, BLUE, 11)
    for pts, color, size, sym in pair:
        pd.dots(fig, pts, color, size, sym, "black")
    pd.panel(fig, lines, step=0.07)
    return pd.finish(fig, title)


figs, holds = [], []
keptG = []
for i, (k, q1, q2) in enumerate(first8):
    f1, f2 = w.free(q1, False), w.free(q2, False)
    out = ("exactly one is free: keep it", BLUE) if k is not None else (
        ("both free: drop both", GREY) if f1 else ("both collide: drop both", GREY))
    figs.append(frame(f"Gaussian sampling, draw {i + 1}", keptG,
                      [([q1], col(q1), 13, "circle"), ([q2], col(q2), 13, "diamond")],
                      [("Gaussian sampling", "black"), ("q1 (circle): uniform", "black"),
                       ("q2 (diamond): near q1,", "black"), ("standard deviation 0.1 m", "black"), ("", "black"),
                       (f"draw {i + 1}: q1 " + ("free" if f1 else "collides") + ", q2 " + ("free" if f2 else "collides"),
                        "black"), out, ("", "black"), (f"milestones so far: {len(keptG) + (k is not None)}", BLUE)]))
    holds.append(4)
    if k is not None:
        keptG.append(k)
keptG = [k for k, _, _ in G if k is not None]
figs.append(frame(f"Gaussian sampling: 20 milestones from {nG} draws", keptG, [],
                  [("Gaussian sampling", "black"), (f"20 milestones from {nG} draws", BLUE), ("", "black"),
                   ("each kept milestone has", "black"), ("an obstacle within about", "black"),
                   ("0.1 m: the milestones", "black"), ("hug the obstacles", "black")]))
holds.append(12)
keptB = []
for i, (m, q1, q2, mid) in enumerate(B[:6]):
    pair = [([q1], col(q1), 13, "circle")]
    if q2 is None:
        txt = [("q1 is free: drop it", GREY)]
    else:
        pair.append(([q2], col(q2), 13, "diamond"))
        if mid is None:
            txt = [("q1 collides, q2 is free:", "black"), ("drop both", GREY)]
        else:
            pair.append(([mid], col(mid), 15, "star"))
            txt = [("q1 and q2 collide;", "black"),
                   ("the midpoint m is free: keep m", BLUE) if m is not None else ("the midpoint m collides: drop", GREY)]
    figs.append(frame(f"bridge test, draw {i + 1}", keptB, pair,
                      [("bridge test", "black"), ("q1 (circle): uniform", "black"),
                       ("q2 (diamond): near q1,", "black"), ("standard deviation 0.3 m", "black"),
                       ("m (star): their midpoint", "black"), ("", "black")] + txt +
                      [("", "black"), (f"milestones so far: {len(keptB) + (m is not None)}", BLUE)]))
    holds.append(5 if m is not None else 4)
    if m is not None:
        keptB.append(m)
keptB = [m for m, _, _, _ in B if m is not None]
figs.append(frame(f"bridge test: 10 milestones from {nB} draws", keptB, [],
                  [("bridge test", "black"), (f"10 milestones from {nB} draws", BLUE), ("", "black"),
                   ("each kept milestone sits in a", "black"), ("thin gap between two obstacles:", "black"),
                   ("under the table, beside the", "black"), ("pink pole, above the table", "black")]))
holds.append(16)
make_gif(figs, here / "pairs", fps=2, holds=holds, keys=[2, 8, 12, len(figs) - 1], cols=2, width=1000)
