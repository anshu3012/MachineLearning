"""Dot products between the positional encodings of positions 0-99 (d_model = 128): equal along every diagonal,
so they depend only on the distance k. Right: the dot product against k (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, FONT

here = Path(__file__).parent
pos, i = np.arange(100)[:, None], np.arange(64)[None, :]
angle = pos / 10000 ** (2 * i / 128)
pe = np.zeros((100, 128))
pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
dk = pd.read_csv(here.parent / "data" / "dot_vs_offset.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("PE(p) · PE(q)", "PE(p) · PE(p + k), any p"))
fig.add_trace(go.Heatmap(z=pe @ pe.T, colorscale="Viridis", colorbar=dict(x=0.43, title="dot")), 1, 1)
fig.add_trace(go.Scatter(x=dk.k, y=dk["dot"], mode="lines", line=dict(color=BLUE, width=3), showlegend=False), 1, 2)
fig.update_xaxes(title="position q", row=1, col=1)
fig.update_yaxes(title="position p", autorange="reversed", row=1, col=1)
fig.update_xaxes(title="distance k", row=1, col=2)
fig.update_yaxes(title="dot product", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "pe_dot.png", scale=2)
fig.write_image(here / "pe_dot.pdf")
