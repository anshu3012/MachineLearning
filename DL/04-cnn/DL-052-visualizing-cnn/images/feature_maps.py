"""The kitten photo and the first 8 feature maps it produces at six layers of VGG16 (Plotly image grid)."""
from pathlib import Path
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
data = here.parent / "data"
maps = np.load(data / "feature_maps.npz")
layers = [("layer1", "layer 1: block1_conv1, 224 x 224"), ("layer2", "layer 2: block1_conv2, 224 x 224"),
          ("layer5", "layer 5: block2_conv2, 112 x 112"), ("layer9", "layer 9: block3_conv3, 56 x 56"),
          ("layer13", "layer 13: block4_conv3, 28 x 28"), ("layer17", "layer 17: block5_conv3, 14 x 14")]
fig = make_subplots(rows=len(layers), cols=9, horizontal_spacing=0.008, vertical_spacing=0.045,
                    column_widths=[1.15] + [1] * 8)
kitten = np.array(Image.open(data / "kitten_224.jpg").resize((112, 112)))
fig.add_trace(go.Image(z=kitten), row=1, col=1)
for r, (key, label) in enumerate(layers, start=1):
    m = maps[key]
    for c in range(8):
        grey = np.repeat(m[..., c:c + 1], 3, axis=2)          # brighter = larger value
        fig.add_trace(go.Image(z=grey), row=r, col=c + 2)
    top = fig.get_subplot(r, 2).yaxis.domain[1]               # just above this row's maps
    left = fig.get_subplot(r, 2).xaxis.domain[0]
    fig.add_annotation(text=label, xref="paper", yref="paper", x=left, xanchor="left", y=top, yanchor="bottom",
                       showarrow=False, font=dict(size=14))
below = fig.get_subplot(1, 1).yaxis.domain[0]
fig.add_annotation(text="input photo", xref="paper", yref="paper", x=0.0, y=below, xanchor="left", yanchor="top",
                   showarrow=False, font=dict(size=14))
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(template="simple_white", width=950, height=820, font=FONT, margin=dict(l=5, r=5, t=28, b=5))
fig.write_image(here / "feature_maps.png", scale=2)
fig.write_image(here / "feature_maps.pdf")
