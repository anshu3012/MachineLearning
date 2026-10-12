"""Multi-goal A* to the nearest of three charging docks, one expansion per frame: G under the door (x 3.5-4.0 m,
y 3.5-4.0 m), D1 in the top-left corner (x 0-0.5 m, y 3.5-4.0 m) and D2 below the table's right end (x 5.0-5.5 m,
y 0.5-1.0 m). Each dock has an edge to one extra vertex V, the virtual goal, drawn outside the room; A* searches for V
with h = the smallest octile distance to a dock (plus that dock's edge). Run 1, all edges 0 m: 6 cells climb
towards the door (f = 3.121 m), the door route then rises to f = 3.414 m at the table's corner, and 6 cells run along
the bottom to D2 (f = 3.207 m): route 3.207 m after 12 cells, against 9 + 14 + 7 = 30 for three separate A* runs.
Run 2, D2 busy (its edge 2 m): route to G, 3.414 m, after 12 cells. Run -> multigoal_anim.gif, multigoal_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, title_at
from gifkit import BLUE, PURPLE, make_gif
from searchkit import GOAL, START, astar, multi_goal, octile, straight

here = Path(__file__).parent
r3 = lambda x: round(x, 3)
DOCKS = {"G": GOAL, "D1": (0, 7), "D2": (10, 1)}
BUSY = {DOCKS["D2"]: 2.0}
ALONE = {n: astar(goal=c) for n, c in DOCKS.items()}
R1, R2 = multi_goal(set(DOCKS.values()), trace=True), multi_goal(set(DOCKS.values()), extra=BUSY, trace=True)
# every number the Note or the frames quote
assert [r3(straight(START, c)) for c in DOCKS.values()] == [2.915, 3.202, 3.041]
assert [r3(octile(START, c)) for c in DOCKS.values()] == [3.121, 3.328, 3.207]
assert [r3(a["cost"]) for a in ALONE.values()] == [3.414, 3.914, 3.207]
assert [len(a["order"]) for a in ALONE.values()] == [9, 14, 7] and sum(len(a["order"]) for a in ALONE.values()) == 30
assert r3(R1["cost"]) == 3.207 and R1["path"][-2] == DOCKS["D2"] and len(R1["order"]) == 13 and R1["order"][-1] == "V"
assert R1["path"][:-1] == ALONE["D2"]["path"]
assert r3(R2["cost"]) == 3.414 and R2["path"][-2] == GOAL and len(R2["order"]) == 13
assert r3(3.207 + 2) == 5.207 and r3(0.707 + 2.5) == 3.207


def guess(c, extra):
    """h at cell c and the dock it comes from."""
    hs = {n: octile(c, q) + extra.get(q, 0.0) for n, q in DOCKS.items()}
    n = min(hs, key=hs.get)
    assert sorted(hs.values())[1] > hs[n] + 1e-9, f"tie at {c}"
    return hs[n], n


VX, VY = 3.75, 4.78                               # where V is drawn: above the door, outside the room
EDGES = {"G": [centre(GOAL), (VX, VY)],
         "D1": [centre(DOCKS["D1"]), (0.25, VY), (VX, VY)],
         "D2": [centre(DOCKS["D2"]), (5.25, -0.38), (7.38, -0.38), (7.38, VY), (VX, VY)]}
ELAB = {"G": (4.08, 4.36), "D1": (0.25, 4.36), "D2": (6.3, -0.56)}


def frame(run, k, final=False):
    R, extra = (R1, {}) if run == 1 else (R2, BUSY)
    s = R["snaps"][k - 1] if k else None
    status = {START: "open"}
    if s:
        status = {c: "open" for c in s["open"] if c != "V"}
        status.update({c: "closed" for c in s["closed"] if c != "V"})
    fig = go.Figure()
    room(fig, None, status, labels=False)
    for n, pts in EDGES.items():
        used = final and R["path"][-2] == DOCKS[n]
        xs, ys = zip(*pts)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", hoverinfo="skip",
                                 line=dict(color=BLUE if used else PURPLE, width=5 if used else 3,
                                           dash=None if used else "dash")))
        cost = extra.get(DOCKS[n], 0.0)
        fig.add_annotation(x=ELAB[n][0], y=ELAB[n][1], text=f"<b>{cost:.0f} m</b>" + (": busy" if cost else ""),
                           showarrow=False, font=dict(size=18, color=PURPLE), bgcolor="white")
    for c in DOCKS.values():
        outline(fig, c, colour=PURPLE, width=5)
    if s and s["cur"] != "V":
        outline(fig, s["cur"])
    if final:
        route(fig, R["path"][:-1])
    for n, c in list(DOCKS.items()) + [("S", START)]:
        x, y = centre(c)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{n}</b>"], textfont=dict(size=15),
                                 hoverinfo="skip", marker=dict(size=32, color="white",
                                                               line=dict(color="black", width=1.5))))
    fig.add_trace(go.Scatter(x=[VX], y=[VY], mode="markers+text", text=["<b>V</b>"], textfont=dict(size=18),
                             hoverinfo="skip", marker=dict(size=36, color="white", line=dict(color=PURPLE, width=3))))
    fig.add_annotation(x=VX - 0.3, y=VY - 0.24, text="V, the virtual goal", showarrow=False, xanchor="right",
                       font=dict(size=18, color=PURPLE))
    for x0, x1, y0, y1 in ((-0.1, 7.6, 4.0, 5.2), (-0.1, 7.6, -0.8, 0.0), (7.0, 7.6, -0.8, 5.2), (-0.1, 0.0, -0.8, 5.2)):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, layer="below", fillcolor="white", opacity=1, line_width=0)
    axes(fig)
    fig.update_xaxes(range=[-0.08, 7.5])
    fig.update_yaxes(range=[-0.72, 5.12])
    name = "run 1, all docks free" if run == 1 else "run 2, D2 busy: its edge to V costs 2 m"
    if k == 0:
        h, n = guess(START, extra)
        t = f"{name}: S on the open list"
        sub = (f"h at S = the smallest guess to a dock = {h:.3f} m, from {n}" if run == 1 else
               f"D2's guess becomes 3.207 + 2 = 5.207 m; h at S is still {h:.3f} m, from {n}")
    elif final:
        d = [n for n, c in DOCKS.items() if c == R["path"][-2]][0]
        t = f"{name}: V comes off after {len(R['order']) - 1} cells"
        sub = (f"route to {d}, {R['cost']:.3f} m (blue); three separate A* runs take 30 cells" if run == 1 else
               f"route to {d}, {R['cost']:.3f} m; through D2 it would cost 5.207 m")
    else:
        c = s["cur"]
        g = R["g"][c]
        h, n = guess(c, extra)
        assert abs(r3(g) + r3(h) - r3(g + h)) < 1e-9
        t = f"{name}: cell {k} off the open list"
        sub = f"f = g + h = {g:.3f} + {h:.3f} = {g + h:.3f} m, h from {n}"
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, t, width=900, height=820, margin=dict(l=30, r=30, t=110, b=20))


n1, n2 = len(R1["order"]) - 1, len(R2["order"]) - 1
figs = ([frame(1, k) for k in range(n1 + 1)] + [frame(1, n1 + 1, final=True)]
        + [frame(2, k) for k in range(n2 + 1)] + [frame(2, n2 + 1, final=True)])
holds = [10] + [3] * n1 + [20] + [10] + [3] * n2 + [30]
holds[6] = holds[7] = 8                                   # cells 6 and 7: the search turns from G to D2
make_gif(figs, here / "multigoal_anim", fps=4, holds=holds, keys=[0, 7, n1 + 1, len(figs) - 1], cols=2, width=760)
