"""Two leaves of the four students' residuals: residuals that agree in sign add up to a large sum and a high
similarity score; residuals that cancel give a small sum and a low score (lambda = 0). Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREY, BLACK = "#4C78A8", "#F58518", "#9A9A9A", "#222222"
leaves = {"residuals that agree": ([-2.875, -1.375], ["student 1", "student 3"], BLUE),
          "residuals that cancel": ([3.625, -1.375], ["student 2", "student 3"], ORANGE)}
S = lambda v: sum(v) ** 2 / len(v)
assert np.isclose(S([-2.875, -1.375]), 9.03, atol=0.01) and np.isclose(S([3.625, -1.375]), 2.53, atol=0.01)

fig = make_subplots(1, 2, subplot_titles=[f"{k}: S = {S(v[0]):.2f}" for k, v in leaves.items()],
                    horizontal_spacing=0.1)
for col, (name, (r, who, c)) in enumerate(leaves.items(), start=1):
    xs = who + ["sum"]
    ys = r + [sum(r)]
    fig.add_trace(go.Bar(x=xs, y=ys, marker_color=[c, c, BLACK], width=0.55, showlegend=False,
                         text=[f"{v:+.4g}" for v in ys], textposition="outside", textfont=dict(size=24)), 1, col)
    fig.add_annotation(x=1, y=-5.6, text=f"S = ({sum(r):+.3g})² / {len(r)} = {S(r):.2f}", showarrow=False,
                       font=dict(size=26), row=1, col=col)
    fig.add_hline(y=0, line=dict(color=BLACK, width=1), row=1, col=col)
fig.update_yaxes(range=[-6.4, 5], title_text="residual", col=1)
fig.update_yaxes(range=[-6.4, 5], col=2)
fig.update_annotations(font_family="Latin Modern Roman")
for a in fig.layout.annotations[:2]:
    a.font.size = 26
fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=80, r=20, t=60, b=40))
fig.write_image(HERE / "similarity.png", scale=2)
fig.write_image(HERE / "similarity.pdf")
