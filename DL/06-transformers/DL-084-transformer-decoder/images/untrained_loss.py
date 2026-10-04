"""Section 9: before training, each correct French word gets about 1/V of the probability, so the loss is close to
ln V. The Note's (Notebook's) probabilities of the 5 target words, as multiples of 1/V with V = 8,004; per-position
loss -ln P, their mean (9.39) and ln V (8.99).
Run: python untrained_loss.py  -> untrained_loss.png (Plotly bars and reference lines)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import GREY, ORANGE, RED

HERE = Path(__file__).parent
V = 8004
targets = ["nous", "sommes", "amis", ".", "&lt;end&gt;"]
pV = np.array([0.76, 0.57, 0.79, 0.38, 1.04])                # P(target) x V, from the Notebook
loss = -np.log(pV / V)
assert round(loss.mean(), 2) == 9.39 and round(np.log(V), 2) == 8.99

fig = go.Figure(go.Bar(x=[f"pos {i + 1}: {t}<br>P = {v:.2f}/V" for i, (t, v) in enumerate(zip(targets, pV))], y=loss, marker_color=ORANGE,
                       text=[f"{l:.2f}" for l in loss], textposition="outside"))
fig.add_hline(y=loss.mean(), line=dict(color=RED, width=3, dash="dash"), layer="below", opacity=1)
fig.add_annotation(x=1.0, xref="paper", xanchor="left", y=loss.mean(), text=f" mean loss {loss.mean():.2f}",
                   showarrow=False, font=dict(color=RED, size=20), yshift=10)
fig.add_hline(y=np.log(V), line=dict(color=GREY, width=3, dash="dot"), layer="below", opacity=1)
fig.add_annotation(x=1.0, xref="paper", xanchor="left", y=np.log(V), text=f" ln V = {np.log(V):.2f}<br> (uniform guess)",
                   showarrow=False, font=dict(color=GREY, size=20), yshift=-14)
fig.update_layout(template="simple_white", width=1100, height=500, font=dict(family="Latin Modern Roman", size=20),
                  yaxis=dict(title="−ln P(correct word)", range=[7.5, 10.6]), margin=dict(l=80, r=200, t=30, b=90))

if __name__ == "__main__":
    fig.write_image(HERE / "untrained_loss.png", scale=2)
