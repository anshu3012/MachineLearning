"""Animation: building a probabilistic roadmap in the room's C-space, then the first trip (seed 0, 100 milestones,
10 nearest neighbours). Phase 1: 189 uniform draws, 100 free (blue milestones) and 89 in collision (red crosses).
Phase 2: each milestone tries a straight edge to its 10 nearest milestones; 573 edges tried, 525 free (blue lines),
48 collide (red, dropped); 7,745 configurations checked along the edges. Query: the dock and the door each try their
10 nearest milestones (purple), then A* finds the route, 3.531 m. Run -> build.gif, build_frames.png"""
from pathlib import Path

import numpy as np

import prm
import prmdraw as pd
from gifkit import BLUE, GREEN, PURPLE, RED, make_gif

here = Path(__file__).parent
w = prm.World()
rng = np.random.default_rng(0)
log = []
V = prm.sample_free(w, rng, 100, log)
c1 = w.checks
elog = []
E = prm.connect(w, V, prm.K, elog)
c2 = w.checks - c1
qlog = []
w0 = w.checks
P, L, extra = prm.query(w, V, E, prm.START, prm.DOOR, log=qlog)
cq = w.checks - w0
assert len(log) == 189 and sum(not ok for _, ok in log) == 89 and c1 == 189
assert len(elog) == 573 and len(E) == 525 and c2 == 7745
assert len(qlog) == 20 and len(extra) == 18 and cq == 226 and round(L, 3) == 3.531
VV = V + [prm.START, prm.DOOR]


def frame(title, draws, tried, query, show_route, lines):
    fig = pd.base(w)
    added = [(VV[i], VV[j]) for i, j, ok, _ in elog[:tried] if ok]
    pd.segs(fig, added)
    if not query:
        bad = [(VV[i], VV[j]) for i, j, ok, _ in elog[max(0, tried - 40):tried] if not ok]
        pd.segs(fig, bad, RED, 2.5, "dot")
    if query:
        pd.segs(fig, [(VV[i], VV[j]) for i, j, ok, _ in qlog if ok], PURPLE, 2.5)
        pd.segs(fig, [(VV[i], VV[j]) for i, j, ok, _ in qlog if not ok], RED, 2.5, "dot")
    if show_route:
        pd.route(fig, P)
    pd.dots(fig, [q for q, ok in log[:draws] if not ok], RED, 9, "x-thin", RED)
    pd.dots(fig, [q for q, ok in log[:draws] if ok], BLUE, 8)
    if query:
        pd.place(fig, prm.START, "dock", PURPLE, "bottom left")
        pd.place(fig, prm.DOOR, "door", PURPLE, "middle right")
    pd.panel(fig, lines)
    return pd.finish(fig, title)


figs, holds = [], []
for d in list(range(10, 189, 10)) + [189]:
    free = sum(ok for _, ok in log[:d])
    figs.append(frame(f"phase 1: sample, draw {d} of 189", d, 0, False, False,
                      [("phase 1: sample", "black"), ("draw a configuration at random", "black"),
                       ("and check it", "black"), ("", "black"), (f"draws: {d}", "black"),
                       (f"free, kept as milestones: {free}", BLUE), (f"in collision, dropped: {d - free}", RED),
                       (f"configurations checked: {d}", "black")]))
    holds.append(1)
holds[-1] = 6
for t in list(range(40, 573, 40)) + [573]:
    ok = sum(e[2] for e in elog[:t])
    checks = 189 + sum(e[3] for e in elog[:t])
    figs.append(frame(f"phase 2: connect, edge {t} of 573", 189, t, False, False,
                      [("phase 2: connect", "black"), ("each milestone tries a straight", "black"),
                       ("edge to its 10 nearest milestones", "black"), ("", "black"), (f"edges tried: {t}", "black"),
                       (f"free, added: {ok}", BLUE), (f"collide, dropped: {t - ok}", RED),
                       (f"configurations checked: {checks:,}", "black")]))
    holds.append(1)
holds[-1] = 6
figs.append(frame("query: join the dock and the door to the roadmap", 189, 573, True, False,
                  [("query: dock to door", "black"), ("each end tries its", "black"),
                   ("10 nearest milestones", "black"), ("", "black"), ("edges tried: 20", "black"),
                   ("free, added: 18", PURPLE), ("collide, dropped: 2", RED), ("configurations checked: 226", "black")]))
holds.append(6)
figs.append(frame("query: A* on the roadmap finds the route, 3.531 m", 189, 573, True, True,
                  [("query: dock to door", "black"), ("A* on the roadmap:", "black"), ("route 3.531 m", GREEN),
                   ("", "black"), ("build, once:", "black"), ("7,934 configurations checked", "black"),
                   ("this trip:", "black"), ("226 configurations checked", "black")]))
holds.append(16)
make_gif(figs, here / "build", fps=4, holds=holds, keys=[9, 18, 26, len(figs) - 1], cols=2, width=1000)
