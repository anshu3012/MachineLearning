"""A real photo and the strength of its vertical and horizontal edges (absolute feature-map values), Plotly."""
from pathlib import Path
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
photo = np.array(Image.open(here.parent / "data" / "photo.png"), dtype=float)
m = np.load(here.parent / "data" / "photo_maps.npz")
titles = ("photo (0 = black, 255 = white)", "vertical-edge filter", "horizontal-edge filter")
fig = make_subplots(1, 3, subplot_titles=titles, horizontal_spacing=0.03)
top = np.percentile(np.abs(np.concatenate([m["V"].ravel(), m["H"].ravel()])), 99)
for k, (z, zmax) in enumerate(((photo, 255), (np.abs(m["V"]), top), (np.abs(m["H"]), top)), start=1):
    fig.add_trace(go.Heatmap(z=z, colorscale="gray" if k == 1 else "gray_r", zmin=0, zmax=zmax, showscale=False), 1, k)
fig.update_xaxes(visible=False, scaleanchor="y")
for k in (1, 2, 3):
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1200, height=450, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "edges_photo.png", scale=2)
fig.write_image(here / "edges_photo.pdf")
