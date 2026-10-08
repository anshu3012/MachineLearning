"""Command "drive 1 m straight", end position spread with standard deviation 0.1 m. The density is highest at 1 m
(3.99 per m); at 1.1 m it is 2.42 per m and at 0.99 m 3.97 per m. Run: python one_meter.py -> one_meter.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
s = 0.1
f = lambda x: np.exp(-0.5 * ((x - 1) / s) ** 2) / np.sqrt(2 * np.pi * s * s)
assert abs(f(1.1) - 2.420) < 1e-3 and abs(f(0.99) - 3.970) < 1e-3
x = np.linspace(0.6, 1.4, 400)
fig = go.Figure(go.Scatter(x=x, y=f(x), mode="lines", line=dict(color=BLUE, width=3)))
xs = np.linspace(1.095, 1.105, 5)
fig.add_trace(go.Scatter(x=[1.09, 1.09, 1.11, 1.11], y=[0, f(1.09), f(1.11), 0], fill="toself", mode="lines",
                         line=dict(color=RED, width=1), fillcolor="rgba(228,87,86,0.35)"))
for q, lab, pos in [(1.0, "1.00 m: 3.99 per m", "top"), (0.99, "0.99 m: 3.97 per m", "left"),
                    (1.1, "1.10 m: 2.42 per m", "right")]:
    fig.add_trace(go.Scatter(x=[q], y=[f(q)], mode="markers", marker=dict(size=11, color=RED)))
fig.add_annotation(x=1.0, y=f(1.0) + 0.25, text="1.00 m: 3.99 per m", showarrow=False, font=dict(size=18))
fig.add_annotation(x=0.985, y=f(0.99), text="0.99 m: 3.97 per m", showarrow=False, xanchor="right",
                   font=dict(size=18))
fig.add_annotation(x=1.12, y=f(1.1) + 0.1, text="1.10 m: 2.42 per m", showarrow=False, xanchor="left",
                   font=dict(size=18))
fig.add_annotation(x=1.1, y=0.7, ax=1.22, ay=1.5, axref="x", ayref="y", text="area 1.09 to 1.11 m:<br>probability 0.048",
                   showarrow=True, arrowhead=2, xanchor="left", font=dict(size=17, color=RED))
fig.update_xaxes(title="end position x (m)", range=[0.6, 1.4], dtick=0.1)
fig.update_yaxes(title="density (per m)", range=[0, 4.6])
fig.update_layout(template="simple_white", width=900, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70),
                  title=dict(text='start 0 m, command "drive 1 m": density of the end position', x=0.5,
                             font=dict(size=22)))
fig.write_image(here / "one_meter.png")
