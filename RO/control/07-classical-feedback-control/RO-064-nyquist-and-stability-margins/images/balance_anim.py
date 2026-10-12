"""When a Bode plot misleads: a balancing robot (normalised inverted pendulum, Feedback Systems Example 10.5) under
PD control, L(s) = (s + 2)/(s^2 - 1). L has one pole in the right half-plane (s = 1, P = 1). The Nyquist plot starts
at L(0) = -2 and goes once counter-clockwise round -1: N = -1, so Z = N + P = 0: stable (closed-loop poles
-0.5 +- 0.866j), although the gain is 2 where the phase is -180 degrees.
Run: python balance_anim.py -> balance_anim.gif, balance_anim_frames.png"""
from pathlib import Path

import numpy as np
from gifkit import make_gif
from nyqdraw import frames

here = Path(__file__).parent
Lb = lambda s: (s + 2) / (s ** 2 - 1)
assert abs(Lb(0) + 2) < 1e-12
assert np.allclose(sorted(np.roots([1, 1, 1]).imag), [-np.sqrt(3) / 2, np.sqrt(3) / 2])   # s^2 - 1 + s + 2 = 0
figs, n = frames(Lb, "balancing robot, L(s) = (s + 2)/(s² − 1)", small=False,
                 extra="N = −1 (one counter-clockwise turn), P = 1, so Z = N + P = 0: stable")
assert abs(n + 1) < 1e-3
make_gif(figs, here / "balance_anim", fps=4, holds=[3] + [1] * (len(figs) - 2) + [14], keys=[6, len(figs) - 1],
         cols=2, width=700)
