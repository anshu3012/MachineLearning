"""The natural frequency only stretches time. The damping ratio stays at 0.2 while the natural frequency rises from
1 to 4 rad/s (Kp = 0.1 wn^2 N m/rad, Kd = 0.04 wn N m s/rad). Left: the two roots move out along one ray from the
origin, on a circle of radius wn (dotted); right: the heading step response 0 -> 0.5 rad. The overshoot stays
52.7 percent; the response is squeezed in time: the 2 percent settling time falls from 9.80 s at wn = 2 to 4.90 s at
wn = 4. The title gives the torque the gain asks for at the start, against the 0.2 N m limit.
Run: python wn_anim.py -> wn_anim.gif, wn_anim_frames.png"""
from pathlib import Path

import numpy as np
from gifkit import make_gif
from stepkit import I, TAU_MAX, TH_REF, roots
from sweepdraw import frame

here = Path(__file__).parent
WNS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0]
ZETA = 0.2
figs, trail, holds, oss = [], [], [], []
for wn in WNS:
    kp = I * wn ** 2
    torque = kp * TH_REF
    flag = "within" if torque <= TAU_MAX + 1e-12 else "over"
    fig, i, settled = frame(wn, ZETA, f"ζ = 0.2, ωn = {wn:g} rad/s: Kp = {kp:.3g}, start torque {torque:.3g} N·m "
                                      f"({flag} the 0.2 limit)", trail=list(trail), circle=wn, xr=(-5, 1), yr=(-5.2, 5.2))
    oss.append(i["overshoot"])
    if wn == 2.0:
        assert abs(i["settle"] - 9.80) < 0.01
    if wn == 4.0:
        assert abs(i["settle"] - 4.90) < 0.01 and np.allclose(sorted(roots(4, ZETA).imag), [-3.919, 3.919], atol=1e-3)
    trail.extend(roots(wn, ZETA))
    figs.append(fig)
    holds.append(16 if wn in (1.0, 2.0) else 30 if wn == 4.0 else 5)
assert max(oss) - min(oss) < 1e-3 and abs(oss[0] - 0.527) < 5e-4      # same overshoot for every wn
make_gif(figs, here / "wn_anim", fps=6, holds=holds, keys=[0, 4, 6, 8], cols=2, width=950)
