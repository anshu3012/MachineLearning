"""Animation: building the visibility roadmap in the room's C-space (seed 0, 300 uniform draws). A free sample that
sees no guard becomes a guard (big dot; the free floor it sees is shaded in its piece's colour). A sample that sees
guards of two different pieces becomes a connector (green) joined to one guard of each, which merges the pieces.
Any other free sample is discarded (grey). Result: 5 guards, 4 connectors, 8 edges, one piece; the last new vertex
comes at draw 240. Run -> visibility.gif, visibility_frames.png"""
from pathlib import Path

import numpy as np

import prm
import prmdraw as pd
from gifkit import GREEN, GREY, make_gif

here = Path(__file__).parent
w = prm.World()
rng = np.random.default_rng(0)
log = []
G, C, E, comp = prm.visibility_roadmap(w, rng, 300, log)
kinds = [k for k, _, _ in log]
assert len(G) == 5 and len(C) == 4 and len(E) == 8 and len(set(comp)) == 1 and w.checks == 10513
assert kinds.count("collision") == 141 and kinds.count("discarded") == 150
assert max(i for i, k in enumerate(kinds) if k in ("guard", "connector")) + 1 == 240
SEEN = {tuple(g): prm.visible_share(w, g)[1:] for g in G}
LIGHT = ["rgba(76,120,168,0.18)", "rgba(227,119,194,0.22)", "rgba(23,190,207,0.22)", "rgba(140,86,75,0.22)",
         "rgba(188,189,34,0.25)"]


def frame(upto, title, cur, lines):
    """State after draw `upto` (1-based), with the draw `cur` (an index) highlighted."""
    guards, label, conns, edges, disc = [], {}, [], [], []
    for i, (k, q, links) in enumerate(log[:upto]):
        if k == "guard":
            label[tuple(q)] = len(guards)
            guards.append(q)
        elif k == "connector":
            conns.append(q)
            edges += [(q, g) for g in links]
            labs = sorted({label[tuple(g)] for g in links})
            for g in label:
                if label[g] in labs:
                    label[g] = labs[0]
        elif k == "discarded":
            disc.append(q)
    fig = pd.base(w)
    for g in guards:
        xs, ys, vis = SEEN[tuple(g)]
        fig.add_scatter(x=xs[vis], y=ys[vis], mode="markers", hoverinfo="skip",
                        marker=dict(color=LIGHT[label[tuple(g)]], size=4, symbol="square"))
    pd.dots(fig, disc, "rgba(107,107,107,0.6)", 6)
    pd.segs(fig, edges, GREEN, 3)
    if cur is not None:
        k, q, links = log[cur]
        pd.segs(fig, [(q, g) for g in links], "black", 2, "dash")
    for g in guards:
        pd.dots(fig, [g], pd.COMP[label[tuple(g)]], 18)
    pd.dots(fig, conns, GREEN, 14, "diamond")
    if cur is not None:
        pd.dots(fig, [log[cur][1]], "black", 16, "circle-open", "black")
    npieces = len(set(label.values()))
    pd.panel(fig, lines + [("", "black"), (f"draws: {upto} of 300", "black"),
                           (f"guards: {len(guards)}, connectors: {len(conns)}", "black"),
                           (f"pieces: {npieces}", "black"), (f"discarded: {len(disc)}", GREY)], step=0.07)
    return pd.finish(fig, title)


figs, holds = [], []
shown_disc = 0
for i, (k, q, links) in enumerate(log):
    if k == "guard":
        figs.append(frame(i + 1, f"draw {i + 1}: sees no guard, so it becomes a guard", i,
                          [("a free sample that sees", "black"), ("no guard becomes a guard;", "black"),
                           ("shaded: the floor it sees", "black")]))
        holds.append(5)
    elif k == "connector":
        figs.append(frame(i + 1, f"draw {i + 1}: sees guards of two pieces, so it becomes a connector", i,
                          [("a sample that sees guards of", "black"), ("two pieces becomes a connector", GREEN),
                           ("and joins the two pieces", "black")]))
        holds.append(5)
    elif k == "discarded" and shown_disc < 2 and i > 10:
        shown_disc += 1
        figs.append(frame(i + 1, f"draw {i + 1}: sees guards of one piece only, so it is discarded", i,
                          [("a sample that sees guards of", "black"), ("only one piece adds nothing:", "black"),
                           ("it is discarded", GREY)]))
        holds.append(5)
figs.append(frame(300, "300 draws: 5 guards and 4 connectors cover the room in one piece", None,
                  [("visibility roadmap:", "black"), ("9 vertices and 8 edges", "black"),
                   ("cover the free floor", "black"), (f"configurations checked: {w.checks:,}", "black")]))
holds.append(16)
make_gif(figs, here / "visibility", fps=2, holds=holds, keys=[0, 3, 6, len(figs) - 1], cols=2, width=1000)
