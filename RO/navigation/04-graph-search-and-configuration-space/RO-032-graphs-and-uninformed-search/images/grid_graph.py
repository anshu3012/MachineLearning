"""Figure 2: the free cells of the room's 0.5 m grid as a graph. Each of the 76 free cells is a vertex (a dot at its
centre); two vertices are joined by an edge (a line) when the cells share a side, so one 0.5 m move left, down, up
or right goes between them: 114 edges. The start cell's 4 edges are orange: all four moves from S stay in free
cells. Run: python grid_graph.py -> grid_graph.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import GREY, ORANGE
from griddraw import axes, grid_lines, grid_trace, layout, lines_below, room_lines, start_goal
from roomsearch import FREE, START, centre, neighbours

here = Path(__file__).parent
EDGES = sorted({tuple(sorted((c, n))) for c in FREE for n, _ in neighbours(c)})
SN = [n for n, _ in neighbours(START)]
assert len(FREE) == 76 and len(EDGES) == 114 and len(SN) == 4

fig = go.Figure()
fig.add_trace(grid_trace())
fig.add_trace(grid_lines())
for t in room_lines():
    fig.add_trace(t)
xs, ys = [], []
for a, b in EDGES:
    (x0, y0), (x1, y1) = centre(a), centre(b)
    xs += [x0, x1, None]
    ys += [y0, y1, None]
fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#4C78A8", width=2.5), hoverinfo="skip"))
for n in SN:
    (x0, y0), (x1, y1) = centre(START), centre(n)
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=ORANGE, width=7),
                             hoverinfo="skip"))
px, py = zip(*(centre(c) for c in FREE))
fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(size=10, color="#4C78A8"), hoverinfo="skip"))
start_goal(fig)
axes(fig)
layout(fig, height=740, title="the free cells as a graph: 76 vertices (dots), 114 edges (lines)", b=170)
lines_below(fig, [("an edge joins two free cells that share a side: one 0.5 m move left, down, up or right", "black"),
                  ("orange: the 4 edges of the start cell S, one per move", ORANGE),
                  ("grey cells are blocked, so they have no vertex", GREY)], y0=-0.14)
fig.write_image(here / "grid_graph.png")
print(len(FREE), "vertices", len(EDGES), "edges; start neighbours", SN)
