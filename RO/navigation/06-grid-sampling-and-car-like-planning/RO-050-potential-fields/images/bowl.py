"""Animation: the attractive potential alone, U_att = 1/2 |q - goal|^2 (zeta = 1), drawn as a surface over the room's
floor: a bowl whose lowest point, 0, is at the doorway centre (3.6, 4.0). The robot (ball) at (2, 1), where
U_att = 5.78, rolls straight down to the door, the 3.4 m straight drive. The furniture is outlined on the surface only:
the bowl does not know it. Then the camera tilts to straight above: the surface becomes its contour map.
Run -> bowl.gif, bowl_frames.png"""
from pathlib import Path

import numpy as np

import cspace as c
import pf
import pf3d
from gifkit import GREEN, make_gif

here = Path(__file__).parent
xs = np.arange(0, c.W + 1e-9, 0.05)
ys = np.arange(0, c.H + 1e-9, 0.05)
X, Y = np.meshgrid(xs, ys)
Z = 0.5 * pf.ZETA * ((X - pf.GOAL[0]) ** 2 + (Y - pf.GOAL[1]) ** 2)
assert round(pf.u_att(pf.START), 2) == 5.78
eta, pf.ETA = pf.ETA, 0.0                  # attraction only
P = pf.descend(pf.START)
pf.ETA = eta
assert abs(pf.path_length(P) + float(np.hypot(*(P[-1] - pf.GOAL))) - 3.4) < 1e-3   # a straight line
T, R1, R2, pink, green = c.furniture()
outl = [T, R1.union(R2), pink, green]
N = 26
idx = np.unique(np.linspace(0, len(P) - 1, N).astype(int))
lab = [(pf.GOAL[0], 3.75, "door, U = 0", "black")]
figs, holds, keys = [], [], []
figs.append(pf3d.frame(xs, ys, Z, balls=[(*P[0], GREEN)], labels=lab + [(2.0, 1.0, "U = 5.78", GREEN)],
                       outlines=outl, title="the pull of the door: a bowl, lowest at the door"))
holds.append(14); keys.append(0)
for k in idx[1:]:
    figs.append(pf3d.frame(xs, ys, Z, balls=[(*P[k], GREEN)], paths=[(P[:k + 1], GREEN)], labels=lab,
                           outlines=outl, title="the robot rolls downhill, straight at the door"))
    holds.append(1)
holds[-1] = 10; keys.append(len(figs) - 1)
T = 12
for j, s in enumerate(np.linspace(0, 1, T)[1:]):
    last = j == T - 2
    figs.append(pf3d.frame(xs, ys, Z, balls=[(*P[-1], GREEN)], paths=[(P, GREEN)], labels=lab if not last else [],
                           outlines=outl, s=s,
                           title="seen from straight above: the contour map" if last else "tilt the camera up"))
    holds.append(1)
holds[-1] = 24; keys.append(len(figs) - 1)
make_gif(figs, here / "bowl", fps=8, holds=holds, keys=keys, cols=3, width=900)
