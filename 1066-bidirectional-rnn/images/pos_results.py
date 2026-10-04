"""Part-of-speech tagging on CoNLL-2000 (from the Notebook): test accuracy per epoch for the three models (mean of 3
seeds, band = min to max), and test accuracy on ambiguous words whose tag depends on the words that follow.
Run: python pos_results.py  -> pos_results.png (Plotly)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, ORANGE, FONT

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "pos_history.csv")
w = pd.read_csv(HERE.parent / "data" / "pos_by_word.csv")
NAMES = {"unidirectional LSTM, 64 nodes": ("LSTM, 64 nodes", BLUE),
         "unidirectional LSTM, 100 nodes (same parameters)": ("LSTM, 100 nodes (= BiLSTM parameters)", ORANGE),
         "bidirectional LSTM, 64 + 64 nodes": ("BiLSTM, 64 + 64 nodes", GREEN)}
WORDS = ["all_words", "ambiguous_words", "that", "about", "as"]
LABELS = ["all", "ambiguous", '"that"', '"about"', '"as"']

fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.1,
                    subplot_titles=["test accuracy per epoch", "test accuracy after 8 epochs, by word"])
for model, (name, colour) in NAMES.items():
    g = h[h.model == model].groupby("epoch").val_accuracy.agg(["mean", "min", "max"]).reset_index()
    fig.add_trace(go.Scatter(x=list(g.epoch) + list(g.epoch[::-1]), y=list(g["max"]) + list(g["min"][::-1]),
                             mode="lines", fill="toself", fillcolor=colour, opacity=0.25, line=dict(width=0), showlegend=False,
                             hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=g.epoch, y=g["mean"], mode="lines+markers", name=name, line=dict(color=colour, width=3),
                             legendgroup=name), row=1, col=1)
    r = w[w.model == model].iloc[0]
    fig.add_trace(go.Bar(x=LABELS, y=[r[c] for c in WORDS], marker_color=colour, name=name, showlegend=False,
                         legendgroup=name), row=1, col=2)
fig.update_xaxes(title_text="epoch", dtick=1, row=1, col=1)
fig.update_yaxes(title_text="accuracy", range=[0.70, 0.96], row=1, col=1)
fig.update_yaxes(range=[0.6, 1.0], row=1, col=2)
fig.update_xaxes(tickangle=0, row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=21), barmode="group",
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
                  margin=dict(l=70, r=30, t=60, b=110))
fig.update_annotations(font=dict(family=FONT["family"], size=22))

if __name__ == "__main__":
    fig.write_image(HERE / "pos_results.png", scale=1.5)
