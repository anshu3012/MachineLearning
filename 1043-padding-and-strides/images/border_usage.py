"""How many 3x3 filter positions cover each pixel of a 5x5 image, without and with one ring of zero padding (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
maps = [pd.read_csv(here.parent / "data" / f"usage_{k}.csv").to_numpy() for k in ("valid", "padded")]
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=("no padding: corners used once, centre 9 times", "padding 1: corners used 4 times"))
for k, M in enumerate(maps, start=1):
    fig.add_trace(go.Heatmap(z=M, zmin=0, zmax=9, colorscale="Blues", showscale=False, text=M, texttemplate="%{text}",
                             textfont=dict(family=FONT["family"], size=22), xgap=2, ygap=2), 1, k)
    fig.update_yaxes(autorange="reversed", visible=False, scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_xaxes(visible=False)
fig.update_layout(template="simple_white", width=1000, height=500, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "border_usage.png", scale=2)
fig.write_image(here / "border_usage.pdf")
