"""More particles, closer to the exact belief: the particle histogram after the second reading (weighed, before
resampling) for 20, 200 and 2000 particles, against the exact belief from a fine grid (blue line).
Run: python cloud_vs_exact.py -> cloud_vs_exact.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE
from pfsim import DOORS, LOOP, grid_belief, run

here = Path(__file__).parent
xs, _, bels = grid_belief()
Ms = [20, 200, 2000]
fig = make_subplots(rows=1, cols=3, subplot_titles=[f"M = {m} particles" for m in Ms], horizontal_spacing=0.06)
for j, M in enumerate(Ms):
    name, x, w = run(M, np.random.default_rng(3))[4]                 # "weigh 2"
    assert name == "weigh 2"
    hist, e = np.histogram(x, bins=40, range=(0, LOOP), weights=w)
    for a, b in DOORS:
        fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, xref=f"x{j + 1 if j else ''}",
                      yref=f"y{j + 1 if j else ''} domain", fillcolor=ORANGE, opacity=0.18, line_width=0, layer="below")
    fig.add_trace(go.Bar(x=(e[:-1] + e[1:]) / 2, y=hist / (e[1] - e[0]), width=e[1] - e[0], marker_color=GREY,
                         opacity=0.7), row=1, col=j + 1)
    fig.add_trace(go.Scatter(x=xs, y=bels[1], mode="lines", line=dict(color=BLUE, width=3)), row=1, col=j + 1)
fig.update_xaxes(range=[0, LOOP], dtick=2, title="position x (m)")
fig.update_yaxes(range=[0, 2.4])
fig.update_yaxes(title="belief (per m)", col=1)
fig.update_layout(template="simple_white", font=FONT, width=1350, height=480, showlegend=False, bargap=0,
                  margin=dict(l=80, r=20, t=70, b=70))
fig.update_annotations(font_size=21)
fig.write_image(here / "cloud_vs_exact.png")
