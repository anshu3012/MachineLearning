"""1000 simulated readings of the beam that faces a wall 3 m away (z_max = 5 m), as counts per 0.05 m bin.
Left: all counts. Right: the same bars with the axis cut at 25, so the small groups show. Run -> wall_data.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from beammodel import load
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE
from histkit import EDGES, counts

here = Path(__file__).parent
z = load()
c = counts(z)
mid = (EDGES[:-1] + EDGES[1:]) / 2
fig = make_subplots(rows=1, cols=2, subplot_titles=["all 1000 readings", "zoom: counts up to 25"], horizontal_spacing=0.1)
for col in (1, 2):
    fig.add_trace(go.Bar(x=mid, y=c, width=0.05, marker=dict(color=BLUE, line=dict(width=0))), row=1, col=col)
    fig.update_xaxes(title="reading z (m)", range=[0, 5.1], dtick=1, row=1, col=col)
fig.update_yaxes(title="readings per 0.05 m bin", range=[0, 330], row=1, col=1)
fig.update_yaxes(range=[0, 25], row=1, col=2)
notes = [(0.45, 23, "short readings", ORANGE, "left"), (4.1, 6, "random readings", GREEN, "center"),
         (4.95, 18, "max range: 47", PURPLE, "right"), (2.85, 15, "near the wall<br>(cut off)", BLUE, "right")]
for x, y, t, col, anc in notes:
    fig.add_annotation(x=x, y=y, text=t, showarrow=False, font=dict(color=col, size=18), xref="x2", yref="y2", xanchor=anc)
fig.update_layout(template="simple_white", width=1150, height=520, font=FONT, showlegend=False, bargap=0,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=21)
fig.write_image(here / "wall_data.png", scale=1)
assert len(z) == 1000 and (z == 5.0).sum() == 47
