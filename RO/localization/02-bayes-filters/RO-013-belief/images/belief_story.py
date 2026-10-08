"""The belief over the 10 hallway cells as the robot reads 'door', moves 2 cells, and reads 'door' again.
Stages: uniform -> after the first 'door' -> moved (shift by 2) -> motion uncertain (blur 0.1/0.8/0.1) -> after the
second 'door'. The black triangle marks the true cell, which the robot does not know.
Run: python belief_story.py -> belief_story.gif, belief_story_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, make_gif
from hallplot import bars, door_labels, layout, predict, story

here = Path(__file__).parent
b0, b1, bb2, b2 = story()
shifted = np.roll(b1, 2)
assert np.allclose(predict(b1), bb2) and abs(b2[3] - 0.3095) < 1e-4

STAGES = [  # (title, belief, true cell)
    ("1. No idea yet: every cell 0.1", b0, 1),
    ("2. Reads 'door': three bumps, one per door", b1, 1),
    ("3. Moves 2 cells right: the bumps move with it", shifted, 3),
    ("4. The move is uncertain: the bumps spread out", bb2, 3),
    ("5. Reads 'door' again: one main bump, at cell 3", b2, 3),
]


def frame(title, bel, true_cell):
    fig = go.Figure()
    bars(fig, bel, BLUE, ymax=0.5)
    door_labels(fig, 0.48)
    fig.add_annotation(x=true_cell, y=bel[true_cell] + 0.035, text="<b>true cell</b>", showarrow=True, ax=0, ay=-42, arrowhead=2,
                       arrowsize=1.4, arrowwidth=2.5, font=dict(size=17))
    fig.update_yaxes(title="belief (probability)", range=[0, 0.5])
    fig.update_xaxes(title="cell", title_standoff=20)
    layout(fig, 900, 520, title=title)
    return fig


figs, holds, keys = [], [], []
prev = None
for title, bel, cell in STAGES:
    if prev is not None:                        # short smooth change from the previous stage
        for a in (0.33, 0.67):
            figs.append(frame(title, (1 - a) * prev + a * bel, cell))
            holds.append(1)
    keys.append(len(figs))
    figs.append(frame(title, bel, cell))
    holds.append(10)
    prev = bel
holds[-1] = 18
make_gif(figs, here / "belief_story", fps=5, holds=holds, keys=keys[1:], cols=2, width=850)
