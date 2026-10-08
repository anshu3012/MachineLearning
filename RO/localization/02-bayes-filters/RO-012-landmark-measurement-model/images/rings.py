"""Where can the robot be? Each frame multiplies in one more landmark's range reading, over every position (x, y)
in the room, and rescales the product so its highest point is 1. Pink alone: a ring of radius 3.10 m. Pink x green:
the two rings meet near (1.9, 2.0); their second meeting point lies outside the room. Pink x green x blue: one
peak at the robot's true position (2, 2). Run -> rings.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, make_gif
from lmmodel import LM, POSE_A, READ, range_density_xy

here = Path(__file__).parent
xs, ys = np.linspace(0, 5, 251), np.linspace(0, 4, 201)
X, Y = np.meshgrid(xs, ys)
COL = {"pink": "#E377C2", "green": "#54A24B", "blue": "#4C78A8"}
steps = [["pink"], ["pink", "green"], ["pink", "green", "blue"]]


def frame(names):
    Z = np.ones_like(X)
    for n in names:
        Z = Z * range_density_xy(X, Y, n)
    Z = Z / Z.max()
    fig = go.Figure(go.Heatmap(x=xs, y=ys, z=Z, colorscale="Magenta", zmin=0, zmax=1, colorbar=dict(title="relative")))
    for n, (mx, my) in LM.items():
        on = n in names
        fig.add_trace(go.Scatter(x=[mx], y=[my], mode="markers", marker=dict(size=18 if on else 12, color=COL[n],
                                 line=dict(color="black", width=2 if on else 0), opacity=1 if on else 0.4)))
    fig.add_trace(go.Scatter(x=[POSE_A[0]], y=[POSE_A[1]], mode="markers", marker=dict(symbol="x", size=14, color="black")))
    i, j = np.unravel_index(Z.argmax(), Z.shape)
    title = " × ".join(f"{n} ({READ[n][0]:.2f} m)" for n in names)
    fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=100, b=60),
                      title=dict(x=0.5, font_size=21, text=f"range readings used: {title}<br>"
                                 + (f"highest point ({xs[j]:.2f}, {ys[i]:.2f}); " if len(names) > 1 else "every point on the ring fits; ")
                                 + "black x: true position (2, 2)"))
    fig.update_xaxes(title="x (m)", range=[0, 5], dtick=1, scaleanchor="y")
    fig.update_yaxes(title="y (m)", range=[0, 4], dtick=1)
    return fig


figs = [frame(s) for s in steps]
make_gif(figs, here / "rings", fps=1, holds=[3, 3, 5], keys=[0, 1, 2], cols=3, width=800)
