"""A digit and the same digit shifted 1 pixel right: feature map (vertical-edge filter + ReLU) and 2x2 max pooled map.
Right: how much each representation changes on 1000 test digits (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "shift_example.npz")
s = pd.read_csv(here.parent / "data" / "shift_change.csv")
fig = make_subplots(2, 4, column_widths=[0.17, 0.17, 0.17, 0.49], horizontal_spacing=0.025, vertical_spacing=0.1,
                    specs=[[{}, {}, {}, {"rowspan": 2}], [{}, {}, {}, None]],
                    subplot_titles=("digit", "feature map", "max pooled 2 x 2", "relative change after a 1-pixel shift",
                                    "shifted 1 pixel", "", ""))
top = max(d["f"].max(), 1e-9)
for r, (x, f, p) in enumerate(((d["x"], d["f"], d["p"]), (d["xs"], d["fs"], d["ps"])), start=1):
    fig.add_trace(go.Heatmap(z=x, colorscale="gray", showscale=False), r, 1)
    fig.add_trace(go.Heatmap(z=f, colorscale="gray_r", zmin=0, zmax=top, showscale=False), r, 2)
    fig.add_trace(go.Heatmap(z=p, colorscale="gray_r", zmin=0, zmax=top, showscale=False), r, 3)
labels = ["no pooling", "2 x 2 max", "3 x 3 max", "4 x 4 max", "global max"]
fig.add_trace(go.Bar(x=s.change, y=labels, orientation="h", marker_color=BLUE, text=s.change.round(2),
                     textposition="outside", cliponaxis=False), 1, 4)
for r in (1, 2):
    for c in (1, 2, 3):
        fig.update_xaxes(visible=False, row=r, col=c)
        fig.update_yaxes(visible=False, autorange="reversed", row=r, col=c)
fig.update_xaxes(range=[0, 1.05], title="change (0 = identical)", row=1, col=4)
fig.update_yaxes(autorange="reversed", ticklabelstandoff=8, row=1, col=4)
fig.layout.xaxis4.domain = [0.66, 1.0]
fig.update_layout(template="simple_white", width=1400, height=560, font=FONT, showlegend=False,
                  margin=dict(l=10, r=40, t=50, b=60))
fig.write_image(here / "shift_pool.png", scale=2)
fig.write_image(here / "shift_pool.pdf")
