"""The revenue R(h, s) = 100 h^(2/3) s^(1/3) of the factory example as a surface over hours of labour h and tonnes of
steel s, then tilted to the top view: the revenue contour map used in budget_slider.gif. The budget line
20h + 2000s = 20000 is lifted onto the surface (green); the best plan (667 h, 3.33 t, R = 11,400) is the red point.
Run: python revenue_surface.py -> revenue_surface.gif, revenue_surface_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from tilt import tilt_gif

here = Path(__file__).parent
R = lambda h, s: 100 * h ** (2 / 3) * s ** (1 / 3)
H, S = np.meshgrid(np.linspace(0, 1600, 80), np.linspace(0, 16, 80))
assert round(R(2000 / 3, 10 / 3)) == 11400 or abs(R(2000 / 3, 10 / 3) - 11400) < 60
h = np.linspace(0, 1000, 100)
s = (20000 - 20 * h) / 2000


def marks(a):
    return [go.Scatter3d(x=h, y=s, z=R(h, s) + 150, mode="lines", line=dict(color="#54A24B", width=8)),
            go.Scatter3d(x=[2000 / 3], y=[10 / 3], z=[R(2000 / 3, 10 / 3) + 300], mode="markers", marker=dict(size=7, color="#E45756"))]


tilt_gif(here / "revenue_surface", H, S, R(H, S), "Blues", (3800, 34200, 3800), (0, 36000), labels=("labour h (hours)", "steel s (tonnes)", "revenue R"),
         extra=marks, aspect=0.7, titles=("Revenue R = 100 h^(2/3) s^(1/3): a hill rising away from (0, 0)", "Turn to the top view …",
                                           "From above: revenue contours, budget line (green), best plan (red)"))
