"""Moving without sensing: the robot starts sure it is in cell 1 and repeats 'move 2' with no readings. Every move
blurs the belief, until it is almost flat at 0.1 per cell: the stationary distribution of this loop.
Run: python lose_info.py -> lose_info.gif, lose_info_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import ORANGE, make_gif
from hallplot import bars, layout, predict

here = Path(__file__).parent
SHOW = [0, 1, 2, 3, 5, 10, 20, 40, 80]
bel, beliefs = np.zeros(10), {}
bel[1] = 1.0
for k in range(max(SHOW) + 1):
    if k in SHOW:
        beliefs[k] = bel.copy()
    bel = predict(bel)
assert abs(beliefs[80].max() - 0.1) < 0.01


def frame(k):
    fig = go.Figure()
    bars(fig, beliefs[k], ORANGE, ymax=1.1)
    fig.update_xaxes(title="cell")
    fig.update_yaxes(title="predicted belief")
    layout(fig, 900, 480, title=f"after {k} move{'' if k == 1 else 's'} without a reading: highest cell {beliefs[k].max():.2f}")
    return fig


figs = [frame(k) for k in SHOW]
make_gif(figs, here / "lose_info", fps=2, holds=[3] * (len(SHOW) - 1) + [8], keys=[1, 3, 5, 8], cols=2, width=800)
