"""Test accuracy of LSTM and GRU on IMDB reviews (last 200 words). Thin lines: 5 seeds; thick: mean (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "val_accuracy.csv")
s = pd.read_csv(here.parent / "data" / "summary.csv", index_col="model")
fig = go.Figure()
for kind, c in (("LSTM", BLUE), ("GRU", ORANGE)):
    d = a[a.model == kind]
    for _, run in d.groupby("seed"):
        fig.add_trace(go.Scatter(x=run.epoch, y=run.val_accuracy, showlegend=False, opacity=0.35,
                                 line=dict(color=c, width=1.5)))
    m = d.groupby("epoch").val_accuracy.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, line=dict(color=c, width=5),
                             name=f"{kind}, {s.loc[kind, 'parameters']:,} parameters (mean of 5)"))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT,
                  xaxis=dict(title="epoch", dtick=1), yaxis=dict(title="test accuracy", range=[0.78, 0.88]),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "gru_vs_lstm.png", scale=2)
fig.write_image(here / "gru_vs_lstm.pdf")
