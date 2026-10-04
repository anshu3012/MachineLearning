"""Mutually exclusive events on simulated rolls (Plotly): one million rolls of one fair die (seed 0), A = "shows 3",
B = "shows 6". Left: P(A) over all rolls is about 1/6, but among the rolls where B happened it is exactly 0.
Right: the share of rolls showing 3 or 6 is about 1/3 = 1/6 + 1/6, the addition rule."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
r = np.random.default_rng(0).integers(1, 7, 1_000_000)
pA, pAgB, pB = (r == 3).mean(), (r[r == 6] == 3).mean(), (r == 6).mean()
pAuB = ((r == 3) | (r == 6)).mean()
assert abs(pA - 1 / 6) < 0.002 and pAgB == 0 and abs(pAuB - 1 / 3) < 0.002 and abs(pAuB - (pA + pB)) < 1e-12
fig = make_subplots(1, 2, horizontal_spacing=0.15, subplot_titles=["knowing B rules A out", "the addition rule"])
fig.update_annotations(font_size=22)
fig.add_trace(go.Bar(x=["P(A): all rolls", "P(A | B): rolls showing 6"], y=[pA, pAgB], marker_color=[BLUE, RED],
                     text=[f"{pA:.4f}", "0 exactly"], textposition="outside", textfont=dict(size=20)), 1, 1)
fig.add_trace(go.Bar(x=["P(A)", "P(B)", "P(A ∪ B)"], y=[pA, pB, pAuB], marker_color=[BLUE, ORANGE, GREEN],
                     text=[f"{v:.4f}" for v in (pA, pB, pAuB)], textposition="outside", textfont=dict(size=20)), 1, 2)
fig.update_yaxes(title="share of rolls", range=[0, 0.42], row=1, col=1)
fig.update_yaxes(range=[0, 0.42], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=60))
fig.write_image(here / "die_sim.png", scale=2)
