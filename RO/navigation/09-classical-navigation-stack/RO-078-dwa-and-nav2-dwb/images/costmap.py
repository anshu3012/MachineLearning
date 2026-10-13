"""The local costmap the critics read in the person's cycle (t = 2.4 s). Top: a cell's cost against the distance d
from its centre to the nearest obstacle (nav2_costmap_2d InflationLayer::computeCost with inflation_radius 0.70 m,
cost_scaling_factor 3.0 and our robot's radius 0.25 m): 254 inside, 253 within the robot's radius, then
252 exp(-3 (d - 0.25)), 0 beyond 0.70 m. Bottom: the 3 m x 3 m window of 0.05 m cells around the robot, coloured by
that cost, with the end of the chosen rollout (cost 160, 0.40 m from the person). Run -> costmap.png"""
import math

import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE
from plotly.subplots import make_subplots

R = d.results()
o = [c for c in R["replan"]["cycles"] if abs(c["t"] - d.T_PERSON) < 1e-9][0]
cm, rec = o["cm"], o["rec"]
end = rec["traj"][-1]
i, j, _ = cm.world_to_map(end[0], end[1])
assert cm.cost[j, i] == 160 and round(float(cm.dist[j, i]), 2) == 0.40
assert [d.inflation_cost(x) for x in (0.3, 0.4, 0.5, 0.7)] == [216, 160, 119, 65]

fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], vertical_spacing=0.09)
dd = np.linspace(0.25001, 0.70, 200)
fig.add_trace(go.Scatter(x=[-0.05, 0, 0], y=[254, 254, 253], mode="lines", line=dict(color="black", width=3)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[0, 0.25], y=[253, 253], mode="lines", line=dict(color="#8B0000", width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=dd, y=[d.inflation_cost(x) for x in dd], mode="lines", line=dict(color=ORANGE, width=3)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[0.70, 0.70, 0.9], y=[d.inflation_cost(0.7), 0, 0], mode="lines",
                         line=dict(color=GREY, width=3)), row=1, col=1)
pts = [(0.4, 160), (0.5, 119), (0.7, 65)]
fig.add_trace(go.Scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers+text",
                         text=[f"{c} at {x:.2f} m" for x, c in pts], textposition="top right",
                         textfont=dict(size=16), marker=dict(size=9, color=ORANGE)), row=1, col=1)
for x0, txt in ((-0.025, "254<br>inside"), (0.125, "253: within the<br>robot's radius"), (0.81, "0: free")):
    fig.add_annotation(x=x0, y=40 if x0 > 0.7 else 200, xref="x", yref="y", text=txt, showarrow=False,
                       font=dict(size=15, color=GREY))
fig.update_xaxes(title_text="distance d from the cell's centre to the nearest obstacle (m)", range=[-0.06, 0.92],
                 row=1, col=1, showgrid=False)
fig.update_yaxes(title_text="cost", range=[-10, 275], row=1, col=1, showgrid=False)

xs = cm.ox + (np.arange(cm.n) + 0.5) * cm.res
ys = cm.oy + (np.arange(cm.n) + 0.5) * cm.res
scale = [[0, "#FFFFFF"], [0.25, "#FDE0C5"], [0.6, "#F58518"], [0.9, "#B33A00"], [0.995, "#8B0000"], [1, "#000000"]]
fig.add_trace(go.Heatmap(x=xs, y=ys, z=cm.cost, zmin=0, zmax=254, colorscale=scale,
                         colorbar=dict(title=dict(text="cost", side="right"), len=0.62, y=0.33, thickness=18)),
              row=2, col=1)
t = list(d.TABLE) + [d.TABLE[0]]
fig.add_trace(go.Scatter(x=[p[0] for p in t], y=[p[1] for p in t], mode="lines", line=dict(color="#555555", width=2)),
              row=2, col=1)
tt = np.linspace(0, 2 * math.pi, 60)
fig.add_trace(go.Scatter(x=d.PERSON[0] + d.PERSON_R * np.cos(tt), y=d.PERSON[1] + d.PERSON_R * np.sin(tt),
                         mode="lines", line=dict(color="#C2185B", width=2)), row=2, col=1)
rd.plan(fig, o["local"], rc=(2, 1), color="#333333")
rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE, rc=(2, 1), fill="rgba(0,0,0,0)")
rd.arcs(fig, [rec["traj"]], BLUE, rc=(2, 1), width=4)
fig.add_annotation(x=end[0], y=end[1], xref="x2", yref="y2", text="end of the chosen rollout: cost 160",
                   ax=-150, ay=-70, font=dict(size=16, color=BLUE), arrowcolor=BLUE, bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=d.PERSON[0], y=d.PERSON[1] + 0.27, xref="x2", yref="y2", text="person", showarrow=False,
                   font=dict(size=16, color="#C2185B"), bgcolor="rgba(255,255,255,0.8)")
fig.update_xaxes(range=[cm.ox, cm.ox + 3], row=2, col=1, title_text="x (m)", showgrid=False)
fig.update_yaxes(range=[cm.oy, cm.oy + 3], row=2, col=1, title_text="y (m)", scaleanchor="x2", showgrid=False)
fig.update_layout(template="simple_white", font=FONT, width=820, height=1250, showlegend=False,
                  margin=dict(l=90, r=20, t=20, b=70))
fig.write_image("costmap.png", scale=2)
