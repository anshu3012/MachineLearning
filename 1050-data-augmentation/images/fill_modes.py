"""The photo shifted 30% right and down, with the empty pixels filled in four ways (Plotly image grid)."""
from pathlib import Path
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
aug = here.parent / "data" / "aug"
modes = ["nearest", "reflect", "constant", "wrap"]
fig = make_subplots(rows=1, cols=5, horizontal_spacing=0.012,
                    subplot_titles=["original"] + [f'fill_mode="{m}"' for m in modes])
fig.add_trace(go.Image(z=np.array(Image.open(aug / "original.jpg"))), row=1, col=1)
for c, m in enumerate(modes, start=2):
    fig.add_trace(go.Image(z=np.array(Image.open(aug / f"fill_{m}.jpg"))), row=1, col=c)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=14))
fig.update_layout(template="simple_white", width=1000, height=250, font=FONT, margin=dict(l=5, r=5, t=35, b=5))
fig.write_image(here / "fill_modes.png", scale=2)
fig.write_image(here / "fill_modes.pdf")
