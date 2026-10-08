"""The likelihood field of the room seen from straight above, as a colour map (same colours as the surface):
bright = an endpoint here is likely, dark = unlikely. The 12 endpoints of the scan at pose A are drawn as red
dots: 11 sit on bright ridges, the person's endpoint (3, 2) sits on the dark floor. Run -> field_map.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from fieldmodel import POSE_A, distance_grid, endpoints, field, make_map, scan_A
from gifkit import FONT, RED
from roomdraw import robot_marker

here = Path(__file__).parent
occ, xs, ys = make_map()
F = field(distance_grid(occ))
k = 2
fig = go.Figure(go.Heatmap(x=xs[::k], y=ys[::k], z=F[::k, ::k], colorscale="Viridis", zmin=0, zmax=3.61,
                           colorbar=dict(title="per m")))
px, py = endpoints(POSE_A, scan_A())
fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(color=RED, size=12, line=dict(color="white", width=2))))
fig.add_trace(robot_marker(POSE_A, color="white"))
fig.add_annotation(x=3.0, y=2.25, text="person's endpoint", showarrow=False, font=dict(color="white", size=18))
fig.update_layout(template="simple_white", width=900, height=680, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=20, b=60))
fig.update_xaxes(title="x (m)", range=[-0.2, 5.2], dtick=1, scaleanchor="y")
fig.update_yaxes(title="y (m)", range=[-0.2, 4.2], dtick=1)
fig.write_image(here / "field_map.png")
