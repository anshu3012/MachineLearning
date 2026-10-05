"""E(m, b) for the 160 training students: tilt from the side view to the top view (the contour map of Figure 1)."""
from pathlib import Path
import numpy as np
from common import B, M, X_train, y_train
from gifkit import make_gif
from surface_tilt import tilt_figs

HERE = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
E = lambda m, b: float(((y - m * x - b) ** 2).sum())
ms, bs = np.linspace(-0.05, 0.85, 90), np.linspace(-1.7, 0.4, 90)
Z = np.log10([[E(mm, bb) for mm in ms] for bb in bs])          # height = log10 E, same as the map
figs = tilt_figs(ms, bs, Z, (float(Z.min()) + 0.04, float(Z.max()), 0.12), "m (slope)", "b (intercept)", "log10 E",
                 mark=(M, B), start=(0.0, 0.0))
make_gif(figs, HERE / "surface_tilt", fps=4, holds=[4] + [1] * (len(figs) - 2) + [10], keys=[0, 3, 6, len(figs) - 1],
         cols=2, width=800)
