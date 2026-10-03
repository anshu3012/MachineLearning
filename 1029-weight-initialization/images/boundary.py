"""Decision regions of a 10-node sigmoid network started from all zeros vs from random weights (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
g = pd.read_csv(here.parent / "data" / "boundary_grid.csv")
d = pd.read_csv(here.parent / "data" / "moons.csv")
xs = np.sort(g.x1.unique())
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=["All weights start at 0: accuracy 87%", "Random start: accuracy 96%"])
scale = [[0, "#d6e2ee"], [0.5, "#ffffff"], [1, "#fde3c8"]]
for i, k in enumerate(("zeros", "random"), start=1):
    z = g[k].to_numpy().reshape(len(xs), len(xs))
    fig.add_trace(go.Heatmap(x=xs, y=xs, z=z, zmin=0, zmax=1, colorscale=scale, showscale=False, showlegend=False), 1, i)
    fig.add_trace(go.Contour(x=xs, y=xs, z=z, contours=dict(start=0.5, end=0.5, coloring="none"),
                             line=dict(color="black", width=3), showscale=False, showlegend=False), 1, i)
    for cls, col in ((0, BLUE), (1, ORANGE)):
        s = d[d.y == cls]
        fig.add_trace(go.Scatter(x=s.x1, y=s.x2, mode="markers", name=f"class {cls}", showlegend=i == 1,
                                 marker=dict(color=col, size=7, line=dict(color="white", width=0.5))), 1, i)
    fig.update_xaxes(title_text="x1 (standardised)", range=[-2.5, 2.5], row=1, col=i)
    fig.update_yaxes(title_text="x2 (standardised)" if i == 1 else None, range=[-2.5, 2.5], scaleanchor=f"x{i}",
                     row=1, col=i)
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.18), margin=dict(l=60, r=20, t=50, b=90))
fig.update_annotations(font=dict(family=FONT["family"], size=18))
fig.write_image(here / "boundary.png", scale=2)
fig.write_image(here / "boundary.pdf")
