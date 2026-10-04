"""Attention weights of the 12 heads in BERT-base's first layer on one sentence, one small heatmap per head (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "bert_layer1_attention.csv")
toks = a[a["head"] == 1].drop_duplicates("key_pos").sort_values("key_pos").key.tolist()
fig = make_subplots(rows=3, cols=4, subplot_titles=[f"head {i}" for i in range(1, 13)],
                    horizontal_spacing=0.035, vertical_spacing=0.09)
for i in range(12):
    m = a[a["head"] == i + 1].pivot(index="query_pos", columns="key_pos", values="weight").values
    fig.add_trace(go.Heatmap(z=m, x=list(range(10)), y=list(range(10)), zmin=0, zmax=0.8, colorscale="Blues",
                             showscale=(i == 0), colorbar=dict(title="weight", len=0.9)), row=i // 4 + 1, col=i % 4 + 1)
ticks = dict(tickmode="array", tickvals=list(range(10)), ticktext=toks, tickfont=dict(size=11))
fig.update_xaxes(**ticks, tickangle=-60)
fig.update_yaxes(**ticks, autorange="reversed")
for r in range(1, 4):
    for c in range(2, 5):
        fig.update_yaxes(showticklabels=False, row=r, col=c)
for r in (1, 2):
    for c in range(1, 5):
        fig.update_xaxes(showticklabels=False, row=r, col=c)
fig.update_layout(template="simple_white", width=1100, height=1000, font=FONT, margin=dict(l=90, r=20, t=40, b=100))
fig.write_image(here / "bert_heads.png", scale=2)
fig.write_image(here / "bert_heads.pdf")
