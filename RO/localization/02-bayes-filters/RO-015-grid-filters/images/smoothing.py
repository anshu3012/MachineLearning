"""Filtered against smoothed belief at t = 1. Filtering uses only the first reading: 0.1875 on each door. Smoothing
also uses the later readings (door at t = 2, wall at t = 3): cell 1 rises to 0.36, cells 3 and 7 fall to 0.09.
Run: python smoothing.py -> smoothing.png"""
from pathlib import Path

from plotly.subplots import make_subplots

from gifkit import BLUE, PURPLE
from hallplot import bars, door_labels, layout
from hmmrun import FILTERED, SMOOTHED

here = Path(__file__).parent
assert abs(SMOOTHED[0][1] - 0.3606) < 1e-4
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.09,
                    subplot_titles=["filtered: p(x<sub>1</sub> | z<sub>1</sub>)",
                                    "smoothed: p(x<sub>1</sub> | z<sub>1</sub>, z<sub>2</sub>, z<sub>3</sub>)"])
bars(fig, FILTERED[0], BLUE, row=1, col=1, ymax=0.45)
bars(fig, SMOOTHED[0], PURPLE, row=1, col=2, ymax=0.45)
for c in (1, 2):
    door_labels(fig, 0.43, row=1, col=c)
    fig.update_xaxes(title="cell x<sub>1</sub>", row=1, col=c)
fig.update_yaxes(title="probability", row=1, col=1)
layout(fig, 1300, 480, top=70)
fig.write_image(here / "smoothing.png", scale=1.5)
