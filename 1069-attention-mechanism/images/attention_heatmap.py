"""Attention weights of the trained attention model on one real test sentence: one row per French word written,
one column per English word read (Plotly heatmap)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "attention_weights.csv", index_col=0, keep_default_na=False)
rows = [r.replace("<", "&lt;") for r in w.index]
fig = go.Figure(go.Heatmap(z=w.values, x=list(w.columns), y=rows, colorscale="Oranges", zmin=0, zmax=1,
                           text=w.values.round(2), texttemplate="%{text}", textfont=dict(size=12),
                           colorbar=dict(title="α")))
fig.update_layout(template="simple_white", width=950, height=110 + 42 * len(rows), font=FONT,
                  xaxis=dict(title="English (input)", side="top", tickangle=-30),
                  yaxis=dict(title="French (output)", autorange="reversed"), margin=dict(l=110, r=20, t=110, b=20))
fig.write_image(here / "attention_heatmap.png", scale=2)
fig.write_image(here / "attention_heatmap.pdf")
