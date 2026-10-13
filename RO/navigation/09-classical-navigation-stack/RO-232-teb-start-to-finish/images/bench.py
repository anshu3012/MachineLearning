"""Roesmann, Makarow and Bertram 2021 (arXiv 2006.03534), Table I: the same differential-drive robot (speed -0.2 to
0.4 m/s, turn rate at most 0.4 rad/s) drives to three goals in a 10 m x 10 m map in ROS, the global plan refreshed
every 2 s and each local planner run at 10 Hz. Top: CPU time per planning step, median (bar) with the 5 and 95 percent
quantiles (whiskers). Bottom: total travel time. Trajectory rollout is the DWA package in its rollout mode. The values
are typed in from the paper. Run -> bench.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE
from plotly.subplots import make_subplots

here = Path(__file__).parent
ROWS = [("elastic band", 10.2, 1.7, 18.3, 192.5, GREY), ("trajectory rollout (DWA)", 19.1, 14.8, 22.1, 122.1, BLUE),
        ("TEB", 5.9, 3.0, 9.4, 126.9, ORANGE), ("MPC, least time", 12.5, 5.4, 21.8, 124.6, PURPLE),
        ("MPC, quadratic cost", 15.8, 7.5, 25.3, 116.0, PURPLE), ("MPC, hybrid", 14.2, 7.6, 22.4, 140.1, PURPLE)]
names = [r[0] for r in ROWS][::-1]
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16,
                    subplot_titles=("CPU time per planning step (ms): median, 5 to 95 percent", "travel time (s)"))
for r in ROWS[::-1]:
    fig.add_trace(go.Bar(y=[r[0]], x=[r[1]], orientation="h", marker_color=r[5], error_x=dict(type="data", symmetric=False, array=[r[3] - r[1]], arrayminus=[r[1] - r[2]],
                                      color="#333333", thickness=2)), row=1, col=1)
    fig.add_trace(go.Bar(y=[r[0]], x=[r[4]], orientation="h", marker_color=r[5], text=[f"{r[4]}"], textposition="outside"),
                  row=2, col=1)
for r in ROWS:
    fig.add_annotation(x=r[3] + 0.4, y=r[0], text=f"{r[1]}", showarrow=False, xanchor="left", xref="x", yref="y",
                       font=dict(size=20))
fig.update_xaxes(range=[0, 33], row=1, col=1)
fig.update_xaxes(range=[0, 230], row=2, col=1)
fig.update_yaxes(categoryorder="array", categoryarray=names)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, showlegend=False, bargap=0.3,
                  margin=dict(l=20, r=20, t=50, b=40))
fig.update_annotations(font=dict(size=21))
fig.write_image(here / "bench.png")
