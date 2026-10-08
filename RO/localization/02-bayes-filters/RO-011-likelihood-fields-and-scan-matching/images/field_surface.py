"""The likelihood field of the room as a 3D surface: height = density of a beam endpoint at that spot (per m).
Ridges stand along the walls and around the box; the flat floor (0.02) lies everywhere far from obstacles.
Seen tilted from above, with the same colour scale as the flat map that follows. Run -> field_surface.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from fieldmodel import distance_grid, field, make_map
from gifkit import FONT

here = Path(__file__).parent
occ, xs, ys = make_map()
F = field(distance_grid(occ))
k = 5                                                        # draw every 5th cell (5 cm) to keep the file small
fig = go.Figure(go.Surface(x=xs[::k], y=ys[::k], z=F[::k, ::k], colorscale="Viridis", cmin=0, cmax=3.61,
                           colorbar=dict(title="per m", len=0.7)))
fig.update_layout(template="simple_white", width=1000, height=700, font=FONT, margin=dict(l=0, r=0, t=10, b=0),
                  scene=dict(zaxis=dict(title="density", range=[0, 4], dtick=2, tickfont=dict(size=14)),
                             xaxis=dict(title="x (m)", tickfont=dict(size=14)), yaxis=dict(title="y (m)", tickfont=dict(size=14)),
                             aspectratio=dict(x=1.25, y=1, z=0.45),
                             camera=dict(eye=dict(x=0.9, y=-1.5, z=1.25))))
fig.write_image(here / "field_surface.png")
