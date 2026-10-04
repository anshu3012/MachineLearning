"""First-layer weights of a dense network against first-layer filters of a CNN, side by side.
Left: the 784 incoming weights of 16 hidden nodes of the MNIST dense network of Note 1012 (784-128-10), each drawn
as a 28 x 28 picture (data/mlp_hidden_weights.npy, copied from that Note's extras.json). Right: 16 of ResNet50's
7 x 7 first-layer filters (data/resnet50_filters.npy). Plotly image grid: a still comparison of two sets of pictures.
The contrast (dense weights look almost random, not like edges) is the one in 3Blue1Brown,
"Gradient descent, how neural networks learn" (14:00-15:00); the pictures are our own networks' weights.
Run: python mlp_vs_cnn.py -> mlp_vs_cnn.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
data = here.parent / "data"
mlp = np.load(data / "mlp_hidden_weights.npy").astype(float)             # (16, 28, 28)
res = np.load(data / "resnet50_filters.npy").astype(float)               # (7, 7, 3, 64), already scaled to 0..1
assert mlp.shape == (16, 28, 28) and res.shape == (7, 7, 3, 64) and 0 <= res.min() and res.max() <= 1


def mosaic(tiles, gap):
    """16 equal (h, w, 3) uint8 tiles -> one 4 x 4 mosaic with white gaps."""
    h, w = tiles[0].shape[:2]
    out = np.full((4 * (h + gap) - gap, 4 * (w + gap) - gap, 3), 255, np.uint8)
    for i, t in enumerate(tiles):
        r, c = divmod(i, 4)
        out[r * (h + gap):r * (h + gap) + h, c * (w + gap):c * (w + gap) + w] = t
    return out


lim = np.abs(mlp).max()


def red_blue(wt):
    """Blue for positive, red for negative, white for 0 (as in Note 1012)."""
    t = np.clip(wt / lim, -1, 1)[..., None]
    blue, red = np.array([33, 102, 172]), np.array([178, 24, 43])
    rgb = np.where(t > 0, 255 + (blue - 255) * t, 255 + (red - 255) * (-t))
    return np.kron(rgb, np.ones((4, 4, 1))).astype(np.uint8)


left = mosaic([red_blue(m) for m in mlp], 8)
right = mosaic([np.kron(res[..., i], np.ones((16, 16, 1))) * 255 for i in range(16)], 8).astype(np.uint8)
fig = make_subplots(1, 2, horizontal_spacing=0.05, subplot_titles=(
    "dense network (MNIST): 16 hidden nodes, 28 × 28 weights each",
    "CNN (ResNet50): 16 first-layer filters, 7 × 7 each"))
fig.add_trace(go.Image(z=left), 1, 1)
fig.add_trace(go.Image(z=right), 1, 2)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1150, height=600, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "mlp_vs_cnn.png", scale=2)
