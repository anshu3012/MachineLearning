"""Validation accuracy of LSTM and GRU on IMDB, with no gap and with 25 padding steps after the review.
Thin lines: 3 seeds; thick: their mean (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "val_accuracy.csv")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=("review only (gap 0)", "review + 25 padding steps (gap 25)"))
for col, gap in enumerate((0, 25), start=1):
    for kind, c in (("LSTM", BLUE), ("GRU", ORANGE)):
        d = a[(a.gap == gap) & (a.model == kind)]
        for _, s in d.groupby("seed"):
            fig.add_trace(go.Scatter(x=s.epoch, y=s.val_accuracy, showlegend=False, opacity=0.35,
                                     line=dict(color=c, width=1.5)), row=1, col=col)
        m = d.groupby("epoch").val_accuracy.mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, name=f"{kind} (mean of 3)", showlegend=(col == 1),
                                 line=dict(color=c, width=5)), row=1, col=col)
fig.update_layout(template="simple_white", width=1000, height=450, font=FONT,
                  legend=dict(x=0.02, y=0.05, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=FONT)
fig.update_xaxes(title="epoch", dtick=1)
fig.update_yaxes(title="validation accuracy", row=1, col=1)
fig.write_image(here / "gru_vs_lstm.png", scale=2)
fig.write_image(here / "gru_vs_lstm.pdf")
