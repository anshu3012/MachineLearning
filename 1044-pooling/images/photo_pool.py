"""Edge map of a photo (vertical-edge filter + ReLU), then 4x4 max pooling and 4x4 average pooling,
same colour scale (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "photo_pool.npz")
top = np.percentile(d["E"], 99)
fig = make_subplots(1, 3, horizontal_spacing=0.03,
                    subplot_titles=("edge map, 254 x 254", "4 x 4 max pooling, 63 x 63", "4 x 4 average pooling, 63 x 63"))
for k, z in enumerate((d["E"], d["Emax"], d["Eavg"]), start=1):
    fig.add_trace(go.Heatmap(z=z, colorscale="gray_r", zmin=0, zmax=top, showscale=False), 1, k)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_xaxes(visible=False)
fig.update_layout(template="simple_white", width=1200, height=450, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "photo_pool.png", scale=2)
fig.write_image(here / "photo_pool.pdf")
