"""Why parameter sharing matters: the weights of a first layer with 10 nodes, for a 10,000-word one-hot
vocabulary, as the review length grows. A dense layer on the stacked words needs T x 10,000 x 10 + 10 weights;
a SimpleRNN layer needs 100,110 for any length (Keras count_params in the Notebook). Plotly, log scale."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, FONT

here = Path(__file__).parent
V, H = 10_000, 10
T = np.array([10, 50, 100, 500, 1000, 2494])
dense = T * V * H + H
rnn = V * H + H * H + H                                   # input weights + recurrent weights + biases
assert dense[2] == 10_000_010 and rnn == 100_110          # the Note's Keras counts
fig = go.Figure()
fig.add_scatter(x=T, y=dense, mode="lines+markers", name="dense layer on the padded input", line=dict(color=RED, width=4),
                marker=dict(size=11))
fig.add_scatter(x=T, y=[rnn] * len(T), mode="lines+markers", name="SimpleRNN layer (same weights at every step)",
                line=dict(color=BLUE, width=4), marker=dict(size=11))
fig.add_annotation(x=np.log10(100), y=np.log10(dense[2]), text="10,000,010 for 100 words", showarrow=True,
                   ax=-120, ay=-50, font=dict(size=19))
fig.add_annotation(x=np.log10(1000), y=np.log10(rnn), text="100,110 for any length", showarrow=False, yshift=-28,
                   font=dict(size=19, color=BLUE))
fig.update_layout(template="simple_white", width=1000, height=480, font=dict(FONT, size=20),
                  xaxis=dict(type="log", title="review length T (words)", tickvals=list(T), ticktext=[f"{t:,}" for t in T]),
                  yaxis=dict(type="log", title="weights in the first layer", exponentformat="power", dtick=1),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=90, r=20, t=20, b=70))
fig.write_image(here / "weights_vs_length.png", scale=2)
fig.write_image(here / "weights_vs_length.pdf")
