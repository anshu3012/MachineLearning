"""An MNIST 9 as an image (left) and a 10 x 10 corner of it as the numbers the computer stores (right), Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import ORANGE, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "digit9.csv").to_numpy()
crop = d[4:14, 10:20]
fig = make_subplots(1, 2, column_widths=[0.42, 0.58], horizontal_spacing=0.06,
                    subplot_titles=("28 x 28 pixels", "the orange window as numbers (0 = black, 255 = white)"))
fig.add_trace(go.Heatmap(z=d, colorscale="gray", zmin=0, zmax=255, showscale=False), 1, 1)
fig.add_shape(type="rect", x0=9.5, x1=19.5, y0=3.5, y1=13.5, line=dict(color=ORANGE, width=4), row=1, col=1)
fig.add_trace(go.Heatmap(z=crop, colorscale="gray", zmin=0, zmax=255, showscale=False, text=crop, texttemplate="%{text}",
                         textfont=dict(family=FONT["family"], size=13), xgap=1, ygap=1), 1, 2)
for k in (1, 2):
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_xaxes(visible=False)
fig.update_layout(template="simple_white", width=1150, height=540, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "digit_grid.png", scale=2)
fig.write_image(here / "digit_grid.pdf")
