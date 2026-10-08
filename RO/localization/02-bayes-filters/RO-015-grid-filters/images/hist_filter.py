"""The histogram filter over seven steps. The true robot starts in cell 1 and moves 2 cells each step (cells 1, 3, 5,
7, 9, 1, 3). The readings are correct except at t = 5, where the sensor says 'door' at the wall of cell 9. Orange:
predicted belief after the move; blue: belief after the reading; arrow: true cell.
Run: python hist_filter.py -> hist_filter.gif, hist_filter_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, ORANGE, make_gif
from hallplot import DOOR, bars, door_labels, layout, predict, update

here = Path(__file__).parent
cells = [(1 + 2 * t) % 10 for t in range(7)]
readings = [int(DOOR[c]) for c in cells]
readings[4] = 1                                   # wrong reading at t = 5
NAME = {1: "door", 0: "wall"}


def frame(title, bel, color, cell):
    fig = go.Figure()
    bars(fig, bel, color, ymax=0.72)
    door_labels(fig, 0.7)
    fig.add_annotation(x=cell, y=bel[cell] + 0.045, text="<b>true cell</b>", showarrow=True, ax=0, ay=-40,
                       arrowhead=2, arrowsize=1.4, arrowwidth=2.5, font=dict(size=17))
    fig.update_xaxes(title="cell")
    fig.update_yaxes(title="probability")
    layout(fig, 900, 520, title=title)
    return fig


figs, holds, keys = [], [], []
bel = update(np.full(10, 0.1), readings[0])
figs.append(frame(f"t = 1: reads '{NAME[readings[0]]}'", bel, BLUE, cells[0]))
holds.append(8)
log = [(1, bel.argmax(), bel.max())]
for t in range(1, 7):
    bb = predict(bel)
    figs.append(frame(f"t = {t + 1}: after 'move 2' (predicted)", bb, ORANGE, cells[t]))
    holds.append(5)
    bel = update(bb, readings[t])
    wrong = "  (wrong reading!)" if t == 4 else ""
    figs.append(frame(f"t = {t + 1}: reads '{NAME[readings[t]]}'{wrong}", bel, BLUE, cells[t]))
    holds.append(8)
    log.append((t + 1, bel.argmax(), bel.max()))
holds[-1] = 16
assert [a for _, a, _ in log] == [1, 3, 5, 7, 3, 1, 3] and abs(log[4][2] - 0.315) < 1e-3
make_gif(figs, here / "hist_filter", fps=5, holds=holds, keys=[6, 8, 10, 12], cols=2, width=850)
