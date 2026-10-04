"""One hidden node as an edge detector. Its 784 weights, drawn as a 28 x 28 grid, are set by hand (not trained):
+1 on a horizontal strip near the top (rows 8-9, columns 8-19), -1 on the two rows above and the two rows below, 0
elsewhere. The weighted sum is large for an image with a horizontal stroke on the strip (a 7) and negative for one
without (a 1). Images: the first 7 and the first 1 of the MNIST test set (data/edge_digits.npz), pixels scaled to 0-1.
Idea after 3Blue1Brown, "But what is a neural network?". Plotly, because the picture is pixel grids."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
X = np.load(HERE.parent / "data" / "edge_digits.npz")["images"] / 255
W = np.zeros((28, 28))
W[8:10, 8:20] = 1
W[6:8, 8:20] = -1
W[10:12, 8:20] = -1
sums = [(W * im).sum() for im in X]
print("weighted sums (7, 1):", [round(float(v), 2) for v in sums])
assert sums[0] > 10 and sums[1] < 0, sums

titles = ["<b>The node's weights</b><br>green +1, red −1, white 0",
          f"<b>A 7</b><br>weighted sum {sums[0]:.1f}".replace("-", "−"),
          f"<b>A 1</b><br>weighted sum {sums[1]:.1f}".replace("-", "−")]
fig = make_subplots(rows=1, cols=3, subplot_titles=titles, horizontal_spacing=0.05)
fig.add_heatmap(z=W[::-1], colorscale=[[0, "#E45756"], [0.5, "#FFFFFF"], [1, "#54A24B"]], zmin=-1, zmax=1,
                showscale=False, xgap=1, ygap=1, row=1, col=1)
for k, im in enumerate(X):
    fig.add_heatmap(z=im[::-1], colorscale="Greys", showscale=False, row=1, col=k + 2)
    # outline of the positive strip (rows 8-9 from the top -> y 18 to 20 after the flip)
    fig.add_shape(type="rect", x0=7.5, x1=19.5, y0=17.5, y1=19.5, line=dict(color="#54A24B", width=3), fillcolor="rgba(0,0,0,0)", row=1, col=k + 2)
    fig.add_shape(type="rect", x0=7.5, x1=19.5, y0=15.5, y1=21.5, line=dict(color="#E45756", width=2, dash="dot"), fillcolor="rgba(0,0,0,0)",
                  row=1, col=k + 2)
fig.add_shape(type="rect", x0=-0.5, x1=27.5, y0=-0.5, y1=27.5, line=dict(color="#999", width=1), fillcolor="rgba(0,0,0,0)", row=1, col=1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=22))
fig.update_layout(template="simple_white", width=1200, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=10, r=10, t=90, b=10))
fig.write_image(HERE / "edge_neuron.png", scale=2)
