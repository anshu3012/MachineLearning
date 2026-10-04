"""For six feature maps in three deep layers, the six photo patches (of 1,000 photos) that excite each map most (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
data = here.parent / "data"
grid = np.array(Image.open(data / "top_patches.jpg"))
top = pd.read_csv(data / "top_patches.csv")
order = top.drop_duplicates(["layer", "channel"])[["layer", "channel"]].values.tolist()
field = {"block3_conv3": 40, "block4_conv3": 92, "block5_conv3": 196}
fig = go.Figure(go.Image(z=grid))
tile = grid.shape[0] / len(order)
for r, (layer, ch) in enumerate(order):
    fig.add_annotation(x=-8, y=(r + 0.5) * tile, xref="x", yref="y", xanchor="right", showarrow=False,
                       text=f"{layer}, map {ch}<br><span style='font-size:13px'>patch {field[layer]} x {field[layer]} pixels</span>",
                       align="right", font=dict(size=15))
h, w = grid.shape[:2]
fig.update_xaxes(visible=False, range=[-262, w + 2])
fig.update_yaxes(visible=False, range=[h + 2, -2])
fig.update_layout(template="simple_white", width=960, height=600, font=FONT, margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "top_patches.png", scale=2)
fig.write_image(here / "top_patches.pdf")
