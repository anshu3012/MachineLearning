"""The damping ratio sets the kind of response. The natural frequency stays at 2 rad/s (Kp = 0.4 N m/rad) while the
damping ratio falls from 2 to 0 (Kd = 0.4 zeta N m s/rad). Left: the two roots, with earlier positions faint and the
circle of radius 2 dotted; right: the heading step response 0 -> 0.5 rad with its overshoot and 2 percent settling
time. Overdamped (zeta > 1): two real roots, a slow creep. Critically damped (zeta = 1): both roots at -2, the fastest
response with no overshoot, settled at 2.92 s. Underdamped (zeta < 1): two complex roots on the circle, overshoot.
Undamped (zeta = 0): roots on the imaginary axis, a swing that never dies.
Run: python zeta_anim.py -> zeta_anim.gif, zeta_anim_frames.png"""
from pathlib import Path

import numpy as np
from gifkit import make_gif
from stepkit import roots
from sweepdraw import frame

here = Path(__file__).parent
ZETAS = [2.0, 1.75, 1.5, 1.3, 1.15, 1.05, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]


def kind(z):
    return ("overdamped" if z > 1 else "critically damped" if z == 1 else "underdamped" if z > 0 else "undamped")


figs, trail, holds = [], [], []
for z in ZETAS:
    fig, i, settled = frame(2.0, z, f"ωn = 2 rad/s, damping ratio ζ = {z:.2f} (Kd = {0.4 * z:.2f}): {kind(z)}",
                            trail=list(trail), circle=2.0)
    if z == 1.0:
        assert np.allclose(roots(2, 1), [-2, -2]) and i["overshoot"] == 0 and abs(i["settle"] - 2.917) < 2e-3
    if z == 0.2:
        assert np.allclose(sorted(roots(2, 0.2).imag), [-1.9596, 1.9596], atol=1e-4) and abs(i["overshoot"] - 0.527) < 5e-4
    if z == 2.0:
        assert np.allclose(sorted(roots(2, 2).real), [-7.464, -0.536], atol=1e-3) and abs(i["settle"] - 7.44) < 0.01
    if z == 0.0:
        assert not settled and abs(i["overshoot"] - 1.0) < 1e-3
    trail.extend(roots(2.0, z))
    figs.append(fig)
    holds.append(14 if z in (2.0, 1.0, 0.7, 0.2) else 30 if z == 0.0 else 4)
make_gif(figs, here / "zeta_anim", fps=6, holds=holds, keys=[0, 6, 14, 16], cols=2, width=950)
