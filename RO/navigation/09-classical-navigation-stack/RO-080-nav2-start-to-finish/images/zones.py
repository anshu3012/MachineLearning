"""Still: the collision monitor package's example zones (nav2_collision_monitor/params/collision_monitor_params.yaml,
all four enabled) on our robot at 3.70 s of the example-zones run, robot frame, x forward (our Python version; not
Nav2 running). Stop box 0.3 m ahead x 0.6 m wide (4 returns stop the robot), slowdown box 0.8 m x 0.8 m (30 percent),
limit box 1.0 m x 1.0 m (0.4 m/s, 0.5 rad/s), approach footprint (2.0 s). The person's returns fall in the stop box,
so the command becomes 0; the person never moves, and the progress checker fails the goal at 12.45 s.
Plotly, because it is drawn from the same run as the animations.
Run -> zones.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import nav2sim as N
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED

here = Path(__file__).parent
R = N.results()
L = R["example_zones"]["log"]
x = [y for y in L if y["zone"] and y["zone"].endswith("stop")][0]
assert round(x["t"], 2) == 3.70 and R["example_zones"]["result"] == "failed to make progress"
pts = x["scan_base"]
Z = {z["name"]: z for z in N.MONITOR_EXAMPLE}
n_stop = N.points_inside(Z["PolygonStop"]["poly"], pts)
assert n_stop >= 4

fig = go.Figure()
near = pts[(np.abs(pts[:, 0]) < 1.2) & (np.abs(pts[:, 1]) < 1.0)]
for name, color, dash, label, pos in (("PolygonLimit", PURPLE, "dot", "limit: 0.4 m/s, 0.5 rad/s", (0.0, 0.58)),
                                      ("PolygonSlow", ORANGE, "dash", "slowdown: x 0.3", (0.0, 0.47)),
                                      ("PolygonStop", RED, None, "stop", (0.15, 0.35))):
    P = np.vstack([Z[name]["poly"], Z[name]["poly"][:1]])
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=color, width=3, dash=dash),
                             hoverinfo="skip"))
    fig.add_annotation(x=pos[0], y=pos[1], text=label, showarrow=False, font=dict(size=18, color=color))
F = np.vstack([Z["FootprintApproach"]["poly"], Z["FootprintApproach"]["poly"][:1]])
fig.add_trace(go.Scatter(x=F[:, 0], y=F[:, 1], mode="lines", line=dict(color=BLUE, width=3), hoverinfo="skip"))
fig.add_trace(go.Scatter(x=[0, 0.25], y=[0, 0], mode="lines", line=dict(color=BLUE, width=3), hoverinfo="skip"))
fig.add_trace(go.Scatter(x=near[:, 0], y=near[:, 1], mode="markers", marker=dict(size=7, color="black"),
                         hoverinfo="skip"))
fig.add_annotation(x=0.65, y=0.3, text=f"{n_stop} returns of the person<br>in the stop box: command 0", showarrow=False,
                   xanchor="left", align="left", font=dict(size=18, color=RED))
fig.update_xaxes(range=[-0.7, 1.2], title="x, forward (m)", dtick=0.25)
fig.update_yaxes(range=[-0.75, 0.7], title="y, left (m)", dtick=0.25, scaleanchor="x")
fig.update_layout(template="simple_white", width=900, height=760, font=FONT, showlegend=False,
                  margin=dict(l=80, r=20, t=70, b=70),
                  title=dict(text="the package's example zones on our robot at 3.70 s", x=0.5, y=0.97, font=dict(size=20)))
fig.write_image(here / "zones.png")
