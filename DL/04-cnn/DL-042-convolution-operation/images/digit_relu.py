"""An MNIST 0, its left-edge feature map (red positive, blue negative) and the same map after ReLU, Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
m = np.load(here.parent / "data" / "digit_maps.npz")
L = m["L"]
a = np.abs(L).max()
titles = ("digit, 28 x 28 (0 to 1)", "left-edge feature map, 26 x 26", "after ReLU")
fig = make_subplots(1, 3, subplot_titles=titles, horizontal_spacing=0.06)
fig.add_trace(go.Heatmap(z=m["digit"], colorscale="gray", zmin=0, zmax=1, showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=L, colorscale="RdBu_r", zmin=-a, zmax=a, showscale=False), 1, 2)
fig.add_trace(go.Heatmap(z=np.maximum(L, 0), colorscale="RdBu_r", zmin=-a, zmax=a, showscale=False), 1, 3)
fig.update_xaxes(visible=False)
for k in (1, 2, 3):
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1200, height=440, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "digit_relu.png", scale=2)
fig.write_image(here / "digit_relu.pdf")
