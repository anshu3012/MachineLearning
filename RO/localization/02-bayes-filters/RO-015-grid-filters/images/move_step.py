"""The move step: the belief after the first 'door' (left), shifted exactly 2 cells (middle), and with the motion
uncertainty 0.1/0.8/0.1 (right): 0.1875 becomes 0.1625. Run: python move_step.py -> move_step.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, ORANGE
from hallplot import bars, door_labels, layout, predict, story

here = Path(__file__).parent
b0, b1, bb2, b2 = story()
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07,
                    subplot_titles=["belief after 'door'", "exact move: shift by 2", "real move: shift and blur"])
for c, vals, color in ((1, b1, BLUE), (2, np.roll(b1, 2), ORANGE), (3, bb2, ORANGE)):
    bars(fig, vals, color, row=1, col=c, ymax=0.25)
    fig.data[-1].text = [f"{v:.4f}" for v in vals]
    fig.data[-1].textfont.size = 11
    door_labels(fig, 0.235, row=1, col=c)
    fig.update_xaxes(title="cell", row=1, col=c)
fig.update_yaxes(title="probability", row=1, col=1)
layout(fig, 1600, 480, top=70)
fig.write_image(here / "move_step.png", scale=1.5)
