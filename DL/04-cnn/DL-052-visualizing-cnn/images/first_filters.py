"""The 64 first-layer filters of VGG16 (3 x 3) and of ResNet50 (7 x 7), each shown as a tiny colour image (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
data = here.parent / "data"


def mosaic(f, scale):
    """(k, k, 3, 64) filters scaled to 0..1 -> one 8 x 8 mosaic image with white gaps."""
    k = f.shape[0]
    cell = k * scale
    out = np.full((8 * (cell + 2), 8 * (cell + 2), 3), 255, np.uint8)
    for i in range(64):
        img = np.kron(f[..., i].astype(float), np.ones((scale, scale, 1)))          # enlarge each cell
        r, c = divmod(i, 8)
        out[r * (cell + 2):r * (cell + 2) + cell, c * (cell + 2):c * (cell + 2) + cell] = (255 * img).astype(np.uint8)
    return out


vgg = np.load(data / "vgg16_filters.npy")
res = np.load(data / "resnet50_filters.npy")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=("VGG16, first layer: 64 filters of 3 x 3", "ResNet50, first layer: 64 filters of 7 x 7"))
fig.add_trace(go.Image(z=mosaic(vgg, 14)), row=1, col=1)
fig.add_trace(go.Image(z=mosaic(res, 6)), row=1, col=2)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(template="simple_white", width=950, height=500, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "first_filters.png", scale=2)
fig.write_image(here / "first_filters.pdf")
