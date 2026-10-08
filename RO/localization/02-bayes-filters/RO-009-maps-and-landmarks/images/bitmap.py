"""Bitmaps of the room's furniture (table, cabinet, poles) at cell sizes 0.5 m and 0.1 m: a cell is 1 (black) if it
contains at least one obstacle point (LaValle §3.1.3). Outlines: the exact polygons. Run: python bitmap.py -> bitmap.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, PURPLE, RED
from plotly.subplots import make_subplots
from roommap import CAB, H, TABLE, W, bitmap

here = Path(__file__).parent
cases = [(0.5, bitmap(0.5)), (0.1, bitmap(0.1, sub=4))]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=[f"cells of {c} m: {B.size} cells, {B.sum()} black" for c, B in cases])
for k, (c, B) in enumerate(cases, start=1):
    fig.add_trace(go.Heatmap(z=B, x0=c / 2, dx=c, y0=c / 2, dy=c, colorscale=[[0, "white"], [1, "#333"]],
                             showscale=False, xgap=1, ygap=1), 1, k)
    px, py = zip(*(TABLE + [TABLE[0]]))
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color=BLUE, width=3)), 1, k)
    cx = [5.6, 7, 7, 6.4, 6.4, 5.6, 5.6]
    cy = [4, 4, 2.4, 2.4, 3.4, 3.4, 4]
    fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=PURPLE, width=3)), 1, k)
    fig.update_xaxes(range=[0, W], dtick=1, title="x (m)", row=1, col=k, showgrid=False)
    fig.update_yaxes(range=[0, H], dtick=1, scaleanchor=f"x{k if k > 1 else ''}", row=1, col=k)
fig.update_yaxes(title="y (m)", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=470, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70))
fig.update_annotations(font_size=20)
fig.write_image(here / "bitmap.png")
print([(c, B.size, int(B.sum()), round(B.sum() * c * c, 2)) for c, B in cases])
