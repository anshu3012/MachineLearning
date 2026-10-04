"""How a colour image is stored (section 3.2): scikit-learn's sample photo flower.jpg (427 x 640 x 3) and its red,
green and blue channels, each a grid of numbers from 0 to 255, with the numbers of one 4 x 4 patch written out.
Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_sample_image

HERE = Path(__file__).parent
img = load_sample_image("flower.jpg")
assert img.shape == (427, 640, 3) and img.dtype == np.uint8
R0, C0 = 200, 300                                       # the patch whose numbers are shown
patch = img[R0:R0 + 4, C0:C0 + 4]
fig = make_subplots(rows=2, cols=4, row_heights=[0.62, 0.38], vertical_spacing=0.08, horizontal_spacing=0.03,
                    subplot_titles=("the photo (427 × 640 × 3)", "red channel", "green channel", "blue channel",
                                    "", "red: 4 × 4 patch", "green: 4 × 4 patch", "blue: 4 × 4 patch"))
fig.add_trace(go.Image(z=img), 1, 1)
fig.add_shape(type="rect", x0=C0 - 8, x1=C0 + 12, y0=R0 - 8, y1=R0 + 12, line=dict(color="yellow", width=3), row=1, col=1)
for k, (name, scale) in enumerate((("red", "Reds"), ("green", "Greens"), ("blue", "Blues"))):
    fig.add_trace(go.Heatmap(z=img[:, :, k], colorscale=[[0, "black"], [1, ["red", "lime", "blue"][k]]], zmin=0, zmax=255,
                             showscale=False, hoverinfo="skip"), 1, k + 2)
    fig.add_trace(go.Heatmap(z=patch[:, :, k], colorscale=[[0, "black"], [1, ["red", "lime", "blue"][k]]], zmin=0,
                             zmax=255, showscale=False, text=patch[:, :, k], texttemplate="%{text}",
                             textfont=dict(size=17, color="white"), hoverinfo="skip"), 2, k + 2)
for r in (1, 2):
    for c in range(1, 5):
        fig.update_xaxes(visible=False, row=r, col=c)
        fig.update_yaxes(visible=False, autorange="reversed", row=r, col=c)
for c in range(2, 5):
    fig.update_yaxes(scaleanchor=f"x{c + 4}", row=2, col=c)
    fig.update_yaxes(scaleanchor=f"x{c}", row=1, col=c)
fig.update_xaxes(visible=False, row=2, col=1)
fig.update_layout(template="simple_white", width=1400, height=720, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(HERE / "rgb_channels.png", scale=2)
print(patch.transpose(2, 0, 1).tolist())
