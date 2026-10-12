"""A* on the room grid step by step, from the start cell S to the goal cell G under the door, shown on the part of
the room it touches (x 1.0-4.5 m, y 0-4 m). Each open (green) or closed (red) cell shows its g, the length of the
best route found so far from S (top left), its h, the octile guess of the distance left (top right), and f = g + h
(middle). One expansion per frame: the open cell with the smallest f comes off the open list; ties go to the smaller
h. Two cells get a smaller g on the way (purple outline). The last frame follows each cell's parent arrow back from G:
the route, 3.414 m. Run -> astar_walk.gif, astar_walk_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, outline, room, route, sg, title_at
from gifkit import PURPLE, make_gif
from searchkit import C, GOAL, START, astar, octile

here = Path(__file__).parent
XR, YR = (2, 9), (0, 8)
A = astar(trace=True)
S = A["snaps"]
assert [s["cur"] for s in S] == [START, (5, 3), (5, 4), (5, 5), (4, 3), (4, 4), (5, 6), (6, 7), GOAL]
# the numbers the frames and the text quote
f = lambda s, c: s["g"][c] + octile(c)
assert round(octile(START), 3) == 3.121
assert round(f(S[0], (5, 3)), 3) == 3.121 and round(f(S[0], (4, 3)), 3) == 3.121
assert round(octile((5, 3)), 3) == 2.414 and round(octile((4, 3)), 3) == 2.621
assert round(S[1]["g"][(4, 4)], 3) == 1.414 and round(S[4]["g"][(4, 4)], 3) == 1.0
assert round(f(S[1], (4, 4)), 3) == 3.536 and round(f(S[4], (4, 4)), 3) == 3.121
assert round(S[2]["g"][(4, 5)], 3) == 1.914 and round(S[5]["g"][(4, 5)], 3) == 1.5
assert round(f(S[2], (4, 5)), 3) == 3.828 and round(f(S[5], (4, 5)), 3) == 3.414
assert round(f(S[3], (5, 6)), 3) == 3.414 and round(octile((5, 6)), 3) == 1.207
assert round(A["cost"], 3) == 3.414

TITLES = [
    "start: only S is on the open list, f = 0 + 3.121",
    "1. take S off: its 8 neighbours get g, h and f = g + h",
    "2. smallest f is 3.121, a tie: the smaller h, 2.414, goes first",
    "3. f stays 3.121 heading for G: g grows as fast as h shrinks",
    "4. the diagonal past the table's corner is not allowed: f 3.414 above",
    "5. back to f = 3.121, above S: a cell's g drops, 1.414 to 1.000",
    "6. one cell higher: g drops again, 1.914 to 1.500",
    "7. every f left is 3.414 or more: the smallest h, 1.207, goes first",
    "8. the cell left of G: f still 3.414",
    "9. G comes off the open list with f = g = 3.414: done",
    "10. follow the parent arrows back from G: the route, 3.414 m",
]
CHANGED = {5: (4, 4), 6: (4, 5)}
LEGEND = "in each cell: g (top left), h (top right), f = g + h (middle)"


def numbers(fig, s, cells):
    xs, ys, ts, xg, yg, tg, xh, yh, th = [], [], [], [], [], [], [], [], []
    for c in cells:
        if not (XR[0] <= c[0] < XR[1] and YR[0] <= c[1] < YR[1]):
            continue
        x, y = centre(c)
        g, h = s["g"][c], octile(c)
        xs.append(x), ys.append(y - 0.04), ts.append(f"{g + h:.3f}")
        xg.append(x - 0.24), yg.append(y + 0.17), tg.append(f"{g:.3f}")
        xh.append(x + 0.24), yh.append(y + 0.17), th.append(f"{h:.3f}")
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="text", text=ts, textfont=dict(size=25, color="black")))
    fig.add_trace(go.Scatter(x=xg, y=yg, mode="text", text=tg, textposition="middle right",
                             textfont=dict(size=18, color="#333333")))
    fig.add_trace(go.Scatter(x=xh, y=yh, mode="text", text=th, textposition="middle left",
                             textfont=dict(size=18, color="#1F3F66")))


def frame(k):
    fig = go.Figure()
    if k == 0:
        s = dict(open=[START], closed=[], g={START: 0.0}, parent={START: None}, cur=None)
    else:
        s = S[min(k, len(S)) - 1]
    status = {c: "open" for c in s["open"]}
    status.update({c: "closed" for c in s["closed"]})
    room(fig, None, status, xr=XR, yr=YR, labels=False)
    if k <= len(S):
        numbers(fig, s, list(s["open"]) + list(s["closed"]))
        if s["cur"]:
            outline(fig, s["cur"])
        if k in CHANGED:
            outline(fig, CHANGED[k], colour=PURPLE, width=5)
    else:
        for c, p in s["parent"].items():
            if p is None or not (XR[0] <= c[0] < XR[1]):
                continue
            (x, y), (px, py) = centre(c), centre(p)
            fig.add_annotation(x=x + 0.55 * (px - x), y=y + 0.55 * (py - y), ax=x + 0.1 * (px - x),
                               ay=y + 0.1 * (py - y), xref="x", yref="y", axref="x", ayref="y", text="",
                               showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2.5, arrowcolor="#555555")
        route(fig, A["path"])
    sg(fig, None, XR, YR, dy=-0.18 if k <= len(S) else 0.0)
    axes(fig, None, XR, YR)
    title_at(fig, LEGEND if k <= len(S) else "each arrow points to the cell the best route came from",
             1.0, size=19)
    return layout(fig, TITLES[k], width=900, height=1080, margin=dict(l=30, r=30, t=115, b=30))


figs = [frame(k) for k in range(len(S) + 2)]
holds = [8, 12, 12, 10, 12, 14, 12, 12, 9, 12, 30]
make_gif(figs, here / "astar_walk", fps=2, holds=[max(1, h // 2) for h in holds], keys=[1, 2, 5, 10], cols=2,
         width=720)
