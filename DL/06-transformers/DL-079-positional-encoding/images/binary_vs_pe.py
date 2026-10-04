"""Binary counting next to the sine-cosine encoding: in both, the first columns change fastest (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
n = 16
bits = np.array([[(p >> b) & 1 for b in range(4)] for p in range(n)])      # bit 0 (fastest) first
pos, i = np.arange(n)[:, None], np.arange(4)[None, :]
angle = pos / 10000 ** (2 * i / 8)
pe = np.zeros((n, 8))
pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
fig = make_subplots(rows=1, cols=2, column_widths=[0.33, 0.67], horizontal_spacing=0.12,
                    subplot_titles=("binary code of the position", "sine-cosine encoding, d<sub>model</sub> = 8"))
fig.add_trace(go.Heatmap(z=bits, x=["bit 0", "bit 1", "bit 2", "bit 3"], colorscale=[[0, "white"], [1, "#4C78A8"]],
                         showscale=False, xgap=2, ygap=2, text=bits, texttemplate="%{text}"), 1, 1)
fig.add_trace(go.Heatmap(z=pe, x=[f"dim {k}" for k in range(8)], colorscale="RdBu", zmin=-1, zmax=1, xgap=2, ygap=2,
                         text=pe.round(2), texttemplate="%{text}", textfont=dict(size=11),
                         colorbar=dict(title="value")), 1, 2)
for c in (1, 2):
    fig.update_yaxes(title="position" if c == 1 else None, autorange="reversed", tickvals=list(range(n)), row=1, col=c)
fig.update_layout(template="simple_white", width=1100, height=620, font=FONT, margin=dict(l=70, r=20, t=50, b=40))
fig.write_image(here / "binary_vs_pe.png", scale=2)
fig.write_image(here / "binary_vs_pe.pdf")
