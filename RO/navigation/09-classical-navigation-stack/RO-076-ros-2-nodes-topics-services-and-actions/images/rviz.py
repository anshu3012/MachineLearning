"""Still: a sketch of what RViz draws for the room robot at 2.4 s, the moment the person steps in, made with Plotly
from the same data the topics carry: the map (/map, grey cells), the laser scan (/scan, red dots: 682 readings, the
nearest straight ahead 0.72 m away, on the person), the global plan (grey dashed), the local plan (/local_plan,
orange, bent left round the person) and the robot's footprint (blue disk). The person is not in the map: the
robot knows of them only through the red dots. Run -> rviz.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import roskit as rk
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
o = rk.L[24]
s = rk.scan(2.4)
x, y, th = o["x"][:3]
keep = s["ranges"] < rk.RMAX - 1e-6
px = x + s["ranges"][keep] * np.cos(th + s["bearings"][keep])
py = y + s["ranges"][keep] * np.sin(th + s["bearings"][keep])
nx, ny = rk.MAP_CELLS
xc = (np.arange(nx) + 0.5) * rk.MAP_RES
yc = (np.arange(ny) + 0.5) * rk.MAP_RES
X, Y = np.meshgrid(xc, yc)
D = np.min([f(X, Y) for f in bk.obstacles(None)], axis=0)
G = (D <= rk.MAP_RES / 2 + 1e-9).astype(float)
G[G == 0] = np.nan
b = np.degrees(s["bearings"])
assert round(float(np.min(np.where(np.abs(b) < 30, s["ranges"], 99))), 2) == 0.72
fig = go.Figure()
fig.add_trace(go.Heatmap(z=G, x=xc, y=yc, colorscale=[[0, "#9A9A9A"], [1, "#9A9A9A"]], showscale=False))
fig.add_trace(go.Scatter(x=rk.ROUTE_PTS[:, 0], y=rk.ROUTE_PTS[:, 1], mode="lines", line=dict(color=GREY, width=3,
                         dash="dash")))
rd.band(fig, o["P"], ORANGE, size=8)
fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(size=4, color=RED)))
rd.robot(fig, x, y, th, BLUE)
for txt, yy, col in (("map: grey cells", 0.62, "#777777"), ("laser scan: red dots", 0.84, RED),
                     ("global plan: grey dashed", 1.06, GREY), ("local plan: orange", 1.28, ORANGE),
                     ("robot: blue disk", 1.50, BLUE)):
    fig.add_annotation(x=1.35, y=yy + 2.1, text=txt, showarrow=False, xanchor="left", font=dict(size=20, color=col),
                       bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=2.95, y=2.42, text="person: only<br>the red dots", showarrow=False, xanchor="left",
                   font=dict(size=18, color=RED), bgcolor="rgba(255,255,255,0.85)")
rd.axes(fig)
fig.update_layout(template="simple_white", font=FONT, width=760, height=950, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "rviz.png", scale=2)
