"""Classification: decision boundaries for dropout rates 0, 0.2 and 0.5, with the training points (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
d = here.parent / "data"
g, pts, sc = (pd.read_csv(d / f) for f in ("classification_grid.csv", "classification_points.csv",
                                            "classification_scores.csv"))
xs, ys = sorted(g.x1.unique()), sorted(g.x2.unique())
titles = [f"p = {r.p:g}: train {r.train_accuracy:.0%}, val. {r.val_accuracy:.0%}" for r in sc.itertuples()]
fig = make_subplots(1, 3, horizontal_spacing=0.05, subplot_titles=titles)
for k, p in enumerate(["0", "0.2", "0.5"]):
    z = g.pivot(index="x2", columns="x1", values=f"p={p}").values
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=(z > 0.5).astype(int), showscale=False, opacity=0.2,
                             colorscale=[[0, ORANGE], [1, BLUE]]), 1, k + 1)
    fig.add_trace(go.Contour(x=xs, y=ys, z=z, showscale=False, contours=dict(start=0.5, end=0.5, size=1,
                  coloring="lines"), colorscale=[[0, "black"], [1, "black"]], line=dict(width=2.5)), 1, k + 1)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        q = pts[pts.y == cls]
        fig.add_scatter(x=q.x1, y=q.x2, mode="markers", name=f"class {cls}", showlegend=k == 0,
                        marker=dict(color=c, size=7, line=dict(width=1, color="white")), row=1, col=k + 1)
fig.update_xaxes(range=[-4, 4], title="x1")
fig.update_yaxes(range=[-4, 4])
fig.update_yaxes(title="x2", col=1)
fig.update_layout(template="simple_white", width=1200, height=480, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=17))
fig.write_image(here / "boundaries.png", scale=2)
fig.write_image(here / "boundaries.pdf")
