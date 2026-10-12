"""Animation: the Rimon-Koditschek navigation function phi (kappa = 2) on the world of disks that stands in for the room:
the robot's centre moves in a disk of radius 3.3 m about (3.5, 2.0); the table, grown by 0.25 m, is a disk of radius
1.3 m at (4.2, 1.9); the two poles, grown, are disks of radius 0.35 m at (1, 3) and (6, 0.8). phi is 0 at the doorway
centre (3.6, 4.0) and 1 on every boundary (drawn at 1 outside the free region too). The robot from (4.0, 0.5),
phi = 0.705, rolls down to the door; then the camera tilts to the contour map.
Run -> rk_surface.gif, rk_surface_frames.png"""
from pathlib import Path

import numpy as np
from shapely.geometry import Point

import pf
import pf3d
from gifkit import RED, make_gif

here = Path(__file__).parent
K = 2.0
xs = np.arange(0.2, 6.8001, 0.03)
ys = np.arange(-1.3, 5.3001, 0.03)
X, Y = np.meshgrid(xs, ys)
Z = np.nan_to_num(pf.rk(np.stack([X, Y], -1), K), nan=1.0)
P = pf.rk_descend(pf.START2, K)
assert np.hypot(*(P[-1] - pf.GOAL)) < 0.03 and round(float(pf.rk(pf.START2, K)), 3) == 0.705
disks = [Point(*pf.SW_C0).buffer(pf.SW_R0, quad_segs=64)] + [Point(*cc).buffer(r, quad_segs=32) for cc, r in pf.SW_OBS]
outl = disks
kw = dict(cmax=1.0, contours=0.1, zlabel="φ", zticks=(0, 0.5, 1), xticks=range(1, 7), yticks=range(-1, 6),
          cam=(40, -20), zaspect=0.55, r0=2.0, r1=1.5, box=1.0, height=720, outlines=outl, notes_x=0.68, width=1250)
N = 30
idx = np.unique(np.linspace(0, len(P) - 1, N).astype(int))
notes0 = [("door: φ = 0", "black"), ("every boundary: φ = 1", "black"), ("red: start (4.0, 0.5), φ = 0.705", RED)]
figs, holds, keys = [pf3d.frame(xs, ys, Z, balls=[(*P[0], RED)], notes=notes0, title="a navigation function on the world of disks", **kw)], [14], [0]
for k in idx[1:]:
    figs.append(pf3d.frame(xs, ys, Z, balls=[(*P[k], RED)], paths=[(P[:k + 1], RED)], notes=notes0,
                           title="the robot rolls downhill to the door", **kw))
    holds.append(1)
holds[-1] = 10; keys.append(len(figs) - 1)
T = 12
for j, s in enumerate(np.linspace(0, 1, T)[1:]):
    last = j == T - 2
    figs.append(pf3d.frame(xs, ys, Z, balls=[(*P[-1], RED)], paths=[(P, RED)], s=s, notes=[] if s > 0.5 else notes0,
                           title="seen from straight above: the contour map" if last else "tilt the camera up", **kw))
    holds.append(1)
holds[-1] = 24; keys.append(len(figs) - 1)
make_gif(figs, here / "rk_surface", fps=8, holds=holds, keys=keys, cols=3, width=900)
