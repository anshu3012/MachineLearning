"""An MNIST image as a table row: the 28 x 28 picture (first training image, a 5) and the same 784 numbers laid out
as one row, shown here wrapped into 28 strips of 28 so the top image row becomes columns 1 to 28."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
img = pd.read_csv(here.parent / "data" / "mnist_example.csv").values.reshape(28, 28)
assert img.shape == (28, 28) and img.max() == 255
row = img.reshape(1, -1)
fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0.12,
                    subplot_titles=["the image: 28 × 28 pixels", "the same image as one row of 784 columns (columns 337 to 476, image rows 13 to 17)"])
fig.add_heatmap(z=img[::-1], colorscale="Greys", zmin=0, zmax=255, showscale=False, row=1, col=1)
fig.add_heatmap(z=row[:, 336:476], x=np.arange(337, 477), colorscale="Greys", zmin=0, zmax=255, showscale=False, row=2, col=1)
for c in (364, 392, 420, 448):
    fig.add_vline(x=c + 0.5, line=dict(color="#E45756", width=2), row=2, col=1)
fig.update_xaxes(visible=False, scaleanchor="y", row=1, col=1)
fig.update_yaxes(visible=False, row=1, col=1)
fig.update_xaxes(title_text="column (red lines: a new image row starts every 28 columns)", row=2, col=1)
fig.update_yaxes(visible=False, row=2, col=1)
for a in fig.layout.annotations:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1100, height=820, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=30, r=30, t=50, b=60))
fig.write_image(here / "image_row.png", scale=2)
fig.write_image(here / "image_row.pdf")
