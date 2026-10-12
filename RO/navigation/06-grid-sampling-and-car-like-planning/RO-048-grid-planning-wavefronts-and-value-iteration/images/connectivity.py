"""The door's numbers under three choices, on the room grid. Top: 4-connected moves, each cell numbered with its fewest
moves to the door; walking to a lower number from S takes 8 moves, 4.0 m. Middle: 8-connected moves, still counting
moves: S is 6 moves away, but walking downhill can give 3.414 m (green) or 3.828 m (orange, dashed), because a
diagonal counts as one move like a straight one. Bottom: 8-connected, counting metres (0.5 per straight move, 0.707 per
diagonal): S is 3.414 m away and the downhill walk is the shortest route. Run -> connectivity.png"""
from pathlib import Path

from drawkit import axes, layout, numbers, outline, room, route, sg, title_at
from gifkit import BLUE, GREEN, ORANGE
from gridplan import START, cost_to_go, downhill, nb4, neighbours, path_cost, wavefront
from plotly.subplots import make_subplots

here = Path(__file__).parent
W4, _ = wavefront(nb4)
W8, _ = wavefront(neighbours)
V = cost_to_go()
P4 = downhill(START, W4, nb4)
P8a = [(4, 2), (4, 3), (4, 4), (4, 5), (5, 6), (6, 6), (7, 7)]
P8b = [(4, 2), (3, 3), (3, 4), (4, 5), (5, 6), (6, 6), (7, 7)]
PM = downhill(START, V)
assert W4[START] == 8 and path_cost(P4) == 4.0 and W8[START] == 6
for p in (P8a, P8b):                                    # both are downhill walks on the moves map
    assert all(W8[b] == W8[a] - 1 for a, b in zip(p, p[1:]))
assert round(path_cost(P8a), 3) == 3.414 and round(path_cost(P8b), 3) == 3.828
assert round(V[START], 3) == 3.414 and round(path_cost(PM), 3) == 3.414

fig = make_subplots(rows=3, cols=1, vertical_spacing=0.07)
panels = [(W4, "{:d}", [(P4, BLUE, None)], "4-connected, counting moves: S is 8 moves, route 4.0 m"),
          (W8, "{:d}", [(P8a, GREEN, None), (P8b, ORANGE, "dash")],
           "8-connected, counting moves: S is 6 moves, route 3.414 or 3.828 m"),
          (V, "{:.2f}", [(PM, BLUE, None)], "8-connected, counting metres: S is 3.414 m, route 3.414 m")]
for r, (vals, fmt, routes, t) in enumerate(panels, start=1):
    room(fig, (r, 1), {}, labels=False)
    for p, col, dash in routes:
        route(fig, p, col, width=5, rc=(r, 1), dash=dash)
    numbers(fig, vals, (r, 1), fmt=fmt, size=18 if fmt == "{:d}" else 15, dy=0.08, box="white")
    outline(fig, START, rc=(r, 1), width=4)
    sg(fig, (r, 1), dy=-0.15, size=16)
    axes(fig, (r, 1))
    title_at(fig, t, [1.005, 0.65, 0.295][r - 1], size=20)
layout(fig, "", width=900, height=1680, margin=dict(l=30, r=30, t=50, b=30))
fig.write_image(here / "connectivity.png", scale=1)
