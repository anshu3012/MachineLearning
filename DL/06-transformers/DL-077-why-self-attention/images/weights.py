"""The three weight matrices of the Notebook (untrained networks): Luong dot attention between French and English
(3 x 4), self-attention on the English embeddings without projections (4 x 4), and with W_Q, W_K, W_V and
scaling (4 x 4) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
files = [("weights_luong", "Luong: French → English"), ("weights_self_plain", "self, no projections"),
         ("weights_self", "self, with W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub>")]
fig = make_subplots(1, 3, subplot_titles=[t for _, t in files], horizontal_spacing=0.07)
for k, (f, _) in enumerate(files, 1):
    w = pd.read_csv(here.parent / "data" / f"{f}.csv", index_col=0)
    fig.add_trace(go.Heatmap(z=w.values, x=list(w.columns), y=list(w.index), zmin=0, zmax=1, colorscale="Blues",
                             showscale=k == 3, text=w.values.round(2), texttemplate="%{text}",
                             colorbar=dict(title="weight")), 1, k)
    fig.update_yaxes(autorange="reversed", scaleanchor=f"x{k if k > 1 else ''}", row=1, col=k)
fig.update_yaxes(title_text="query word", row=1, col=1)
fig.update_xaxes(title_text="key word")
fig.update_layout(template="simple_white", width=1150, height=430, font=FONT, margin=dict(l=90, r=20, t=50, b=60))
fig.write_image(here / "weights.png", scale=2)
fig.write_image(here / "weights.pdf")
