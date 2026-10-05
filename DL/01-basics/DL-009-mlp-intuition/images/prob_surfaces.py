"""The probability surfaces behind sigmoid_map.png and prob_maps.png: the camera tilts from a side view to the top view,
which is the contour map of the next figure. sigmoid_surface: p = s(3 x1 + 3 x2) with the point (0.5, 0.5), p = 0.953.
prob_surfaces: perceptron 1, perceptron 2 and the combined s(8 p1 + 8 p2 - 12), with the point (0, 0): 0.5, 0.5, 0.018.
Plotly (go.Surface) -> gifkit. Run: python prob_surfaces.py"""
from pathlib import Path

import numpy as np

from surftilt import tilt_gif

HERE = Path(__file__).parent
s = lambda z: 1 / (1 + np.exp(-z))
xs = np.linspace(-3, 3, 121)
X1, X2 = np.meshgrid(xs, xs)
H1, H2 = s(3 * (X1 + X2)), s(3 * (X1 - X2))
OUT = s(8 * H1 + 8 * H2 - 12)
SCALE = [[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]]
assert round(float(s(3)), 3) == 0.953 and round(float(s(8 * 0.5 + 8 * 0.5 - 12)), 3) == 0.018
CON = dict(start=0.1, end=0.9, size=0.1)


def pane(Z, xy, title, color="#E45756"):
    z0 = float(Z[len(xs) // 2 + int(round(xy[1] / 0.05)), len(xs) // 2 + int(round(xy[0] / 0.05))])
    return dict(x=xs, y=xs, Z=Z, xlab="x₁", ylab="x₂", zlab="p", cscale=SCALE, contours=CON, zrange=(0, 1), title=title,
                marks=[dict(x=[xy[0]], y=[xy[1]], z=[z0], color="black", size=8, line=False)])


tilt_gif("sigmoid_surface", HERE, pane(H1, (0.5, 0.5), None), zasp=0.6, floor=0.3)
tilt_gif("prob_surfaces", HERE, [pane(H1, (0, 0), "Perceptron 1"), pane(H2, (0, 0), "Perceptron 2"), pane(OUT, (0, 0), "Combined")],
         zasp=0.6, floor=0.3)
