"""Figure 4: the search tree of the waypoint graph growing. Every path from S that never visits a waypoint twice is
one node of the tree; a path that reaches the door G is not extended. One new path per frame, in level order: level 1
(3 paths), level 2 (8), level 3 (11). Top: the newest path drawn on the room (orange). Bottom: the tree; green = a path
that reaches G, purple outline = a copy of waypoint D. The last frame gives the counts of the whole tree (6 levels,
40 paths, 14 reach G). Run: python search_tree.py -> search_tree.gif, search_tree_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, PURPLE, make_gif
from griddraw import furniture_fill, room_lines, wp_nodes, wp_traces
from plotly.subplots import make_subplots
from roomsearch import tree_paths, wp_nbrs

here = Path(__file__).parent
FULL = tree_paths(wp_nbrs, "S", "G", 6)
T = [p for p in FULL if len(p) <= 4]                            # levels 0 to 3
LEVELS = [sum(len(p) == k + 1 for p in FULL) for k in range(7)]
assert LEVELS == [1, 3, 8, 11, 10, 5, 2] and len(FULL) == 40 and sum(p[-1] == "G" for p in FULL) == 14
assert len(T) == 23 and sum(p[-1] == "G" for p in T) == 6
D_COPIES = sum(p[-1] == "D" for p in T)
assert D_COPIES == 3

# tree layout: leaves (no child within level 3) get slots left to right; a parent sits above the middle of its children
kids = {tuple(p): [q for q in T if len(q) == len(p) + 1 and q[:-1] == p] for p in T}
pos, slot = {}, [0]


def place(p):
    ch = kids[tuple(p)]
    if not ch:
        pos[tuple(p)] = (slot[0], -(len(p) - 1))
        slot[0] += 1
    else:
        for q in ch:
            place(q)
        xs = [pos[tuple(q)][0] for q in ch]
        pos[tuple(p)] = ((min(xs) + max(xs)) / 2, -(len(p) - 1))


place(["S"])
NSLOT = slot[0]


def frame(n, title, lines, final=False):
    """The first n paths of T are drawn; path n - 1 is the newest."""
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.06)
    new = T[n - 1]
    for t in furniture_fill() + room_lines(color="#bbb") + wp_traces(highlight=new if not final else ()):
        fig.add_trace(t, 1, 1)
    for t in wp_nodes(fill={v: "#fdd0a2" for v in new} if not final else None, size=30, font=16):
        fig.add_trace(t, 1, 1)
    shown = T[:n]
    for p in shown[1:]:
        (x0, y0), (x1, y1) = pos[tuple(p[:-1])], pos[tuple(p)]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color="#999", width=2),
                                 hoverinfo="skip"), 2, 1)
    for p in shown:
        x, y = pos[tuple(p)]
        is_new = p is new and not final
        fill = GREEN if p[-1] == "G" else ("#fdd0a2" if is_new else "white")
        edge = PURPLE if (final and p[-1] == "D") else (ORANGE if is_new else "#444")
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{p[-1]}</b>"],
                                 marker=dict(size=30, color=fill, line=dict(color=edge, width=4 if edge != "#444" else 2)),
                                 textfont=dict(size=16, color="white" if p[-1] == "G" else "black"), hoverinfo="skip"),
                      2, 1)
    for k in range(4):
        fig.add_annotation(x=-0.9, y=-k, text=f"level {k}", showarrow=False, xanchor="right",
                           font=dict(size=15, color=GREY), row=2, col=1)
    fig.update_xaxes(range=[-0.1, 7.1], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.1, 4.15], visible=False, scaleanchor="x", row=1, col=1)
    fig.update_xaxes(range=[-2.6, NSLOT - 0.4], visible=False, row=2, col=1)
    fig.update_yaxes(range=[-3.45, 0.45], visible=False, row=2, col=1)
    fig.update_layout(template="simple_white", width=1000, height=1150, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=150), title=dict(text=title, x=0.5, font=dict(size=22)))
    for k, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.0, y=-0.03 - 0.045 * k, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=19, color=col))
    return fig


figs, holds, keys = [], [], []
for n in range(1, len(T) + 1):
    p = T[n - 1]
    lvl = len(p) - 1
    title = "level 0: the path that has not moved yet" if n == 1 else f"level {lvl}: path " + "–".join(p)
    lines = [("each node of the tree is a whole path from S; orange: the newest path", ORANGE)]
    if p[-1] == "G":
        lines.append(("green: this path reaches the door G, so it is not extended", GREEN))
    else:
        lines.append(("a path never visits a waypoint twice", "black"))
    figs.append(frame(n, title, lines))
    holds.append(8 if n in (1, 4, 12, 23) or p[-1] == "G" else 3)
    if n in (4, 12):
        keys.append(len(figs) - 1)
figs.append(frame(len(T), "levels 0 to 3: 23 paths, 6 of them reach G",
                  [(f"purple outline: waypoint D appears {D_COPIES} times; each copy is searched again below it", PURPLE),
                   ("the whole tree goes 6 levels deep: 40 paths, of which 14 reach G", "black"),
                   ("levels 0 to 6 hold 1, 3, 8, 11, 10, 5 and 2 paths", GREY)], final=True))
holds.append(30)
keys.append(len(figs) - 1)
keys = [0] + keys
make_gif(figs, here / "search_tree.gif", fps=4, holds=holds, keys=keys, cols=2, width=760)
print("levels", LEVELS, "D copies to level 3", D_COPIES, "slots", NSLOT)
