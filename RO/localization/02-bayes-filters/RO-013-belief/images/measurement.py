"""Measurement probability p(z | x) of the door sensor in every hallway cell: reading 'door' (left) is 0.6 likely in
front of a door and 0.2 at a wall; reading 'wall' (right) is 0.4 and 0.8. Each cell's two bars add to 1.
Run: python measurement.py -> measurement.png"""
from pathlib import Path

from plotly.subplots import make_subplots

from gifkit import GREEN
from hallplot import bars, door_labels, layout, likelihood

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.09,
                    subplot_titles=["reading z = 'door':  p(z = door | x)", "reading z = 'wall':  p(z = wall | x)"])
for c, z in ((1, 1), (2, 0)):
    bars(fig, likelihood(z), GREEN, row=1, col=c, ymax=1.0)
    door_labels(fig, 0.95, row=1, col=c)
    fig.update_xaxes(title="cell x", row=1, col=c)
fig.update_yaxes(title="probability of the reading", row=1, col=1)
assert (likelihood(1) + likelihood(0) == 1).all()
layout(fig, 1300, 480, top=70)
fig.write_image(here / "measurement.png", scale=1.5)
