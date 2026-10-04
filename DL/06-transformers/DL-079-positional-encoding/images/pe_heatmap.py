"""The positional encodings of 50 positions with d_model = 128, as a heatmap (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
pos, i = np.arange(50)[:, None], np.arange(64)[None, :]
angle = pos / 10000 ** (2 * i / 128)
pe = np.zeros((50, 128))
pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
fig = go.Figure(go.Heatmap(z=pe, colorscale="RdBu", zmin=-1, zmax=1, colorbar=dict(title="value")))
fig.update_layout(template="simple_white", width=950, height=520, font=FONT,
                  xaxis=dict(title="dimension of the encoding (0 to 127)"),
                  yaxis=dict(title="position in the sentence", autorange="reversed"),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "pe_heatmap.png", scale=2)
fig.write_image(here / "pe_heatmap.pdf")
