"""Section 5: the leak in numbers. For each word of the decoder input, the share of its unmasked self-attention weight
that comes from words after it (Notebook, random untrained weights; data/weights_unmasked.csv). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import RED, GREY, FONT

here = Path(__file__).parent
W = pd.read_csv(here.parent / "data" / "weights_unmasked.csv", index_col=0)
A = W.to_numpy()
future = np.array([A[i, i + 1:].sum() for i in range(len(A))])
assert np.allclose(future.round(3), [0.866, 0.695, 0.437, 0.254, 0.0], atol=0.0015)
labels = [w.replace("<", "&lt;").replace(">", "&gt;") for w in W.index]
fig = go.Figure(go.Bar(x=labels, y=future, marker_color=RED, text=[f"{v:.3f}" for v in future], textposition="outside"))
fig.update_layout(template="simple_white", width=1000, height=420, font=dict(FONT, size=20), showlegend=False,
                  xaxis=dict(title="word being computed (in order)"),
                  yaxis=dict(title="weight taken from later words", range=[0, 1.05]),
                  margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "future_weight.png", scale=2)
fig.write_image(here / "future_weight.pdf")
