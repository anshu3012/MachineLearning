"""One kitten photo and two random versions from each of five transformations (Plotly image grid)."""
from pathlib import Path
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
aug = here.parent / "data" / "aug"
names = ["flip", "rotation", "shift", "zoom", "shear"]
labels = {"flip": "horizontal flip", "rotation": "rotation (up to 40 degrees)", "shift": "shift (up to 20%)",
          "zoom": "zoom (up to 20%)", "shear": "shear (up to 20%)"}
fig = make_subplots(rows=2, cols=6, horizontal_spacing=0.01, vertical_spacing=0.08,
                    subplot_titles=["original"] + [labels[n] for n in names] + [""] * 6)
fig.add_trace(go.Image(z=np.array(Image.open(aug / "original.jpg"))), row=1, col=1)
for c, n in enumerate(names, start=2):
    for r in (1, 2):
        fig.add_trace(go.Image(z=np.array(Image.open(aug / f"{n}_{r - 1}.jpg"))), row=r, col=c)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=13))
fig.update_layout(template="simple_white", width=1000, height=380, font=FONT, margin=dict(l=5, r=5, t=30, b=5))
fig.write_image(here / "transforms.png", scale=2)
fig.write_image(here / "transforms.pdf")
