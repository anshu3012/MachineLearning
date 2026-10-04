"""Augmentation acts only during training (section 5.2): the Note's augmentation pipeline of section 6.1
(RandomFlip, RandomRotation(0.1), RandomZoom(0.2)) applied to the kitten photo (data/aug/original.jpg) three times
with training=True, which gives three different images, and three times with training=False, which returns the photo
unchanged. Seeded. Plotly."""
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402
import keras  # noqa: E402
from keras import layers  # noqa: E402

HERE = Path(__file__).parent
img = np.array(Image.open(HERE.parent / "data" / "aug" / "original.jpg").convert("RGB"), dtype="float32")
keras.utils.set_random_seed(0)
aug = keras.Sequential([layers.RandomFlip("horizontal"), layers.RandomRotation(0.1), layers.RandomZoom(0.2)])
train = [aug(img[None], training=True).numpy()[0] for _ in range(3)]
infer = [aug(img[None], training=False).numpy()[0] for _ in range(3)]
assert all(np.allclose(x, img) for x in infer) and not np.allclose(train[0], train[1])
fig = make_subplots(rows=2, cols=3, horizontal_spacing=0.02, vertical_spacing=0.08,
                    subplot_titles=[f"training=True, call {k + 1}" for k in range(3)] +
                                   [f"training=False, call {k + 1}: unchanged" for k in range(3)])
for k in range(3):
    fig.add_trace(go.Image(z=train[k].clip(0, 255).astype("uint8")), 1, k + 1)
    fig.add_trace(go.Image(z=infer[k].clip(0, 255).astype("uint8")), 2, k + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(template="simple_white", width=1100, height=780, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(HERE / "train_vs_infer.png", scale=2)
