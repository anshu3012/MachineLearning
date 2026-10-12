"""Animation: the roadmap of seed 0 with its first 5, 10, 20, 50 and 100 milestones (each connected to its 10
nearest). Each piece of the roadmap has its own colour; red squares mark free floor (tested every 0.1 m) from which
no straight free edge reaches one of the 10 nearest milestones. With 5 and 10 milestones the roadmap has 2 pieces
and trips 2 and 4 fail; from 20 milestones on it is one piece, like the free space, and every trip is found.
Run -> grow.gif, grow_frames.png"""
from pathlib import Path

import numpy as np

import prm
import prmdraw as pd
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent
w = prm.World()
rng = np.random.default_rng(0)
V = prm.sample_free(w, rng, 100)
EXPECT = {5: (2, 0.982, [1, 0, 1, 0]), 10: (2, 0.997, [1, 0, 1, 0]), 20: (1, 0.999, [1, 1, 1, 1]),
          50: (1, 1.0, [1, 1, 1, 1]), 100: (1, 1.0, [1, 1, 1, 1])}
figs, holds = [], []
for n, (pieces, share, found) in EXPECT.items():
    E = prm.connect(prm.World(), V[:n], prm.K)
    nc, lab = prm.components(n, E)
    acc, P, a = prm.accessible_share(w, V[:n], prm.K, 0.1)
    ok = [prm.query(prm.World(), V[:n], E, s, g)[0] is not None for _, s, _, g in prm.TRIPS]
    assert nc == pieces and round(acc, 3) == share and ok == [bool(f) for f in found], (n, nc, acc, ok)
    fig = pd.base(w)
    pd.dots(fig, P[~a], RED, 7, "square", RED)
    for k in range(nc):
        col = pd.COMP[k]
        pd.segs(fig, [(V[i], V[j]) for i, j in E if lab[i] == k], col, 1.6)
        pd.dots(fig, [V[i] for i in range(n) if lab[i] == k], col, 10)
    lines = [(f"milestones: {n}", "black"),
             (f"pieces of the roadmap: {nc}", pd.COMP[1] if nc > 1 else "black"),
             ("pieces of the free space: 1", "black"), ("", "black"),
             (f"free floor that reaches", "black"), (f"a milestone: {100 * acc:.1f} percent", "black"),
             (f"red: the other {100 * (1 - acc):.1f} percent", RED) if acc < 1 else ("", "black"), ("", "black"),
             ("trips found:", "black")]
    lines += [(f"{i + 1}  {a_} to {b_}: " + ("yes" if f else "no"), GREEN if f else RED)
              for i, ((a_, _, b_, _), f) in enumerate(zip(prm.TRIPS, ok))]
    pd.panel(fig, lines, step=0.07)
    figs.append(pd.finish(fig, f"{n} milestones: " + (f"{nc} pieces, trips 2 and 4 fail" if nc > 1
                                                       else "one piece, every trip found")))
    holds.append(8)
holds[-1] = 16
make_gif(figs, here / "grow", fps=2, holds=holds, keys=[0, 1, 2, 4], cols=2, width=1000)
