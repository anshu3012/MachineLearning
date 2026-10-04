"""Section 7: the new memory lies between the old memory and the candidate. For each aspect, a segment from the old
value h_{t-1} to the candidate value; the new value sits a share z of the way along it. Sentence 4 of the story.
Run: python blend.py  -> blend.png (Plotly dumbbell chart: positions along segments)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, GREY, PURPLE, RED

HERE = Path(__file__).parent
ASPECTS = ["power", "conflict", "tragedy", "revenge"]
old, cand, z = np.array([0.6, 0.6, 0.7, 0.1]), np.array([0.7, 0.2, 0.1, 0.2]), np.array([0.1, 0.7, 0.8, 0.2])
new = (1 - z) * old + z * cand
assert np.allclose(np.round(new, 2), [0.61, 0.32, 0.22, 0.12])                # section 8.4

fig = go.Figure()
for k, a in enumerate(ASPECTS):
    fig.add_trace(go.Scatter(x=[old[k], cand[k]], y=[a, a], mode="lines", line=dict(color=GREY, width=3),
                             showlegend=False))
    fig.add_annotation(x=new[k], y=a, yshift=-30, showarrow=False, font=dict(size=20, color=PURPLE),
                       text=f"z = {z[k]:g}: {z[k]:.0%} of the way")
fig.add_trace(go.Scatter(x=old, y=ASPECTS, mode="markers", name="old memory h<sub>t−1</sub>",
                         marker=dict(size=20, color=RED)))
fig.add_trace(go.Scatter(x=cand, y=ASPECTS, mode="markers", name="candidate h̃<sub>t</sub>",
                         marker=dict(size=20, color=BLUE)))
fig.add_trace(go.Scatter(x=new, y=ASPECTS, mode="markers+text", name="new memory h<sub>t</sub>",
                         text=[f"{v:.2f}" for v in new], textposition="top center", textfont=dict(size=20),
                         marker=dict(size=22, color=PURPLE, symbol="diamond")))
fig.update_yaxes(range=[3.6, -0.5])
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="value", range=[0, 0.8]), legend=dict(orientation="h", y=1.12, x=0),
                  margin=dict(l=110, r=30, t=60, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "blend.png", scale=2)
