"""Section 4's worked example: node 1's five values z = 7, 2, 6, 3, 2 (mean 4, standard deviation 2.10) before and
after batch normalisation, on two number lines (epsilon = 0.001, as in Keras). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
z = np.array([7, 2, 6, 3, 2.0])
zh = (z - z.mean()) / np.sqrt(z.var() + 1e-3)
assert z.mean() == 4 and round(z.std(), 2) == 2.10 and round(zh[0], 2) == 1.43
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.34,
                    subplot_titles=("column z1 as computed: mean 4, standard deviation 2.10",
                                    "after (z - 4) / 2.10: mean 0, standard deviation 1"))
for r, v, col, fmt in ((1, z, BLUE, "{:g}"), (2, zh, ORANGE, "{:.2f}")):
    groups = {}
    for i, t in enumerate(v):
        groups.setdefault(round(float(t), 6), []).append(i + 1)
    xs = list(groups)
    labels = [f"obs {', '.join(map(str, groups[x]))}: {fmt.format(x)}" for x in xs]
    fig.add_scatter(x=xs, y=[0] * len(xs), mode="markers+text", text=labels, textposition="top center",
                    marker=dict(size=15, color=col), showlegend=False, row=r, col=1)
    fig.add_vline(x=v.mean(), line=dict(color="black", dash="dot", width=2), row=r, col=1)
fig.update_xaxes(range=[0.5, 8], row=1, col=1)
fig.update_xaxes(range=[-1.6, 1.9], row=2, col=1)
fig.update_yaxes(visible=False, range=[-0.4, 1.3])
fig.update_layout(template="simple_white", width=1000, height=430, font=dict(FONT, size=18), margin=dict(l=30, r=20, t=50, b=40))
fig.write_image(here / "bn_column.png", scale=2)
fig.write_image(here / "bn_column.pdf")
