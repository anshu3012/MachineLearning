"""Validation accuracy with and without batch normalisation, 5 seeds each, mean in bold (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, GREY, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "val_accuracy.csv")
fig = go.Figure()
for key, name, c in (("without", "without batch normalisation", GREY), ("with", "with batch normalisation", GREEN)):
    cols = [k for k in a.columns if k.startswith(key + "_")]
    for k in cols:
        fig.add_trace(go.Scatter(x=a.epoch + 1, y=a[k], showlegend=False, opacity=0.35, line=dict(color=c, width=1.5)))
    fig.add_trace(go.Scatter(x=a.epoch + 1, y=a[cols].mean(axis=1), name=name + " (mean of 5)", line=dict(color=c, width=5)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, xaxis=dict(title="epoch"),
                  yaxis=dict(title="validation accuracy", range=[0.4, 1.02]), legend=dict(x=0.45, y=0.45, bgcolor="rgba(255,255,255,0.8)"),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "val_accuracy.png", scale=2)
fig.write_image(here / "val_accuracy.pdf")
