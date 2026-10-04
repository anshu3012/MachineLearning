"""Section 5.3's worked example: the probability the decoder gave each correct word and its loss -ln p.
Values from the text (0.1, 0.1, 0.4); total 5.52, mean 1.84. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, FONT

here = Path(__file__).parent
words, p = ["soch", "lo", "<end>"], np.array([0.1, 0.1, 0.4])
L = -np.log(p)
assert round(L.sum(), 2) == 5.52 and round(L.mean(), 2) == 1.84
labels = [f"step {i + 1}: {w}" for i, w in enumerate(words)]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("probability given to the correct word", "loss at the step, -ln p"))
fig.add_bar(x=labels, y=p, marker_color=BLUE, text=[f"{v:.1f}" for v in p], textposition="outside", row=1, col=1)
fig.add_bar(x=labels, y=L, marker_color=RED, text=[f"{v:.3f}" for v in L], textposition="outside", row=1, col=2)
fig.update_yaxes(range=[0, 1], row=1, col=1)
fig.update_yaxes(range=[0, 2.8], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=400, font=dict(FONT, size=19), showlegend=False,
                  margin=dict(l=50, r=20, t=50, b=50))
fig.write_image(here / "step_loss.png", scale=2)
fig.write_image(here / "step_loss.pdf")
