"""One beam (330 degrees, reading 1.86 m) from poses (2, y, 0) as y moves past the box corner. Left: from y = 1.53
the beam meets the box after 1.85 m; from y = 1.52 it passes under the box and meets the floor wall after 3.05 m.
Right: the beam model's density of the reading jumps 270-fold between the two; the likelihood field changes
smoothly. Run -> edge_jump.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from beamref import mixture
from fieldmodel import distance_grid, endpoints, field, lookup, make_map, raycast
from gifkit import BLUE, FONT, GREEN, ORANGE, RED
from roomdraw import room_shapes

here = Path(__file__).parent
occ, _, _ = make_map()
F = field(distance_grid(occ))
a, z = np.radians(330), 1.86
ys = np.round(np.arange(1.40, 1.701, 0.005), 3)
beam = [mixture(z, raycast(occ, (2, y, 0), a)) for y in ys]
fld = [lookup(F, *endpoints((2, y, 0), np.array([z]), np.array([a])))[0] for y in ys]
fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.12,
                    subplot_titles=["the beam just misses, or just hits, the box", "density of the reading 1.86 m"])
room_shapes(fig, 1, 1)
for y, col in ((1.52, ORANGE), (1.53, BLUE)):
    zs = raycast(occ, (2, y, 0), a)
    fig.add_trace(go.Scatter(x=[2, 2 + zs * np.cos(a)], y=[y, y + zs * np.sin(a)], mode="lines+markers",
                             line=dict(color=col, width=3), marker=dict(size=9)), row=1, col=1)
    lx, ly, anc = ((2.0, 1.8, "left") if col == BLUE else (0.75, 0.3, "left"))
    fig.add_annotation(x=lx, y=ly, xanchor=anc, showarrow=False,
                       text=f"from y = {y}: z* = {zs:.2f} m", font=dict(color=col, size=17), row=1, col=1)
fig.update_xaxes(range=[0.6, 5.1], dtick=1, title="x (m)", row=1, col=1)
fig.update_yaxes(range=[-0.1, 2.0], dtick=0.5, title="y (m)", row=1, col=1)
fig.add_trace(go.Scatter(x=ys, y=beam, mode="lines", line=dict(color=RED, width=3, shape="hv"), name="beam model"),
              row=1, col=2)
fig.add_trace(go.Scatter(x=ys, y=fld, mode="lines", line=dict(color=GREEN, width=3), name="likelihood field"),
              row=1, col=2)
fig.add_annotation(x=1.47, y=5.3, text="beam model", showarrow=False, font=dict(color=RED, size=18), xref="x2", yref="y2")
fig.add_annotation(x=1.62, y=3.1, text="likelihood field", showarrow=False, font=dict(color=GREEN, size=18), xref="x2", yref="y2")
fig.update_xaxes(title="robot position y (m)", range=[1.4, 1.7], dtick=0.05, row=1, col=2)
fig.update_yaxes(title="density (per m)", range=[0, 6.5], row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=20)
fig.write_image(here / "edge_jump.png")
assert raycast(occ, (2, 1.53, 0), a) < 1.9 < raycast(occ, (2, 1.52, 0), a)
