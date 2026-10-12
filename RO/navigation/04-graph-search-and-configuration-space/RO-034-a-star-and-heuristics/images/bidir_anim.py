"""Backward and bidirectional search on the room grid, one expansion per frame in both panels. Top: Dijkstra run
backwards, from the goal cell G towards S (blue: taken off its open list; pale blue: on it); it reaches S after 31
cells. Bottom: bidirectional Dijkstra, one expansion from S (red and green) and one from G (blue) in turn; it stops
when a cell has come off both open lists, after 38 cells, and the route is the cell both searches reached with the
smallest sum of the two distances: 3.414 m. The forward search alone needs 54 cells.
Run -> bidir_anim.gif, bidir_anim_frames.png"""
from pathlib import Path

from drawkit import axes, layout, outline, room, route, sg, title_at
from gifkit import PURPLE, make_gif
from plotly.subplots import make_subplots
from searchkit import GOAL, START, bidirectional, dijkstra

here = Path(__file__).parent
BW, BI = dijkstra(start=GOAL, goal=START, trace=True), bidirectional()
assert len(BW["order"]) == 31 and BI["expanded"] == 38 and round(BI["cost"], 3) == 3.414
assert len(dijkstra()["order"]) == 54 and round(BW["cost"], 3) == 3.414
assert sum(f["turn"] == 0 for f in BI["frames"]) == 19 and sum(f["turn"] == 1 for f in BI["frames"]) == 19


def frame(k):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.09)
    # top: backward Dijkstra
    n = min(k, len(BW["snaps"]))
    s = BW["snaps"][n - 1] if n else None
    st = {}
    if s:
        st.update({c: "back_open" for c in s["open"]})
        st.update({c: "back" for c in s["closed"]})
    room(fig, (1, 1), st, labels=False)
    if s:
        outline(fig, s["cur"], rc=(1, 1))
    if n == len(BW["snaps"]):
        route(fig, BW["path"][::-1], rc=(1, 1))
    sg(fig, (1, 1))
    t1 = f"backward, from G: {n} cells" + (f", route {BW['cost']:.3f} m" if n == len(BW["snaps"]) else "")
    # bottom: bidirectional
    m = min(k, len(BI["frames"]))
    fr = BI["frames"][m - 1] if m else None
    st = {}
    if fr:
        st.update({c: "open" for c in fr["open"][0]})
        st.update({c: "back_open" for c in fr["open"][1]})
        st.update({c: "closed" for c in fr["closed"][0]})
        st.update({c: "back" for c in fr["closed"][1]})
    room(fig, (2, 1), st, labels=False)
    done = m == len(BI["frames"])
    if fr:
        outline(fig, fr["cur"], rc=(2, 1))
    if done:
        outline(fig, BI["w"], colour=PURPLE, rc=(2, 1))
        route(fig, BI["path"], rc=(2, 1))
    sg(fig, (2, 1))
    t2 = (f"bidirectional: {m} cells" + (", one from each side in turn" if not done else
                                         f": a cell is off both lists; route {BI['cost']:.3f} m"))
    for rc in ((1, 1), (2, 1)):
        axes(fig, rc)
    title_at(fig, t1, 1.0)
    title_at(fig, t2, 0.455)
    title = "two ways to save cells: search from G, or from both ends" if k == 0 else f"expansion {k}"
    return layout(fig, title, width=900, height=1060, margin=dict(l=30, r=30, t=110, b=30))


ks = list(range(len(BI["frames"]) + 1))
figs = [frame(k) for k in ks]
holds = [6] + [2] * (len(ks) - 2) + [24]
holds[31] = 8
make_gif(figs, here / "bidir_anim", fps=5, holds=holds, keys=[10, 20, 31, 38], cols=2, width=700)
