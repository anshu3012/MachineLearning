"""Next-character prediction on IMDB review text (from the Notebook): validation loss per epoch for one LSTM layer,
two stacked LSTM layers, and one wider LSTM layer with about as many parameters as the stack (mean of 2 seeds,
band = lower to higher seed). Run: python char_lm.py  -> char_lm.png (Plotly)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, ORANGE, FONT

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "char_lm_history.csv")
COLOURS = {"1 layer, 128 nodes": BLUE, "1 wide layer, 215 nodes": ORANGE, "2 stacked layers, 128 + 128 nodes": GREEN}

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["training loss", "validation loss (unseen reviews)"])
for col, metric in ((1, "loss"), (2, "val_loss")):
    for model, colour in COLOURS.items():
        g = h[h.model == model].groupby("epoch")[metric].agg(["mean", "min", "max"]).reset_index()
        fig.add_trace(go.Scatter(x=list(g.epoch) + list(g.epoch[::-1]), y=list(g["max"]) + list(g["min"][::-1]),
                                 mode="lines", fill="toself", fillcolor=colour, opacity=0.25, line=dict(width=0),
                                 showlegend=False, hoverinfo="skip"), row=1, col=col)
        fig.add_trace(go.Scatter(x=g.epoch, y=g["mean"], mode="lines+markers", name=model, showlegend=col == 1,
                                 line=dict(color=colour, width=3)), row=1, col=col)
    fig.update_xaxes(title_text="epoch", dtick=5, range=[0, 41], row=1, col=col)
fig.update_yaxes(title_text="cross-entropy loss per character", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=21),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22), margin=dict(l=80, r=30, t=60, b=110))
fig.update_annotations(font=dict(family=FONT["family"], size=22))

if __name__ == "__main__":
    fig.write_image(HERE / "char_lm.png", scale=1.5)
