"""200 readings of a range sensor aimed at a wall 2.00 m away: 190 with sensor noise (standard deviation 3 cm),
10 taken while a person walked past (0.6 to 1.2 m). Seeded. Run: python wall_readings.py -> wall_readings.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
rng = np.random.default_rng(7)
wall = rng.normal(2.0, 0.03, 190)
person = rng.uniform(0.6, 1.2, 10)
assert abs(wall.min() - 1.924) < 1e-3 and abs(wall.max() - 2.067) < 1e-3
top = np.histogram(wall, bins=np.arange(0.5, 2.3001, 0.02))[0].max()
fig = go.Figure()
fig.add_trace(go.Histogram(x=wall, xbins=dict(start=0.5, end=2.3, size=0.02), marker_color=BLUE, name="wall"))
fig.add_trace(go.Histogram(x=person, xbins=dict(start=0.5, end=2.3, size=0.02), marker_color=RED, name="person"))
fig.add_vline(x=2.0, line=dict(color=GREY, dash="dash", width=2))
fig.add_annotation(x=2.0, y=top + 4, text="true distance 2.00 m", showarrow=False, xanchor="right", xshift=-8,
                   font=dict(size=18, color=GREY))
fig.add_annotation(x=0.9, y=6, text="10 readings: a person<br>walked past", showarrow=False, font=dict(size=18, color=RED))
fig.add_annotation(x=1.55, y=22, text="190 readings: the wall,<br>spread by sensor noise", showarrow=False,
                   font=dict(size=18, color=BLUE))
fig.update_layout(template="simple_white", width=900, height=520, font=FONT, showlegend=False, barmode="overlay",
                  margin=dict(l=80, r=30, t=90, b=70),
                  title=dict(text="200 readings of one wall from one spot", x=0.5, font=dict(size=22)))
fig.update_xaxes(title="reading (m)", range=[0.5, 2.25])
fig.update_yaxes(title="number of readings", range=[0, top + 8])
fig.write_image(here / "wall_readings.png")
