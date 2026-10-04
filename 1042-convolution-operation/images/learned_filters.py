"""The 8 filters of a small CNN at their random start and after 2 epochs on MNIST, and the feature maps they give
for one digit (ReLU applied), Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "learned.npz")
rows = ("random start", "after training", "feature map")
fig = make_subplots(3, 8, horizontal_spacing=0.015, vertical_spacing=0.05, row_titles=rows,
                    subplot_titles=[f"filter {k}" for k in range(8)] + [""] * 16)
a = np.abs(np.concatenate([d["before"].ravel(), d["after"].ravel()])).max()
for k in range(8):
    fig.add_trace(go.Heatmap(z=d["before"][:, :, k], colorscale="RdBu_r", zmin=-a, zmax=a, showscale=False), 1, k + 1)
    fig.add_trace(go.Heatmap(z=d["after"][:, :, k], colorscale="RdBu_r", zmin=-a, zmax=a, showscale=False), 2, k + 1)
    fig.add_trace(go.Heatmap(z=d["maps"][:, :, k], colorscale="gray_r", zmin=0, zmax=d["maps"].max(), showscale=False), 3, k + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False, autorange="reversed")
for i in range(1, 25):
    fig.layout[f"yaxis{'' if i == 1 else i}"].scaleanchor = f"x{'' if i == 1 else i}"
fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, margin=dict(l=10, r=60, t=40, b=10))
fig.write_image(here / "learned_filters.png", scale=2)
fig.write_image(here / "learned_filters.pdf")
