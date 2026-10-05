"""The bowl f = x1^2 + x1 x2 + x2^2 - 8 x1 - 7 x2 of the quadratic program as a 3-D surface, with the feasible triangle
lifted onto it (orange), the unconstrained minimum (3, 2) (black) and the constrained minimum (1.5, 0.5) (green star
colour), then tilted to the top view: the contour map of qp_region.png.
Run: python qp_surface.py -> qp_surface.gif, qp_surface_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from tilt import tilt_gif

here = Path(__file__).parent
f = lambda x, y: x ** 2 + x * y + y ** 2 - 8 * x - 7 * y
assert f(3, 2) == -19 and f(1.5, 0.5) == -12.25
X, Y = np.meshgrid(np.linspace(-0.5, 4, 70), np.linspace(-0.5, 4, 70))
tri = np.array([[0, 0], [2, 0], [0, 2], [0, 0]])
e = np.linspace(0, 2, 30)


def marks(a):
    pts = [(tri[i] + (tri[i + 1] - tri[i]) * t) for i in range(3) for t in np.linspace(0, 1, 20)]
    pts = np.array(pts)
    return [go.Scatter3d(x=pts[:, 0], y=pts[:, 1], z=f(pts[:, 0], pts[:, 1]) + 0.3, mode="lines", line=dict(color="#F58518", width=8)),
            go.Scatter3d(x=[3], y=[2], z=[-19 + 0.4], mode="markers", marker=dict(size=6, color="black")),
            go.Scatter3d(x=[1.5], y=[0.5], z=[-12.25 + 0.5], mode="markers", marker=dict(size=7, color="#54A24B"))]


tilt_gif(here / "qp_surface", X, Y, f(X, Y), "Blues", (-18, 6, 3), (-20, 12), labels=("x1", "x2", "f"), extra=marks, reverse=True,
         aspect=0.7, titles=("The bowl f(x1, x2): its bottom (3, 2) lies outside the orange triangle", "Turn to the top view …",
                             "From above: the contour map, the triangle, the bottom (black), the answer (green)"))
