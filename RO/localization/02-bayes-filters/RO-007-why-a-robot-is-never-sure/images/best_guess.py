"""One reading fits three cells. A robot that keeps all three (bars) finds itself after "move 2" and a second "door";
a robot that keeps one best guess (purple triangle, here cell 7) is contradicted and has nothing left.
Moves and readings are exact here. Run: python best_guess.py -> best_guess.gif, best_guess_frames.png"""
from pathlib import Path

import numpy as np
from corrdraw import DOORS, panel
from gifkit import make_gif

here = Path(__file__).parent
uni = np.full(10, 0.1)
z1 = np.array([1 / 3 if i in DOORS else 0 for i in range(10)])
u2 = np.roll(z1, 2)                                   # exact move 2 cells: 1, 3, 7 -> 3, 5, 9
z2 = np.where([i in DOORS for i in range(10)], u2, 0)
z2 = z2 / z2.sum()
assert list(np.nonzero(u2)[0]) == [3, 5, 9] and z2[3] == 1.0
figs = [panel(uni, "t = 1, before any reading: no idea yet, 0.1 each", truth=1),
        panel(z1, 't = 1, reading "door": three cells fit, 0.33 each', truth=1, guess=7),
        panel(u2, 't = 2, control "move 2": all three candidates move', truth=3, guess=9),
        panel(z2, 't = 2, reading "door": only cell 3 fits both readings', truth=3, guess=9,
              guess_text="guess 9: lost")]
make_gif(figs, here / "best_guess", fps=1, holds=[3, 4, 4, 6], keys=[0, 1, 2, 3], cols=2, width=900)
