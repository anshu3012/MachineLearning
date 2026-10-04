"""Section 3's worked example: the query of "bank" against the keys of "money", "bank", "grows" (scores 4, 6, 2).
The softmax weights without and with the division by sqrt(3). Numbers from the text (asserted). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import RED, BLUE, FONT

here = Path(__file__).parent
q = np.array([1, 2, 1])
K = np.array([[2, 1, 0], [1, 2, 1], [0, 1, 0]])
s = K @ q
sm = lambda z: np.exp(z) / np.exp(z).sum()
raw, scaled = sm(s), sm(s / np.sqrt(3))
assert s.tolist() == [4, 6, 2] and np.allclose(raw.round(3), [0.117, 0.867, 0.016]) \
    and np.allclose(scaled.round(3), [0.223, 0.707, 0.070])
words = ["money", "bank", "grows"]
fig = go.Figure()
fig.add_bar(x=words, y=raw, name="softmax(scores): 4, 6, 2", marker_color=RED, text=[f"{v:.3f}" for v in raw], textposition="outside")
fig.add_bar(x=words, y=scaled, name="softmax(scores / √3): 2.31, 3.46, 1.15", marker_color=BLUE,
            text=[f"{v:.3f}" for v in scaled], textposition="outside")
fig.update_layout(template="simple_white", width=1000, height=420, font=dict(FONT, size=20), barmode="group",
                  xaxis=dict(title='key word (the query is "bank")'), yaxis=dict(title="attention weight", range=[0, 1.05]),
                  legend=dict(x=0.55, y=0.98), margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "example_weights.png", scale=2)
fig.write_image(here / "example_weights.pdf")
