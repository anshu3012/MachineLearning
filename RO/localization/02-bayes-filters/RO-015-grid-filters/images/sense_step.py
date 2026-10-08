"""The sense step of the histogram filter on the hallway: prior 0.1 everywhere, times p(door | cell) (0.6 at doors,
0.2 at walls), gives products 0.06 and 0.02 that add to 0.32; dividing by 0.32 gives 0.1875 and 0.0625.
Run: python sense_step.py -> sense_step.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, GREEN, GREY
from hallplot import bars, door_labels, layout, likelihood

here = Path(__file__).parent
prior = np.full(10, 0.1)
lik = likelihood(1)
prod = lik * prior
post = prod / prod.sum()
assert abs(prod.sum() - 0.32) < 1e-12
fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.09, vertical_spacing=0.2,
                    subplot_titles=["1. prior: 0.1 in every cell", "2. times p(door | cell)",
                                    "3. products: they add to 0.32", "4. divided by 0.32: the new belief"])
for (r, c), vals, color, ymax, fmt in (((1, 1), prior, BLUE, 0.8, 2), ((1, 2), lik, GREEN, 0.8, 2),
                                       ((2, 1), prod, GREY, 0.08, 2), ((2, 2), post, BLUE, 0.25, 4)):
    bars(fig, vals, color, row=r, col=c, ymax=ymax)
    if fmt == 4:
        fig.data[-1].text = [f"{v:.4f}" for v in vals]
    door_labels(fig, ymax * 0.93, row=r, col=c)
    fig.update_xaxes(title="cell", row=r, col=c)
layout(fig, 1300, 900, top=70)
fig.write_image(here / "sense_step.png", scale=1.5)
