"""Section 8 worked example: four logits of a toy vocabulary turned into probabilities by the softmax.
Run: python softmax_toy.py  -> softmax_toy.png (Plotly: logits and probabilities side by side)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREY

HERE = Path(__file__).parent
words, u = ["nous", "sommes", "amis", "&lt;end&gt;"], np.array([2.0, 1.0, 0.5, -1.0])
e = np.exp(u)
p = e / e.sum()
assert np.allclose(e.round(2), [7.39, 2.72, 1.65, 0.37]) and round(e.round(2).sum(), 2) == 12.13   # the Note adds the rounded values
assert np.allclose(p.round(3), [0.609, 0.224, 0.136, 0.030])

fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=["logits u (linear layer)", "probabilities (softmax)"])
fig.add_trace(go.Bar(x=words, y=u, marker_color=GREY, text=[f"{v:.1f}" for v in u], textposition="outside"), 1, 1)
fig.add_trace(go.Bar(x=words, y=p, marker_color=BLUE, text=[f"{v:.3f}" for v in p], textposition="outside"), 1, 2)
fig.update_yaxes(range=[-1.6, 2.6], zeroline=True, zerolinecolor=GREY, row=1, col=1)
fig.update_yaxes(range=[0, 0.75], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=22), margin=dict(l=60, r=20, t=60, b=50))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "softmax_toy.png", scale=2)
