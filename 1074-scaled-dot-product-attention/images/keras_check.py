"""Section 7's result: the attention weights of "money bank grows" computed by hand with NumPy, as printed in the
Note; Keras' MultiHeadAttention with one head returns the same matrix (Notebook). Plotly heatmap."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
A = np.array([[0.015, 0.670, 0.316], [0.159, 0.575, 0.267], [0.250, 0.116, 0.634]])
assert np.allclose(A.sum(1), 1, atol=0.002)
w = ["money", "bank", "grows"]
fig = go.Figure(go.Heatmap(z=A, x=w, y=w, colorscale="Blues", zmin=0, zmax=1, text=A, texttemplate="%{text:.3f}",
                           textfont=dict(size=24), colorbar=dict(title="weight")))
fig.update_layout(template="simple_white", width=700, height=520, font=dict(FONT, size=20),
                  xaxis=dict(title="key", side="top"), yaxis=dict(title="query", autorange="reversed"),
                  margin=dict(l=90, r=20, t=80, b=20))
fig.write_image(here / "keras_check.png", scale=2)
fig.write_image(here / "keras_check.pdf")
