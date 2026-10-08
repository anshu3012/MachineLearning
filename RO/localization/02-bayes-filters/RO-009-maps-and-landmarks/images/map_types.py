"""The same room as a feature-based map (a list of landmarks: position and signature) and as a location-based grid map
(every 0.1 m cell marked occupied or free). Run: python map_types.py -> map_types.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY
from plotly.subplots import make_subplots
from roommap import H, POLES, W, bitmap

here = Path(__file__).parent
PINK = "#E377C2"
cell = 0.1
B = bitmap(cell, sub=4)
ny, nx = B.shape
assert (nx, ny) == (70, 40)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=["feature-based map: 2 landmarks, 6 numbers",
                                    f"location-based (grid) map: {nx} × {ny} = {nx * ny} cells"])
for name, (px, py), col in [("pink", POLES["pink"], PINK), ("green", POLES["green"], GREEN)]:
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers+text", marker=dict(size=18, color=col),
                             text=[f"({px:g}, {py:g}), {name}"], textposition="middle right" if px < 3 else "top center",
                             textfont=dict(size=17, color=col)), 1, 1)
fig.add_shape(type="rect", x0=0, y0=0, x1=W, y1=H, line=dict(color=GREY, dash="dot"), fillcolor="rgba(0,0,0,0)", row=1, col=1)
# grid map: border walls drawn as occupied cells too
G = B.copy()
G[0, :] = G[-1, :] = G[:, 0] = G[:, -1] = 1
G[-1, 30:42] = 0                                            # door gap 3.0-4.2 m
fig.add_trace(go.Heatmap(z=G, x0=cell / 2, dx=cell, y0=cell / 2, dy=cell, colorscale=[[0, "white"], [1, "black"]],
                         showscale=False, xgap=0.5, ygap=0.5), 1, 2)
for c in (1, 2):
    fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", row=1, col=c)
    fig.update_yaxes(range=[-0.2, 4.2], dtick=1, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
fig.update_yaxes(title="y (m)", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=470, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70))
fig.update_annotations(font_size=20)
fig.write_image(here / "map_types.png")
print("occupied cells:", int(G.sum()), "of", G.size)
