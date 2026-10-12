"""Figure 3: the waypoint graph, a small graph of the same room for tracing by hand. Seven waypoints: the start S at
(2, 1), the four table corners A (3, 1), B (5, 1), C (5.5, 2.5), D (3.5, 3), the pink pole P (1, 3) and the door G
(3.6, 4). Two waypoints are joined when the straight line between them misses the table and the cabinet (running
along a table edge is allowed) and is at most 2.8 m long: 11 edges, each labelled with its length in m.
Run: python waypoints.py -> waypoints.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import GREY
from griddraw import axes, furniture_fill, layout, lines_below, room_lines, wp_labels, wp_nodes, wp_traces
from roomsearch import WP, WP_EDGES, wp_dist

here = Path(__file__).parent
assert len(WP) == 7 and len(WP_EDGES) == 11
assert [round(wp_dist(a, b), 3) for a, b in WP_EDGES] == [2.0, 2.062, 1.0, 1.581, 2.062, 2.421, 1.005, 2.5, 2.5,
                                                          2.786, 2.236]
fig = go.Figure()
for t in furniture_fill() + room_lines(color="#bbb") + wp_traces():
    fig.add_trace(t)
wp_labels(fig)
for t in wp_nodes():
    fig.add_trace(t)
for v, (x, y), dx, dy in [("S", WP["S"], 0, -0.32), ("G", WP["G"], -0.55, 0.14), ("P", WP["P"], 0, 0.32)]:
    fig.add_annotation(x=x + dx, y=y + dy, text={"S": "start", "G": "door", "P": "pink pole"}[v], showarrow=False,
                       font=dict(size=17, color=GREY))
axes(fig, top=4.4)
layout(fig, height=700, title="the waypoint graph: 7 vertices, 11 edges (lengths in m)", b=140)
lines_below(fig, [("A, B, C, D: the table's corners; the table and the cabinet are shaded grey", GREY),
                  ("an edge: the straight line misses the table and the cabinet and is at most 2.8 m long", "black")],
            y0=-0.15)
fig.write_image(here / "waypoints.png")
