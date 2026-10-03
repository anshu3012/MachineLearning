"""Decision boundaries on make_moons: one hidden layer of 1, 10, 50, 1000 neurons (neurons.png), and the 128-128
network without regularisation, with L2 and with L1 (regularised.png) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
d = here.parent / "data"
g, pts = pd.read_csv(d / "boundary_grid.csv"), pd.read_csv(d / "points.csv")
xs, ys = sorted(g.x1.unique()), sorted(g.x2.unique())


def panel_figure(keys, titles, name):
    fig = make_subplots(1, len(keys), horizontal_spacing=0.03, subplot_titles=titles)
    for k, key in enumerate(keys):
        z = g.pivot(index="x2", columns="x1", values=key).values
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=(z > 0.5).astype(int), showscale=False, opacity=0.2,
                                 colorscale=[[0, ORANGE], [1, BLUE]]), 1, k + 1)
        fig.add_trace(go.Contour(x=xs, y=ys, z=z, showscale=False, contours=dict(start=0.5, end=0.5, size=1,
                      coloring="lines"), colorscale=[[0, "black"], [1, "black"]], line=dict(width=2.5)), 1, k + 1)
        for cls, c in ((0, ORANGE), (1, BLUE)):
            q = pts[pts.y == cls]
            fig.add_scatter(x=q.x1, y=q.x2, mode="markers", name=f"class {cls}", showlegend=k == 0,
                            marker=dict(color=c, size=7, line=dict(width=1, color="white")), row=1, col=k + 1)
    fig.update_xaxes(range=[-2, 3], showticklabels=False)
    fig.update_yaxes(range=[-1.75, 2.25], showticklabels=False)
    fig.update_layout(template="simple_white", width=300 * len(keys) + 100, height=380, font=FONT,
                      legend=dict(orientation="h", x=0.0, y=-0.05), margin=dict(l=20, r=20, t=50, b=40))
    fig.update_annotations(font=dict(size=18))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


panel_figure(["n=1", "n=10", "n=50", "n=1000"], ["1 neuron", "10 neurons", "50 neurons", "1,000 neurons"], "neurons")
panel_figure(["none", "L2", "L1"], ["No regularisation", "L2, λ = 0.03", "L1, λ = 0.001"], "regularised")
