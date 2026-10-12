"""Figure 1: with diagonal moves allowed (8-connected grid, 0.5 m straight, 0.707 m diagonal, no cutting corners),
breadth-first search returns a 6-move route of 3.828 m (orange, dashed: 4 diagonals and 2 straight moves), while the
shortest route, found by Dijkstra's algorithm, also has 6 moves but is 3.414 m long (green: 2 diagonals and 4 straight
moves). The two routes share their last 3 moves. Run: python routes8.py -> routes8.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import GREEN, ORANGE
from griddraw import axes, grid_lines, grid_trace, layout, lines_below, room_lines, route, start_goal
from roomsearch import GOAL, START, STEPS8, bfs, dijkstra, length, neighbours

here = Path(__file__).parent
B = bfs(STEPS8)["path"]
D = dijkstra(lambda c: neighbours(c, STEPS8), START, GOAL)["path"]
assert len(B) - 1 == 6 and round(length(B), 3) == 3.828 and len(D) - 1 == 6 and round(length(D), 3) == 3.414
assert B[3:] == D[3:]

fig = go.Figure()
fig.add_trace(grid_trace())
fig.add_trace(grid_lines())
for t in room_lines():
    fig.add_trace(t)
fig.add_trace(route(D, GREEN, 7))
shifted = [(i + 0.12, j - 0.12) for i, j in B]                 # drawn slightly off the cell centres so both show
fig.add_trace(route(shifted, ORANGE, 4, dash="dash"))
start_goal(fig)
axes(fig)
layout(fig, height=740, title="diagonal moves allowed: two 6-move routes", b=170)
lines_below(fig, [("orange, dashed: breadth-first search, 6 moves = 3.828 m (4 diagonals, 2 straight)", ORANGE),
                  ("green: the shortest route, 6 moves = 3.414 m (2 diagonals, 4 straight)", GREEN),
                  ("the orange route is drawn a little to the lower right so that both stay visible", "black")],
            y0=-0.14)
fig.write_image(here / "routes8.png")
print(B, D)
