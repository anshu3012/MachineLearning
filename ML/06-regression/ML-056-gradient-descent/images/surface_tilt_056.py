"""Loss surface of the 100-point example (m and b), tilted from the side view to the top view, ending on the contour
map of contour_path.py. The orange path is the 30-epoch gradient descent run of Figure 6."""
from pathlib import Path
import numpy as np
from common import x100, y100
from gifkit import make_gif
from surface_tilt import tilt_figs

HERE = Path(__file__).parent
m, b, lr = -127.82, 150.0, 0.001
path = [(m, b)]
for _ in range(30):
    gb = -2 * np.sum(y100 - m * x100 - b)
    gm = -2 * np.sum((y100 - m * x100 - b) * x100)
    b, m = b - lr * gb, m - lr * gm
    path.append((m, b))
path = np.array(path)
mg, bg = np.linspace(-150, 150, 90), np.linspace(-150, 170, 90)
Z = np.array([[np.sum((y100 - mm * x100 - bb) ** 2) for mm in mg] for bb in bg])
LEVELS = (float(Z.min()), float(Z.max()), (float(Z.max()) - float(Z.min())) / 25)
if __name__ == "__main__":
    figs = tilt_figs(mg, bg, Z, LEVELS, "m (slope)", "b (intercept)", "loss", mark=tuple(path[-1]), path=path,
                     start=tuple(path[0]), lift=float(Z.max()) * 0.01)
    make_gif(figs, HERE / "surface_tilt", fps=4, holds=[4] + [1] * (len(figs) - 2) + [10],
             keys=[0, 3, 6, len(figs) - 1], cols=2, width=800)
