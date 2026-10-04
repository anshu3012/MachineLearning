"""Learning from labelled examples: twelve photos, each labelled "dog" or "not a dog". Data: 12 photos from the Kaggle
Cats vs Dogs dataset, shared with Note 1 (../01-what-is-ml/data/dog_cat_photos.npz). Plotly: a grid of images."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
GREEN, ORANGE = "#2E7D32", "#C2410C"
D = np.load(HERE.parent.parent / "01-what-is-ml" / "data" / "dog_cat_photos.npz")
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
