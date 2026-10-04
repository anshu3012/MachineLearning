"""The bag of 3 red and 2 green balls read both ways (Plotly). Left, probability: with p = 2/5 known, one draw is red
with probability 0.6 and green with 0.4. Right, likelihood: with five green draws observed, L(p) = p^5 for every
candidate share p of green balls; L(2/5) = 0.010 and L(4/5) = 0.328."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
assert round(0.4 ** 5, 3) == 0.010 and round(0.8 ** 5, 3) == 0.328
fig = make_subplots(1, 2, column_widths=[0.38, 0.62], horizontal_spacing=0.12,
                    subplot_titles=["probability: p = 2/5 known, one draw", "likelihood: 5 green observed, p varies"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Bar(x=["red", "green"], y=[0.6, 0.4], marker_color=[RED, GREEN], text=["0.6", "0.4"],
                     textposition="outside", textfont=dict(size=22)), 1, 1)
p = np.linspace(0, 1, 201)
fig.add_trace(go.Scatter(x=p, y=p ** 5, mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
for v, c, t in ((0.4, ORANGE, "L(2/5) = 0.010"), (0.8, GREEN, "L(4/5) = 0.328")):
    fig.add_trace(go.Scatter(x=[v, v], y=[0, v ** 5], mode="lines+markers", line=dict(color=c, width=4), marker=dict(size=[0, 13])), 1, 2)
    fig.add_annotation(x=v, y=v ** 5, text=t, xanchor="right", xshift=-10, yshift=12, showarrow=False, font=dict(size=20, color=c),
                       row=1, col=2)
fig.update_yaxes(title="probability", range=[0, 0.75], row=1, col=1)
fig.update_xaxes(title="candidate share of green balls, p", row=1, col=2)
fig.update_yaxes(title="likelihood L(p) = p⁵", range=[0, 1.05], row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "bag_both.png", scale=2)
