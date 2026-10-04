"""How much of the photo one feature-map value sees, layer by layer in VGG16 (section 8.2): the receptive field r,
from r = 1 and jump j = 1, grows by 2j at each 3 x 3 convolution and by j at each 2 x 2 pooling, which doubles j.
Drawn as a square centred on the kitten's eye in the Note's 224 x 224 photo (data/kitten_224.jpg).
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
img = np.array(Image.open(HERE.parent / "data" / "kitten_224.jpg").convert("RGB"))
assert img.shape == (224, 224, 3)
LAYERS = ["c"] * 2 + ["p"] + ["c"] * 2 + ["p"] + ["c"] * 3 + ["p"] + ["c"] * 3 + ["p"] + ["c"] * 3
NAMES = ["block1_conv1", "block1_conv2", "block1_pool", "block2_conv1", "block2_conv2", "block2_pool",
         "block3_conv1", "block3_conv2", "block3_conv3", "block3_pool", "block4_conv1", "block4_conv2",
         "block4_conv3", "block4_pool", "block5_conv1", "block5_conv2", "block5_conv3"]
r, j, R = 1, 1, []
for kind in LAYERS:
    if kind == "c":
        r += 2 * j
    else:
        r, j = r + j, 2 * j
    R.append(r)
assert [R[NAMES.index(n)] for n in ("block3_conv3", "block4_conv3", "block5_conv3")] == [40, 92, 196]
CX, CY = 84, 92                                          # a point near the kitten's left eye
CONV = [k for k, kind in enumerate(LAYERS) if kind == "c"]


def frame(k):
    fig = go.Figure(go.Image(z=img))
    h = R[k] / 2
    fig.add_shape(type="rect", x0=CX - h, x1=CX + h, y0=CY - h, y1=CY + h, line=dict(color="#F58518", width=7),
                  fillcolor="rgba(245,133,24,0.15)", opacity=1, layer="above")
    fig.add_scatter(x=[CX], y=[CY], mode="markers", marker=dict(size=8, color="#F58518"), showlegend=False)
    fig.update_xaxes(visible=False, range=[-0.5, 223.5])
    fig.update_yaxes(visible=False, range=[223.5, -0.5], scaleanchor="x")
    fig.update_layout(template="simple_white", width=760, height=820, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>{NAMES[k]}</b>: one value sees {R[k]} × {R[k]} pixels", x=0.5, y=0.97,
                                 font=dict(size=24)),
                      margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    print(dict(zip(NAMES, R)))
    tmp = HERE / ".rf_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for k in CONV:
        keys[k] = tmp / f"k{k}.png"
        frame(k).write_image(keys[k])
    seq = [CONV[0]] * 2 + [k for k in CONV for _ in range(2)] + [CONV[-1]] * 4
    for n, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{n:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=600:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse",
                    str(HERE / "receptive_field.gif")], check=True)
    ims = [Image.open(keys[NAMES.index(n)]).convert("RGB") for n in ("block3_conv3", "block4_conv3", "block5_conv3")]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "receptive_field_frames.png")
    shutil.rmtree(tmp)
