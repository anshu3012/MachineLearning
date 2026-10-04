"""Why strides lose detail and save work (section 6): a 3 x 3 vertical-edge filter on a 256 x 256 photo (the SciPy
'ascent' test image, data/photo.png), padding 1, at strides 1, 2 and 3. Each panel shows the edge strength and
the number of multiplications (9 per position). Computed with Keras Conv2D. Plotly."""
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402
import keras  # noqa: E402

HERE = Path(__file__).parent
img = np.array(Image.open(HERE.parent / "data" / "photo.png"), dtype="float32") / 255
assert img.shape == (256, 256)
K = np.array([[-1, 0, 1]] * 3, dtype="float32")[:, :, None, None]
maps = {}
for s in (1, 2, 3):
    layer = keras.layers.Conv2D(1, 3, strides=s, padding="same", use_bias=False)
    layer.build((1, 256, 256, 1))
    layer.set_weights([K])
    maps[s] = np.abs(layer(img[None, :, :, None]).numpy()[0, :, :, 0])
mult = {s: maps[s].size * 9 for s in maps}
assert [maps[s].shape[0] for s in (1, 2, 3)] == [256, 128, 86] and mult[1] == 589_824
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.03, subplot_titles=[
    f"stride {s}: {maps[s].shape[0]} × {maps[s].shape[1]} map, {mult[s]:,} multiplications" for s in (1, 2, 3)])
for k, s in enumerate((1, 2, 3), start=1):
    fig.add_trace(go.Heatmap(z=maps[s], colorscale="Greys", showscale=False, hoverinfo="skip",
                             zmax=np.percentile(maps[1], 99)), 1, k)
    fig.update_xaxes(visible=False, row=1, col=k)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1400, height=520, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=10, r=10, t=60, b=10))
for a in fig.layout.annotations:
    a.font.size = 19
fig.write_image(HERE / "stride_photo.png", scale=2)
print(mult)
