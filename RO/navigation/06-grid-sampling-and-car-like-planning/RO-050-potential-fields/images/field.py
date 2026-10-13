"""Animation: the total potential U = U_att + sum of U_rep (zeta = 1, eta = 0.02, influence distance 0.5 m) drawn as a
surface over the middle of the room (x from 1.4 to 5.8 m, y from 0.35 to 4 m; heights above 10 are cut off at 10, so
every obstacle with its 0.25 m band is a flat-topped block). Two robots (balls) roll downhill by gradient descent:
from (2, 1), U = 5.78, the green one rolls round the table's corner to the doorway; from (4.0, 0.5), U = 6.285, the red
one rolls left under the table and stops at (3.60, 0.59), U = 6.00, against the table's hill. Then the camera tilts to
straight above: the contour map, with both paths.
Run -> field.gif, field_frames.png"""
from pathlib import Path

import numpy as np

import pf
import pf3d
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent
xs, ys, U = pf.u_grid(0.04)
m, n = (xs >= 1.39) & (xs <= 5.81), ys >= 0.35
xs, ys, U = xs[m], ys[n], U[np.ix_(n, m)]
PA, PB = pf.descend(pf.START), pf.descend(pf.START2)
assert round(pf.U(pf.START), 2) == 5.78 and abs(pf.U(pf.START2) - 6.285) < 1e-9 and round(pf.U(PB[-1]), 2) == 6.00
N = 34
ia = np.unique(np.linspace(0, len(PA) - 1, N).astype(int))
ib = np.unique(np.linspace(0, len(PB) - 1, N).astype(int))
CAM, CMAX = (48, -20), 10.0
kw = dict(cam=CAM, cmax=CMAX, zaspect=0.6, r0=1.85, r1=1.25, box=1.55, height=640, notes_x=0.66, width=1250)
figs, holds, keys = [], [], []
figs.append(pf3d.frame(xs, ys, U, balls=[(*PA[0], GREEN), (*PB[0], RED)],
                       notes=[("green: start (2, 1), U = 5.78", GREEN), ("red: start (4.0, 0.5), U = 6.285", RED)],
                       title="the pull of the door plus a hill round every obstacle", **kw))
holds.append(14); keys.append(0)
for k in range(1, N):
    a, b = ia[k], ib[k]
    lab = [] if k < N - 1 else [("green: at the door", GREEN), ("red: stopped at (3.60, 0.59), U = 6.00", RED)]
    figs.append(pf3d.frame(xs, ys, U, balls=[(*PA[a], GREEN), (*PB[b], RED)], paths=[(PA[:a + 1], GREEN), (PB[:b + 1], RED)],
                           notes=lab, title="both robots roll downhill", **kw))
    holds.append(1)
holds[-1] = 12; keys.append(len(figs) - 1)
T = 12
for j, s in enumerate(np.linspace(0, 1, T)[1:]):
    last = j == T - 2
    figs.append(pf3d.frame(xs, ys, U, balls=[(*PA[-1], GREEN), (*PB[-1], RED)], paths=[(PA, GREEN), (PB, RED)], s=s,
                           title="seen from straight above: the contour map" if last else "tilt the camera up", **kw))
    holds.append(1)
holds[-1] = 24; keys.append(len(figs) - 1)
make_gif(figs, here / "field", fps=8, holds=holds, keys=keys, cols=3, width=900)
