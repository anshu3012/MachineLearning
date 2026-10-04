"""Decision boundaries after 3,500 epochs and after early stopping, with the training points (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
g = pd.read_csv(here.parent / "data" / "boundary_grid.csv")
pts = pd.read_csv(here.parent / "data" / "points.csv")
e = pd.read_csv(here.parent / "data" / "history_early_stopping.csv")
xs, ys = sorted(g.x1.unique()), sorted(g.x2.unique())
fig = make_subplots(1, 2, horizontal_spacing=0.06,
                    subplot_titles=["3,500 epochs", f"Early stopping ({len(e)} epochs)"])
for col, key in ((1, "p_3500"), (2, "p_es")):
    z = g.pivot(index="x2", columns="x1", values=key).values
    fig.add_trace(go.Contour(x=xs, y=ys, z=z, showscale=False, contours=dict(start=0.5, end=0.5, size=1,
                  coloring="lines"), colorscale=[[0, "black"], [1, "black"]], line=dict(width=3)), 1, col)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=(z > 0.5).astype(int), showscale=False, opacity=0.18,
                             colorscale=[[0, ORANGE], [1, BLUE]]), 1, col)
    for cls, c, name in ((0, ORANGE, "class 0 (outer)"), (1, BLUE, "class 1 (inner)")):
        for s, sym in (("train", "circle"), ("validation", "x")):
            d = pts[(pts.y == cls) & (pts.set == s)]
            fig.add_scatter(x=d.x1, y=d.x2, mode="markers", marker=dict(color=c, size=9, symbol=sym,
                            line=dict(width=1, color="white") if sym == "circle" else None),
                            name=f"{name}, {s}", showlegend=col == 1, row=1, col=col)
fig.update_xaxes(range=[-1.6, 1.6], title="x1")
fig.update_yaxes(range=[-1.6, 1.6], scaleanchor="x", title="x2", row=1, col=1)
fig.update_yaxes(range=[-1.6, 1.6], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=600, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.15), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "boundaries.png", scale=2)
fig.write_image(here / "boundaries.pdf")
