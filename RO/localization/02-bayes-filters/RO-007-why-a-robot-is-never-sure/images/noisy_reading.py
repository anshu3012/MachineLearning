"""One reading "door" from a perfect sensor and from the chapter's noisy sensor, which reads "door" with probability
0.6 at a door and 0.2 at a wall (a door cell is 3 times as likely as a wall cell: 3 x 3 + 7 x 1 = 16 shares). Run: python noisy_reading.py -> noisy_reading.png"""
from pathlib import Path

import numpy as np
from corrdraw import DOORS, panel
from gifkit import GREY
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from gifkit import BLUE, FONT, PURPLE

here = Path(__file__).parent
perfect = np.array([1 / 3 if i in DOORS else 0 for i in range(10)])
w = np.array([3.0 if i in DOORS else 1.0 for i in range(10)])
noisy = w / w.sum()
assert abs(noisy[1] - 3 / 16) < 1e-12 and abs(noisy[0] - 1 / 16) < 1e-12
fig = make_subplots(rows=1, cols=2, subplot_titles=["perfect sensor: walls crossed out", "noisy sensor: 0.6 at a door, 0.2 at a wall"],
                    horizontal_spacing=0.1)
for c, (b, col) in enumerate([(perfect, BLUE), (noisy, PURPLE)], start=1):
    fig.add_trace(go.Bar(x=np.arange(10), y=b, marker_color=col, width=0.6,
                         text=[f"{v:.4f}".rstrip("0") if v > 0 else "0" for v in b], textposition="outside", constraintext="none", cliponaxis=False,
                         textfont=dict(size=13)), 1, c)
    fig.update_xaxes(tickvals=list(range(10)), title="cell", row=1, col=c)
    fig.update_yaxes(range=[0, 0.4], row=1, col=c)
fig.update_yaxes(title="probability", row=1, col=1)
fig.update_layout(template="simple_white", width=1250, height=480, font=FONT, showlegend=False,
                  margin=dict(l=90, r=30, t=110, b=70),
                  title=dict(text='after one reading "door" (doors at cells 1, 3 and 7)', x=0.5, y=0.95,
                             font=dict(size=22)))
fig.update_annotations(font_size=19)
fig.write_image(here / "noisy_reading.png")
