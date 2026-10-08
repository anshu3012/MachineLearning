"""Predicted belief and belief at t = 2: after the move (left, orange) and after the reading 'door' (right, blue).
Run: python belbar.py -> belbar.png"""
from pathlib import Path

from plotly.subplots import make_subplots

from gifkit import BLUE, ORANGE
from hallplot import bars, door_labels, layout, story

here = Path(__file__).parent
b0, b1, bb2, b2 = story()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.09,
                    subplot_titles=["predicted belief: after u<sub>2</sub> = move 2, before z<sub>2</sub>",
                                    "belief: after z<sub>2</sub> = door"])
bars(fig, bb2, ORANGE, row=1, col=1, ymax=0.4)
bars(fig, b2, BLUE, row=1, col=2, ymax=0.4)
for c in (1, 2):
    door_labels(fig, 0.38, row=1, col=c)
    fig.update_xaxes(title="cell x<sub>2</sub>", row=1, col=c)
fig.update_yaxes(title="probability", row=1, col=1)
layout(fig, 1300, 480, top=70)
fig.write_image(here / "belbar.png", scale=1.5)
