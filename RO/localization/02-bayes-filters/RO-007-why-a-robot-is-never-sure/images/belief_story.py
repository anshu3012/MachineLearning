"""Moving spreads the belief, sensing sharpens it. The robot knows it is in cell 3; two noisy moves of 2 cells spread
its belief over cells 5-9 (0.01, 0.16, 0.66, 0.16, 0.01); the noisy sensor reads "door" (0.6 at a door, 0.2 at a
wall), which lifts cell 7 to 0.853. Run: python belief_story.py -> belief_story.gif, belief_story_frames.png"""
from pathlib import Path

import numpy as np
from corrdraw import DOORS, SENSE_DOOR, panel, predict
from gifkit import make_gif

here = Path(__file__).parent
b2 = np.eye(10)[3]
b3 = predict(b2)
b4 = predict(b3)
lik = np.array([SENSE_DOOR[i in DOORS] for i in range(10)])
b4z = b4 * lik / (b4 * lik).sum()
assert np.allclose(b4[5:10], [0.01, 0.16, 0.66, 0.16, 0.01]) and abs(b4z[7] - 0.853) < 5e-4
figs = [panel(b2, "the robot is sure it is in cell 3", truth=3),
        panel(b3, 'control "move 2": the belief spreads', truth=5),
        panel(b4, 'control "move 2" again: it spreads more', truth=7),
        panel(b4z, 'reading "door" (noisy sensor): cell 7 rises to 0.85', truth=7)]
make_gif(figs, here / "belief_story", fps=1, holds=[3, 4, 4, 6], keys=[0, 1, 2, 3], cols=2, width=900)
