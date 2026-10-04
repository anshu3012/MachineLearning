"""Attention weights of the Bahdanau, Luong dot and Luong general models on the same real test sentence (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "attention_three.csv", keep_default_na=False)
kinds = ["Bahdanau (concat)", "Luong dot", "Luong general"]
fig = make_subplots(rows=1, cols=3, subplot_titles=kinds, horizontal_spacing=0.09)
for k, kind in enumerate(kinds, start=1):
    s = a[a.model == kind]
    z = s.pivot(index="i", columns="j", values="alpha")
    y = s.drop_duplicates("i").sort_values("i").french.str.replace("<", "&lt;")
    x = s.drop_duplicates("j").sort_values("j").english
    fig.add_trace(go.Heatmap(z=z.values, x=list(x), y=[f"{w} " + "​" * i for i, w in enumerate(y)],
                             colorscale="Oranges", zmin=0, zmax=1, showscale=(k == 3)), row=1, col=k)
    fig.update_yaxes(autorange="reversed", row=1, col=k)
    fig.update_xaxes(side="top", tickangle=-50, row=1, col=k)
fig.update_layout(template="simple_white", width=1400, height=560, font=FONT, margin=dict(l=90, r=20, t=150, b=20))
fig.update_annotations(yshift=95)
fig.write_image(here / "attention_three.png", scale=2)
fig.write_image(here / "attention_three.pdf")
