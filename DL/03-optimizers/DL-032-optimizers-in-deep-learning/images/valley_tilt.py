"""The narrow valley L = (w1^2 + 100 w2^2)/2 as a surface, tilting from the side view to the top view, which is the
contour map of Figure 5. Height = the loss L; the lines are drawn at the contour map's own levels (a ring every 0.3 in
log10(L + 0.01), about a factor 2 in L). The red path is plain gradient descent, eta = 0.019, from (-10, 0.4), 50 steps (middle panel of
Figure 5). Run: python valley_tilt.py -> valley_tilt.gif, valley_tilt_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import FONT
from surf import quad_surface, VALLEY_LEVELS, path3d, star3d, scene, phase, gif

HERE = Path(__file__).parent
K, ETA = 100, 0.019
w = np.array([-10.0, 0.4])
P = [w.copy()]
for _ in range(50):
    w = w - ETA * np.array([w[0], K * w[1]])
    P.append(w.copy())
P = np.array(P)
height = lambda a, b: 0.5 * (a ** 2 + K * b ** 2)          # the true loss
assert abs(0.5 * (10 ** 2 + K * 0.4 ** 2) - 58) < 1e-9
gx, gy = np.linspace(-11, 2, 130), np.linspace(-0.6, 0.6, 61)
ZMAX = 62                                                   # the corners go higher than drawn
TRACES = quad_surface(gx, gy, np.zeros(2), np.diag([0.5, 50.0]), 0.0, VALLEY_LEVELS, ZMAX, -2, 2.2, off=0.01)
N = 24


def frame(k):
    t = k / (N - 1)
    fig = go.Figure([*TRACES, path3d(P, height(P[:, 0], P[:, 1])), star3d(0, 0, 0.4)])
    fig.update_layout(template="simple_white", width=950, height=560, font=dict(FONT, size=18),
                      title=dict(text=phase(t), x=0.5, y=0.96),
                      scene=scene("w₁", "w₂", "loss L", [0, ZMAX], (2.6, 1.3, 1.0), t,
                                  x=dict(range=[-11, 2]), y=dict(range=[-0.6, 0.6], nticks=3), z=dict(nticks=3)),
                      margin=dict(l=0, r=0, t=50, b=0))
    return fig


if __name__ == "__main__":
    gif(HERE, "valley_tilt", frame, N, 3, 8, 6, 760, (0, 8, 16, N - 1))
