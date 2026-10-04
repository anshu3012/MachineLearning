"""Too many cases to write: eight dogs that share no single colour, size or pose, and four photos that are
not dogs, each with its label. Data: 12 photos from the Kaggle Cats vs Dogs dataset (data/dog_cat_photos.npz, taken
from the batch saved by Note DL-049). Plotly: a grid of images with a text label under each."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
GREEN, ORANGE = "#2E7D32", "#C2410C"
D = np.load(HERE.parent / "data" / "dog_cat_photos.npz")
assert D["labels"].tolist() == [1] * 8 + [0] * 4          # 1 = dog

titles = [f"<span style='color:{GREEN if l else ORANGE}'><b>{'dog' if l else 'not a dog'}</b></span>"
          for l in D["labels"]]
fig = make_subplots(rows=2, cols=6, subplot_titles=titles, horizontal_spacing=0.015, vertical_spacing=0.14)
for k, im in enumerate(D["images"]):
    fig.add_trace(go.Image(z=im), row=k // 6 + 1, col=k % 6 + 1)
fig.update_xaxes(visible=False).update_yaxes(visible=False)
fig.update_annotations(font=dict(family="Latin Modern Roman", size=26))
fig.update_layout(width=1400, height=560, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="white")
fig.write_image(HERE / "dog_photos.png", scale=1)
