"""Probability and log odds: l = ln(p / (1 - p)). p = 0.5 -> 0; 0.75 -> 1.10; 0.9 -> 2.20; 1/3 -> -0.69. Probabilities
near 0 and 1 are squeezed together; log odds spread them over the whole number line.
Run: python logodds.py -> logodds.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREEN, GREY, RED

here = Path(__file__).parent
p = np.linspace(0.005, 0.995, 400)
l = np.log(p / (1 - p))
fig = go.Figure(go.Scatter(x=l, y=p, mode="lines", line=dict(color=BLUE, width=4)))
pts = [(0.5, "p = 0.5 → l = 0", GREY), (0.75, "p = 0.75 → l = 1.10", GREEN), (0.9, "p = 0.9 → l = 2.20", GREEN),
       (1 / 3, "p = 0.33 → l = −0.69", RED)]
for pv, text, color in pts:
    lv = np.log(pv / (1 - pv))
    fig.add_trace(go.Scatter(x=[lv], y=[pv], mode="markers", marker=dict(size=14, color=color)))
    fig.add_annotation(x=lv, y=pv, text=text, showarrow=False, xanchor="left" if lv >= 0 else "right",
                       xshift=12 if lv >= 0 else -12, yshift=16 if lv < 0 else -16, font=dict(size=19, color=color))
fig.update_xaxes(title="log odds l", range=[-5.5, 5.5], dtick=1, zeroline=True)
fig.update_yaxes(title="probability p", range=[0, 1], dtick=0.25)
fig.update_layout(template="simple_white", width=950, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(here / "logodds.png", scale=1.5)
