"""Figures for the gradient boosting maths Note (Plotly):
additive.png  - y = x + sin(x) built from its two parts;
regions.png   - the first tree on the three startups: two terminal regions on R&D spend and their leaf values."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
BLUE, RED, GREEN, GREY, ORANGE = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B", "#F58518"

x = np.linspace(-10, 10, 500)
fig = make_subplots(1, 3, subplot_titles=["y = x", "y = sin(x)", "y = x + sin(x): the sum"], horizontal_spacing=0.06)
for c, (yy, col) in enumerate([(x, GREEN), (np.sin(x), ORANGE), (x + np.sin(x), RED)], start=1):
    fig.add_trace(go.Scatter(x=x, y=yy, mode="lines", line=dict(color=col, width=3, simplify=False), showlegend=False), 1, c)
fig.update_yaxes(range=[-11, 11])
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1400, height=480, font=FONT, margin=dict(l=40, r=20, t=50, b=40))
fig.write_image(HERE / "additive.png", scale=2)
fig.write_image(HERE / "additive.pdf")

d = pd.read_csv(HERE.parent / "data" / "startups3.csv")
res = d.profit - d.profit.mean()
cut = (28.66 + 100.67) / 2
fig = go.Figure()
fig.add_vrect(x0=0, x1=cut, fillcolor=BLUE, opacity=0.12, line_width=0)
fig.add_vrect(x0=cut, x1=180, fillcolor=GREEN, opacity=0.12, line_width=0)
fig.add_vline(x=cut, line=dict(color=GREY, dash="dash", width=2))
fig.add_trace(go.Scatter(x=d.rd, y=res, mode="markers+text", marker=dict(color=BLUE, size=14),
                         text=[f"startup {i + 1}: r = {r:.2f}" for i, r in enumerate(res)],
                         textposition=["bottom left", "bottom center", "top right"], textfont=dict(size=18),
                         showlegend=False))
for x0, x1, v, name in [(0, cut, res[2], "R<sub>11</sub>"), (cut, 180, (res[0] + res[1]) / 2, "R<sub>21</sub>")]:
    fig.add_trace(go.Scatter(x=[x0, x1], y=[v, v], mode="lines", line=dict(color=RED, width=4), showlegend=False))
    fig.add_annotation(x=(x0 + x1) / 2, y=62, text=f"region {name}<br>leaf value {v:.2f}", showarrow=False,
                       font=dict(size=19))
fig.add_annotation(x=cut, y=-68, text=f"R&D spend = {cut:.2f}", showarrow=False, xshift=70, font=dict(size=17))
fig.update_xaxes(title="R&D spend (thousands)", range=[0, 180])
fig.update_yaxes(title="pseudo-residual r (thousands)", range=[-75, 75], zeroline=True)
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(HERE / "regions.png", scale=2)
fig.write_image(HERE / "regions.pdf")
