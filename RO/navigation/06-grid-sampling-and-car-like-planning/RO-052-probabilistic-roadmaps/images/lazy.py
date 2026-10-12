"""Animation: lazy collision checking on trip 2, door to cabinet, with the 100 milestones of seed 0. Every milestone
(and the two ends) is joined to its 10 nearest without checking the edge (grey). A* finds a candidate route
(orange); its edges are checked in order from the door: a free edge turns green, a colliding edge turns red and is
deleted, and A* searches again. 5 searches, 11 edges checked (4 collide), 129 configurations checked; route
3.579 m. Checking every edge first would cost 7,954 configuration checks. Run -> lazy.gif, lazy_frames.png"""
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

import prm
import prmdraw as pd
from gifkit import GREEN, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
w = prm.World()
V = prm.sample_free(w, np.random.default_rng(0), 100)
w.checks = 0
log = []
P, L, checked, searches = prm.lazy_query(w, V, prm.K, prm.DOOR, prm.CABINET, log)
assert (searches, checked, w.checks, round(L, 3)) == (5, 11, 129, 3.579)
assert sum(not ok for *_, ok in log) == 4
VV = [tuple(p) for p in V] + [prm.DOOR, prm.CABINET]
A = np.asarray(VV)
tree = cKDTree(A)
E = set()
for i in range(len(A)):
    _, idx = tree.query(A[i], k=prm.K + 1)
    E |= {(min(i, j), max(i, j)) for j in idx[1:]}
cost = {}                                    # configurations checked for each logged edge, in order
w2 = prm.World()
for _, _, (a, b), _ in log:
    cost[(a, b)] = w2.seg_free(VV[a], VV[b])[1]


def frame(title, good, bad, cand, current, n_edges, n_conf, s, lines):
    fig = pd.base(w)
    pd.segs(fig, [(VV[a], VV[b]) for a, b in E - set(bad)], "rgba(107,107,107,0.35)", 1.2)
    if cand:
        pd.route(fig, cand, ORANGE, 4)
    pd.segs(fig, [(VV[a], VV[b]) for a, b in good], GREEN, 5)
    pd.segs(fig, [(VV[a], VV[b]) for a, b in bad], RED, 4, "dot")
    if current:
        pd.segs(fig, [current[0]], current[1], 7)
    pd.dots(fig, V, "#4C78A8", 6)
    pd.place(fig, prm.DOOR, "door", PURPLE, "middle right")
    pd.place(fig, prm.CABINET, "cabinet", PURPLE, "middle left")
    pd.panel(fig, lines + [("", "black"), (f"search: {s}", "black"), (f"edges checked: {n_edges}", "black"),
                           (f"configurations checked: {n_conf}", "black"), ("", "black"),
                           ("checking every edge first:", "black"), ("7,954 configurations", "black")], step=0.07)
    return pd.finish(fig, title)


figs, holds = [], []
figs.append(frame("lazy: join every milestone to its 10 nearest, unchecked", [], [], None, None, 0, 0, 0,
                  [("grey: edges not yet checked", "black"), ("only the milestones", "black"),
                   ("themselves were checked", "black")]))
holds.append(6)
good, bad, n_conf, last_s = set(), set(), 0, 0
for k, (s, path, key, ok) in enumerate(log):
    if s != last_s:
        figs.append(frame(f"search {s}: A* finds a candidate route (orange)", sorted(good), sorted(bad), path, None,
                          k, n_conf, s, [("A* treats every unchecked", "black"), ("edge as free", "black")]))
        holds.append(4)
        last_s = s
    n_conf += cost[key]
    seg = (VV[key[0]], VV[key[1]])
    (good if ok else bad).add(key)
    figs.append(frame(f"search {s}: check an edge of the route: " + ("free" if ok else "collides, delete it"),
                      sorted(good), sorted(bad), path, (seg, GREEN if ok else RED), k + 1, n_conf, s,
                      [("check the route's edges", "black"), ("from the door, in order", "black")]))
    holds.append(3 if ok else 5)
assert n_conf == 129
figs.append(frame("route found: 3.579 m after 11 edge checks", sorted(good), sorted(bad), P, None, 11, 129, 5,
                  [("every edge of the route", "black"), ("is checked and free", GREEN)]))
holds.append(16)
make_gif(figs, here / "lazy", fps=3, holds=holds, keys=[1, 5, 9, len(figs) - 1], cols=2, width=1000)
