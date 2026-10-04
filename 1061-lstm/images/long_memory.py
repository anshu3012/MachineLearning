"""Validation accuracy of SimpleRNN vs LSTM on IMDB reviews (first 50 words), with no gap and with 25 padding
steps after the words. Thin lines: 3 seeds; thick lines: their mean (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREEN, GREY, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "val_accuracy.csv")
panels = (0, 25)
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=["no gap: words end at the last step", "gap of 25 padding steps after the words"])
for col, gap in enumerate(panels, start=1):
    for kind, c in (("SimpleRNN", GREY), ("LSTM", GREEN)):
        d = a[(a.gap == gap) & (a.model == kind)]
        for _, s in d.groupby("seed"):
            fig.add_trace(go.Scatter(x=s.epoch, y=s.val_accuracy, showlegend=False, opacity=0.35,
                                     line=dict(color=c, width=1.5)), row=1, col=col)
        m = d.groupby("epoch").val_accuracy.mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, name=f"{kind} (mean of 3)", showlegend=col == 1,
                                 line=dict(color=c, width=5)), row=1, col=col)
    fig.add_hline(y=0.5, line=dict(color=GREY, dash="dot"), row=1, col=col)
    fig.update_xaxes(title_text="epoch", row=1, col=col)
fig.update_yaxes(title_text="validation accuracy", range=[0.45, 0.8], row=1, col=1)
fig.update_layout(template="simple_white", width=1050, height=460, font=FONT,
                  legend=dict(orientation="h", x=0.25, y=-0.2), margin=dict(l=70, r=20, t=50, b=100))
fig.update_annotations(font=dict(family=FONT["family"], size=17))
fig.write_image(here / "long_memory.png", scale=2)
fig.write_image(here / "long_memory.pdf")
