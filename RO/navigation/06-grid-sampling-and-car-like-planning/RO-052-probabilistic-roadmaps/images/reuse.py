"""Animation: the four trips of the day answered on one roadmap (seed 0, 100 milestones, 525 edges). For each trip
the two ends try their 10 nearest milestones (purple) and A* finds the route (green): 3.531, 3.587, 1.898 and
4.758 m, costing 226, 209, 195 and 212 configuration checks. Bars on the right add up the checks: one roadmap built
once (7,934) plus the trips, against a new roadmap for every trip. Run -> reuse.gif, reuse_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import prm
import prmdraw as pd
from gifkit import BLUE, GREEN, PURPLE, RED, make_gif

here = Path(__file__).parent
w = prm.World()
rng = np.random.default_rng(0)
V = prm.sample_free(w, rng, 100)
E = prm.connect(w, V, prm.K)
BUILD = w.checks
assert BUILD == 7934 and len(E) == 525
trips = []
for a, s, b, g in prm.TRIPS:
    qlog = []
    w0 = w.checks
    P, L, extra = prm.query(w, V, E, s, g, log=qlog)
    trips.append((a, s, b, g, P, L, qlog, w.checks - w0))
assert [round(t[5], 3) for t in trips] == [3.531, 3.587, 1.898, 4.758]
assert [t[7] for t in trips] == [226, 209, 195, 212]
assert BUILD + 842 == 8776 and 4 * BUILD + 842 == 32578
VV = V + [None, None]
POS = {"dock": "bottom left", "door": "middle right", "cabinet": "middle left", "corner": "bottom center"}


def frame(k, stage):
    a, s, b, g, P, L, qlog, cost = trips[k]
    VV[-2:] = [s, g]
    fig = pd.base(w)
    pd.segs(fig, [(V[i], V[j]) for i, j in E], "rgba(76,120,168,0.35)", 1.2)
    pd.dots(fig, V, BLUE, 6)
    pd.segs(fig, [(VV[i], VV[j]) for i, j, ok, _ in qlog if ok], PURPLE, 2.5)
    for j in range(k):
        pd.route(fig, trips[j][4], "rgba(84,162,75,0.35)", 3)
    if stage:
        pd.route(fig, P)
    pd.place(fig, s, a, PURPLE, POS[a])
    pd.place(fig, g, b, PURPLE, POS[b])
    done = sum(t[7] for t in trips[:k + (1 if stage else 0)])
    n = k + (1 if stage else 0)
    once, again = BUILD + done, n * BUILD + done
    fig.add_trace(go.Bar(y=["new roadmap<br>every trip", "one roadmap"], x=[again, once], orientation="h",
                         marker_color=[RED, BLUE], xaxis="x2", yaxis="y2", text=[f"{again:,}", f"{once:,}"],
                         textposition="outside", textfont=dict(size=18), cliponaxis=False, width=0.55))
    fig.update_layout(xaxis2=dict(domain=[0.80, 0.97], anchor="y2", range=[0, 34000], showticklabels=False,
                                  showgrid=False, zeroline=True, title=dict(text="configurations checked",
                                                                            font=dict(size=17))),
                      yaxis2=dict(domain=[0.08, 0.42], anchor="x2", tickfont=dict(size=17)))
    title = (f"trip {k + 1}, {a} to {b}: " + (f"A* finds the route, {L:.3f} m" if stage else "join the two ends"))
    pd.panel(fig, [(f"trip {k + 1}: {a} to {b}", "black"), ("the roadmap is reused;", "black"),
                   ("only the two ends are joined", "black"),
                   (f"this trip: {cost} checks" if stage else "", PURPLE),
                   (f"route: {L:.3f} m" if stage else "", GREEN)], top=0.97)
    return pd.finish(fig, title)


figs, holds = [], []
for k in range(4):
    figs += [frame(k, False), frame(k, True)]
    holds += [3, 6]
holds[-1] = 16
make_gif(figs, here / "reuse", fps=3, holds=holds, keys=[1, 3, 5, 7], cols=2, width=1000)
