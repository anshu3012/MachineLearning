"""Six photos from the cats-vs-dogs dataset with their label and original size (Plotly image grid)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "samples.npz")
titles = [f"{lab}: {size} pixels" for lab, size in zip(d["labels"], d["sizes"])]
fig = make_subplots(rows=1, cols=6, subplot_titles=titles, horizontal_spacing=0.012)
for i, img in enumerate(d["images"]):
    fig.add_trace(go.Image(z=img), row=1, col=i + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=14))
fig.update_layout(template="simple_white", width=1000, height=230, font=FONT, margin=dict(l=5, r=5, t=35, b=5))
fig.write_image(here / "samples.png", scale=2)
fig.write_image(here / "samples.pdf")
