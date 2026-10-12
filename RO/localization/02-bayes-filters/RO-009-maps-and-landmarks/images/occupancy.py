"""The room's 0.5 m cells two ways. Left: the bitmap, 1 (black) if a cell contains any obstacle point (LaValle §3.1.3).
Right: an occupancy grid whose number per cell is the share of the cell's area covered by the table, cabinet and
poles, which is the probability that a point picked at random in the cell lies inside an obstacle (no sensor data yet).
The shares add up to the true covered area, 5.13 m2; the 47 black cells claim 11.75 m2. Run -> occupancy.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, PURPLE
from plotly.subplots import make_subplots
from roommap import CAB, H, POLE_R, POLES, TABLE, W, bitmap
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

here = Path(__file__).parent
C = 0.5
obst = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                   + [Point(p).buffer(POLE_R, quad_segs=256) for p in POLES.values()])
nx, ny = int(round(W / C)), int(round(H / C))
S = np.array([[box(i * C, j * C, (i + 1) * C, (j + 1) * C).intersection(obst).area / C ** 2 for i in range(nx)]
              for j in range(ny)])
B = bitmap(C)
full, free = np.isclose(S, 1), np.isclose(S, 0)
part = ~full & ~free
assert B.size == 112 and B.sum() == 47 and B.sum() * C * C == 11.75
assert full.sum() == 13 and part.sum() == 23 and free.sum() == 76
assert ((B == 1) & free).sum() == 11 and ((B == 0) & ~free).sum() == 0     # 11 black cells only touch an obstacle
assert round(S.sum(), 2) == 20.51 and round(S.sum() * C * C, 2) == 5.13
assert round(20.51 * C * C, 2) == 5.13                                       # the rounded sum reproduces the area
assert round(S[3, 10], 2) == 0.50                                             # cell x 5.0-5.5 m, y 1.5-2.0 m: half covered

GREYS = [[0, "white"], [1, "#333"]]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=[f"bitmap: 0 or 1; {B.sum()} black cells = {B.sum() * C * C:.2f} m²",
                                    f"occupancy grid: share covered; {S.sum():.2f} × {C * C} m² = {S.sum() * C * C:.2f} m²"])
for k, Z in enumerate([B, S], start=1):
    fig.add_trace(go.Heatmap(z=Z, x0=C / 2, dx=C, y0=C / 2, dy=C, colorscale=GREYS, zmin=0, zmax=1, xgap=1, ygap=1,
                             showscale=k == 2, colorbar=dict(title="share", tickvals=[0, 0.5, 1], len=0.8)), 1, k)
    px, py = zip(*(TABLE + [TABLE[0]]))
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color=BLUE, width=3)), 1, k)
    fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                             line=dict(color=PURPLE, width=3)), 1, k)
    fig.update_xaxes(range=[0, W], dtick=1, title="x (m)", row=1, col=k, showgrid=False)
    fig.update_yaxes(range=[0, H], dtick=1, scaleanchor=f"x{k if k > 1 else ''}", row=1, col=k)
for j, i in zip(*np.nonzero(part)):                                          # the in-between values, written in
    fig.add_annotation(x=(i + 0.5) * C, y=(j + 0.5) * C, text=f"{S[j, i]:.2f}", showarrow=False, row=1, col=2,
                       font=dict(size=14, color="white" if S[j, i] > 0.5 else "black"))
fig.update_yaxes(title="y (m)", row=1, col=1)
fig.update_layout(template="simple_white", width=1300, height=500, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70))
for a in fig.layout.annotations[:2]:
    a.font.size = 20
fig.write_image(here / "occupancy.png")
print(f"full {full.sum()}, partial {part.sum()}, free {free.sum()}, black but share 0: {((B == 1) & free).sum()}, "
      f"sum of shares {S.sum():.2f} cells = {S.sum() * C * C:.2f} m2")
