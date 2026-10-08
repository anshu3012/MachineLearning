"""The likelihood field along one line across the room, y = 0.9 m: it passes the left wall (x = 0), the box
(x = 3.6 to 4.2) and the right wall (x = 5). Top: distance to the nearest obstacle. Bottom: the field value,
0.9 N(d; 0, 0.1^2) + 0.1/5. Run -> field_slice.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fieldmodel import distance_grid, field, lookup, make_map
from gifkit import BLUE, FONT, GREEN, GREY

here = Path(__file__).parent
occ, _, _ = make_map()
D = distance_grid(occ)
F = field(D)
xs = np.arange(-0.15, 5.15, 0.005)
ys = np.full_like(xs, 0.9)
d, f = lookup(D, xs, ys), lookup(F, xs, ys)
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.14, shared_xaxes=True,
                    subplot_titles=["distance to the nearest obstacle (m)", "likelihood field: density of an endpoint here (per m)"])
fig.add_trace(go.Scatter(x=xs, y=d, mode="lines", line=dict(color=BLUE, width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=xs, y=f, mode="lines", line=dict(color=GREEN, width=3)), row=2, col=1)
for r in (1, 2):
    for x0, x1, lab in ((-0.2, 0, "wall"), (3.6, 4.2, "box"), (5, 5.2, "wall")):
        fig.add_vrect(x0=x0, x1=x1, fillcolor=GREY, opacity=0.3, line_width=0, row=r, col=1)
        if r == 1:
            fig.add_annotation(x=(x0 + x1) / 2, y=1.65, text=lab, showarrow=False, font_size=17, row=1, col=1)
fig.add_hline(y=0.02, line=dict(color=GREY, dash="dot"), row=2, col=1)
fig.add_annotation(x=2.0, y=0.4, text="far from everything: floor 0.1 / 5 = 0.02", showarrow=False, font_size=17, row=2, col=1)
fig.update_yaxes(range=[0, 1.8], row=1, col=1)
fig.update_yaxes(range=[0, 4], row=2, col=1)
fig.update_xaxes(range=[-0.2, 5.2], dtick=0.5, row=1, col=1)
fig.update_xaxes(title="x (m) along the line y = 0.9 m", range=[-0.2, 5.2], dtick=0.5, row=2, col=1)
fig.update_layout(template="simple_white", width=1000, height=620, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=20)
fig.write_image(here / "field_slice.png")
