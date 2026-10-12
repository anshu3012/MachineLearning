"""The Nyquist plot of the heading loop L(s) = (0.8 s + 4) e^{-s tau}/s^2 traced as s walks the Nyquist contour, with
a string from -1 counting clockwise turns. Delay 0.1 s: the string ends where it started, N = 0, so Z = N + P = 0:
stable. Delay 0.25 s: N = 2 clockwise, Z = 2: two closed-loop poles in the right half-plane, the growing swing of
Figure 1. Drawn with the radial squeeze of loopkit.squeeze (stated in every frame).
Run: python nyquist_anim.py -> nyquist_anim.gif, nyquist_anim_frames.png"""
from pathlib import Path

from gifkit import make_gif
from loopkit import L_head
from nyqdraw import frames

here = Path(__file__).parent
figs, holds, keys = [], [], []
for tau, want in [(0.1, 0), (0.25, 2)]:
    fs, n = frames(lambda s: L_head(s, tau), f"heading loop, delay T<sub>d</sub> = {tau:g} s",
                   extra=f"N = {want} clockwise turns, P = 0, so Z = N + P = {want}"
                   + (": stable" if want == 0 else ": unstable"))
    assert abs(n - want) < 1e-6
    figs += fs
    holds += [3] + [1] * (len(fs) - 2) + [14]
    keys += [len(figs) - len(fs) + 11, len(figs) - 1]
make_gif(figs, here / "nyquist_anim", fps=4, holds=holds, keys=keys, cols=2, width=700)
