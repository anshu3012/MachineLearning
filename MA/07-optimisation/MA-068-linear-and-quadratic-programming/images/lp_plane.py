"""The profit 3 x1 + 2 x2 of the workshop LP as a surface (a tilted plane) over the plans (x1, x2), then tilted to the
top view: the profit lines of lp_region.png. The feasible polygon is lifted onto the plane (orange); the best corner
(3, 1) with profit 11 is the red point. Run: python lp_plane.py -> lp_plane.gif, lp_plane_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from tilt import tilt_gif

here = Path(__file__).parent
P = lambda x1, x2: 3 * x1 + 2 * x2
assert P(3, 1) == 11
X1, X2 = np.meshgrid(np.linspace(0, 4.6, 30), np.linspace(0, 4.2, 30))
corners = np.array([[0, 0], [3, 0], [3, 1], [1.5, 2.5], [0, 3], [0, 0]])


def marks(a):
    return [go.Scatter3d(x=corners[:, 0], y=corners[:, 1], z=P(corners[:, 0], corners[:, 1]) + 0.15, mode="lines",
                         line=dict(color="#F58518", width=8)),
            go.Scatter3d(x=[3], y=[1], z=[11.4], mode="markers", marker=dict(size=7, color="#E45756"))]


tilt_gif(here / "lp_plane", X1, X2, P(X1, X2), "Blues", (3, 21, 3), (0, 24), labels=("x1 (product A)", "x2 (product B)", "profit"),
         extra=marks, aspect=0.6, side_eye=(-1.4, -1.6, 0.8),
         titles=("Profit 3·x1 + 2·x2: a tilted plane, rising with both products", "Turn to the top view …",
                 "From above: lines of equal profit, the allowed plans (orange), the best corner (red)"))
