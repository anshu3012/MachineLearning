"""Figure 8: how the search tree grows level by level. Grey bars: every sequence of d moves on the grid, 4 choices per
move, 4^d of them. Orange bars: the paths of d moves in our room that stay in free cells and never revisit a cell
(the nodes on level d of the room's search tree). One level per frame, d = 0 to 8; the axis is linear, so early
levels look empty. The last frame: 65,536 move sequences of 8 moves, 1,447 room paths, 16 of which end at the door;
breadth-first search with a visited list took 57 expansions. Run: python growth.py -> growth.gif, growth_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, make_gif
from roomsearch import GOAL, START, neighbours, tree_paths

here = Path(__file__).parent
P = tree_paths(lambda c: neighbours(c), START, None, 8)
ROOM = [sum(len(p) == d + 1 for p in P) for d in range(9)]
AT_GOAL = sum(len(p) == 9 and p[-1] == GOAL for p in P)
FOUR = [4 ** d for d in range(9)]
assert ROOM == [1, 4, 11, 30, 69, 158, 342, 728, 1447] and AT_GOAL == 16 and FOUR[-1] == 65536
assert sum(FOUR) == 87381 and sum(ROOM) == 2790


def frame(d, title, lines):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(d + 1)), y=FOUR[:d + 1], marker_color="#bdbdbd", offsetgroup=0))
    fig.add_trace(go.Bar(x=list(range(d + 1)), y=ROOM[:d + 1], marker_color=ORANGE, offsetgroup=1))
    for k in range(d + 1):                                         # labels as annotations: fixed size, never shrunk
        for v, dx, col in ((FOUR[k], -0.2, GREY), (ROOM[k], 0.2, ORANGE)):
            fig.add_annotation(x=k + dx, y=v, text=f"{v:,}", textangle=-90, showarrow=False, yanchor="bottom",
                               yshift=4, font=dict(size=17, color=col))
    fig.update_xaxes(range=[-0.6, 8.6], dtick=1, title="level d (moves from the start)")
    fig.update_yaxes(range=[0, 82000], title="paths on level d", tickformat=",")
    fig.update_layout(template="simple_white", width=1000, height=760, font=FONT, showlegend=False, bargap=0.25,
                      margin=dict(l=110, r=30, t=80, b=200), title=dict(text=title, x=0.5, font=dict(size=22)))
    base = [("grey: every sequence of d moves, 4 choices each: 4<sup>d</sup> (linear axis)", GREY),
            ("orange: paths of d moves in the room that never revisit a cell", ORANGE)]
    for k, (s, col) in enumerate(base + lines):
        fig.add_annotation(x=0.0, y=-0.17 - 0.06 * k, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=19, color=col))
    return fig


figs, holds = [], []
for d in range(9):
    tot4, totr = sum(FOUR[:d + 1]), sum(ROOM[:d + 1])
    lines = [(f"levels 0 to {d} together: {tot4:,} move sequences, {totr:,} room paths", "black")]
    title = f"level {d}: 4<sup>{d}</sup> = {FOUR[d]:,} sequences, {ROOM[d]:,} room paths"
    if d == 8:
        lines.append((f"{AT_GOAL} of the {ROOM[8]:,} room paths on level 8 end at the door; "
                      "breadth-first search needed 57 expansions", GREEN))
    figs.append(frame(d, title, lines))
    holds.append(30 if d == 8 else 6)
make_gif(figs, here / "growth.gif", fps=2, holds=holds, keys=[3, 6, 7, 8], cols=2, width=900)
print("room levels", ROOM, "at goal", AT_GOAL)
