"""Attention weights of a 10-word IMDB sentence with random d = 512 embeddings and weights: softmax(QK^T)
against softmax(QK^T / sqrt(d)) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
fig = make_subplots(1, 2, subplot_titles=["softmax(QKᵀ)", "softmax(QKᵀ / √512)"], horizontal_spacing=0.14)
for k, name in ((1, "unscaled"), (2, "scaled")):
    w = pd.read_csv(here.parent / "data" / f"weights_{name}.csv", index_col=0)
    fig.add_trace(go.Heatmap(z=w.values, x=list(w.columns), y=list(w.index), zmin=0, zmax=1, colorscale="Blues",
                             showscale=k == 2, text=w.values.round(2), texttemplate="%{text}",
                             textfont=dict(size=10), colorbar=dict(title="weight")), 1, k)
fig.update_yaxes(autorange="reversed", title_text="query word")
fig.update_yaxes(title_text="", row=1, col=2)
fig.update_xaxes(title_text="key word", tickangle=-45)
fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, margin=dict(l=90, r=20, t=40, b=100))
fig.write_image(here / "heatmaps.png", scale=2)
fig.write_image(here / "heatmaps.pdf")
