"""Real-time search with the box unknown until seen, on the part of the room the robot crosses (x 1.0 to 4.5 m,
y 0.5 to 4.0 m), one move per frame. Each cell shows h, the robot's current guess of its distance to the door,
starting as the octile distance. Top: LRTA*, which looks only at the 8 neighbours: it raises h of its own cell to the
smallest move + neighbour's h, then moves there. It walks into the pocket between box and table, raises 4 guesses
(orange outline) and leaves: 9 moves, 5.121 m. Bottom: RTAA*, which takes up to 4 cells off an A* open list (light
red), sets h(u) = f(s) - g(u) for each, s being the best cell left on the open list, and moves towards s: 4 searches,
13 cells, 8 moves, 4.414 m. Run -> realtime.gif, realtime_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, box_outline, centre, layout, numbers, outline, robot, room, route, sg, title_at
from gifkit import BLUE, ORANGE, make_gif
from plotly.subplots import make_subplots
from replan import C, GOAL, Grid, lrta, rtaa

here = Path(__file__).parent
XR, YR = (2, 9), (1, 8)
LR, LLOG = lrta()
RR, RTOT, RLOG = rtaa(4)
plen = lambda p: sum(C * ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 for a, b in zip(p, p[1:]))
assert len(LR) - 1 == 9 and round(plen(LR), 3) == 5.121
assert [(L["pos"], round(L["h_old"], 3), round(L["h_new"], 3)) for L in LLOG if L["h_new"] > L["h_old"] + 1e-9] == [
    ((5, 3), 2.414, 3.121), ((4, 3), 2.621, 3.328), ((3, 3), 2.828, 3.121), ((3, 4), 2.621, 2.914)]
assert len(RR) - 1 == 8 and round(plen(RR), 3) == 4.414 and RTOT == 13 and len(RLOG) == 4
assert RLOG[1]["pos"] == (4, 3) and RLOG[1]["best"] == (3, 4) and round(RLOG[1]["f"], 3) == 3.621
G0 = Grid(1)
CELLS = [(i, j) for j in range(*YR) for i in range(*XR) if G0.free((i, j))]
BOX = sorted(G0.box_cells())
OCT = {c: G0.octile(c, GOAL) for c in CELLS}


def lrta_state(k):
    h, seen, raised = dict(OCT), set(), None
    for m, L in enumerate(LLOG[:k]):
        h[L["pos"]] = L["h_new"]
        seen = L["seen"]
        if m == k - 1 and L["h_new"] > L["h_old"] + 1e-9:
            raised = (L["pos"], L["h_old"], L["h_new"])
    if k < len(LLOG):
        seen = LLOG[k]["seen"]
    return h, seen, raised, LR[:k + 1]


def rtaa_state(k):
    """After k moves: the h values, the search that chose the current move, the route so far."""
    h, done, search = dict(OCT), 0, None
    for L in RLOG:
        start = RR.index(L["pos"])
        if start > k:
            break
        search = L
        for u, (_, new) in L["upd"].items():
            h[u] = new
    seen = {c for c in BOX if any(max(abs(c[0] - p[0]), abs(c[1] - p[1])) <= 1 for p in RR[:k + 1])}
    return h, seen, search, RR[:k + 1]


def panel(fig, r, h, seen, work, path, marks):
    st = {c: "box" for c in seen}
    st.update({c: "closed" for c in work if c not in seen})
    room(fig, (1, r), st, XR, YR, labels=False)
    if len(seen) < len(BOX):
        box_outline(fig, (1, r))
    if len(path) > 1:
        route(fig, path, BLUE, width=5, rc=(1, r))
    numbers(fig, {c: f"{h[c]:.2f}" for c in CELLS if c not in seen}, (1, r), size=16, dy=0.1, xr=XR, yr=YR,
            box="white")
    for c in marks:
        outline(fig, c, colour=ORANGE, width=5, rc=(1, r))
    robot(fig, (centre(path[-1])[0], centre(path[-1])[1] - 0.15), (1, r), size=14)
    sg(fig, (1, r), XR, YR, dy=-0.15, size=15)
    axes(fig, (1, r), XR, YR)


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.05)
    kl = min(k, len(LR) - 1)
    h, seen, raised, path = lrta_state(kl)
    marks = [L["pos"] for L in LLOG[:kl] if L["h_new"] > L["h_old"] + 1e-9]
    panel(fig, 1, h, seen, [], path, marks)
    t1 = "LRTA*, one cell ahead"
    if raised:
        t1 += f": h {raised[1]:.2f} to {raised[2]:.2f}"
    elif kl == len(LR) - 1:
        t1 += ": at the door, 5.121 m"
    kr = min(k, len(RR) - 1)
    h2, seen2, search, path2 = rtaa_state(kr)
    work = search["closed"] if search and RR.index(search["pos"]) == kr else []
    marks2 = [u for L in RLOG if RR.index(L["pos"]) <= kr for u, (o, n) in L["upd"].items() if n > o + 1e-9]
    panel(fig, 2, h2, seen2, work, path2, marks2)
    t2 = "RTAA*, 4 cells per search"
    if work:
        t2 += f": f(s) = {search['f']:.2f}"
    elif kr == len(RR) - 1:
        t2 += ": at the door, 4.414 m"
    title_at(fig, t1, 1.0, x=0.24, size=19)
    title_at(fig, t2, 1.0, x=0.76, size=19)
    return layout(fig, f"move {k}" if k else "h starts as the octile distance; the box is unknown", width=1100,
                  height=640, margin=dict(l=20, r=20, t=110, b=20))


n = max(len(LR), len(RR))
figs = [frame(k) for k in range(n)]
holds = [12] + [10] * (n - 2) + [30]
make_gif(figs, here / "realtime", fps=4, holds=holds, keys=[1, 2, 3, n - 1], cols=2, width=900)
