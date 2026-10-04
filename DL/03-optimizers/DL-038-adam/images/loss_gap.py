"""Section 6's table as a picture: for the five optimizers of Figure 1 on the students data (shared.py: same
settings and runs), the loss above its minimum at every step, on a log scale. The dashed line is the 0.01 target of
the table. Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, GREEN, ORANGE, PURPLE, RED
from shared import BEST, SETTINGS, loss, run, steps_to

HERE = Path(__file__).parent
COL = [BLUE, ORANGE, GREEN, PURPLE, RED]
best = loss(BEST)
fig = go.Figure()
reached = {}
for (name, (kind, eta)), c in zip(SETTINGS.items(), COL):
    P = run(kind, eta)
    gap = np.array([loss(p) for p in P]) - best
    reached[name] = steps_to(P)
    fig.add_scatter(x=np.arange(len(gap)), y=np.maximum(gap, 1e-9), mode="lines", name=f"{name}: {reached[name]} steps",
                    line=dict(color=c, width=4 if kind == "adam" else 2.5))
assert list(reached.values()) == [61, 64, 44, 48, 42], reached
fig.add_hline(y=0.01, line=dict(color="black", width=2, dash="dash"), opacity=1)
fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Loss above its minimum, step by step (legend: steps to get within 0.01)", x=0.5,
                             font=dict(size=21)),
                  xaxis=dict(title="step", range=[0, 150]),
                  yaxis=dict(title="loss − minimum loss (log scale)", type="log", range=[-6, 2.3]),
                  legend=dict(x=0.55, y=0.98, font=dict(size=17)), margin=dict(l=90, r=30, t=70, b=70))
fig.write_image(HERE / "loss_gap.png", scale=2)
