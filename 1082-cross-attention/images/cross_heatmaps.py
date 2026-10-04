"""Cross-attention weights (mean of 4 heads) of the small trained English -> French transformer, two held-out pairs (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
cw = pd.read_csv(here.parent / "data" / "cross_weights.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.16,
                    subplot_titles=["Tom likes to eat ice cream.", "I want ice cream for dessert."])
for col, k in ((1, 0), (2, 1)):
    a = cw[cw.pair == k]
    m = a.pivot(index="query_pos", columns="key_pos", values="weight").values
    rows = a.drop_duplicates("query_pos").sort_values("query_pos").predicts.tolist()
    cols = a.drop_duplicates("key_pos").sort_values("key_pos").key.tolist()
    fig.add_trace(go.Heatmap(z=m, x=list(range(len(cols))), y=list(range(len(rows))), zmin=0, zmax=1, colorscale="Blues",
                             text=[[f"{v:.2f}".lstrip("0") if v >= 0.1 else "" for v in r] for r in m],
                             texttemplate="%{text}", textfont=dict(size=12), showscale=(col == 2),
                             colorbar=dict(title="weight")), row=1, col=col)
    fig.update_xaxes(tickmode="array", tickvals=list(range(len(cols))), ticktext=cols, row=1, col=col)
    fig.update_yaxes(tickmode="array", tickvals=list(range(len(rows))), ticktext=rows, autorange="reversed", row=1, col=col)
fig.update_xaxes(title_text="English word (key and value, from the encoder)")
fig.update_yaxes(title_text="French word being predicted (query)", col=1)
fig.update_layout(template="simple_white", width=1300, height=620, font=FONT, margin=dict(l=110, r=20, t=50, b=80))
fig.write_image(here / "cross_heatmaps.png", scale=2)
fig.write_image(here / "cross_heatmaps.pdf")
