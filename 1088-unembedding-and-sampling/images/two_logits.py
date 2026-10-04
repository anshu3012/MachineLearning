"""Section 5.1's worked example: two logits z = (2, 1) through the softmax at T = 0.5, 1 and 2.
Low T sharpens, high T flattens. Numbers from the text (asserted). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
z = np.array([2.0, 1.0])
rows = []
for T in (0.5, 1.0, 2.0):
    p = np.exp(z / T) / np.exp(z / T).sum()
    rows.append((T, p))
assert [tuple(p.round(2)) for _, p in rows] == [(0.88, 0.12), (0.73, 0.27), (0.62, 0.38)]
fig = go.Figure()
labels = [f"T = {T:g}<br>logits / T = ({2 / T:g}, {1 / T:g})" for T, _ in rows]
fig.add_bar(x=labels, y=[p[0] for _, p in rows], name="token with logit 2", marker_color=BLUE,
            text=[f"{p[0]:.2f}" for _, p in rows], textposition="outside")
fig.add_bar(x=labels, y=[p[1] for _, p in rows], name="token with logit 1", marker_color=ORANGE,
            text=[f"{p[1]:.2f}" for _, p in rows], textposition="outside")
fig.update_layout(template="simple_white", width=1000, height=430, font=dict(FONT, size=19), barmode="group",
                  yaxis=dict(title="probability", range=[0, 1.05]), legend=dict(x=0.62, y=0.98),
                  margin=dict(l=70, r=20, t=20, b=80))
fig.write_image(here / "two_logits.png", scale=2)
fig.write_image(here / "two_logits.pdf")
