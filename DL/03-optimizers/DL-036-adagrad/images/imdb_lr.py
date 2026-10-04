"""IMDB, 5,000 words: AdaGrad's effective learning rate for each word against how often the word occurs (left),
and the mean size of the learned weights by frequency band, SGD vs AdaGrad (right) (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, FONT

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "imdb_words.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.55, 0.45],
                    subplot_titles=("AdaGrad's learning rate per word", "mean |weight| of the words"))
fig.add_trace(go.Scatter(x=w.freq, y=w.eff_lr, mode="markers", showlegend=False,
                         marker=dict(color=GREEN, size=4, opacity=0.4)), 1, 1)
bands = [(0, 0.003, "< 0.3%"), (0.003, 0.01, "0.3–1%"), (0.01, 0.1, "1–10%"), (0.1, 1.01, "> 10%")]
labels = [b[2] for b in bands]
for col, name, c in (("w_sgd", "SGD", BLUE), ("w_adagrad", "AdaGrad", GREEN)):
    vals = [w[(w.freq >= lo) & (w.freq < hi)][col].mean() for lo, hi, _ in bands]
    fig.add_trace(go.Bar(x=labels, y=vals, name=name, marker_color=c, text=[f"{v:.3f}" for v in vals],
                         textposition="outside", textfont=dict(size=13)), 1, 2)
fig.update_xaxes(type="log", title_text="share of reviews containing the word", row=1, col=1)
fig.update_yaxes(type="log", title_text="η / √v after 10 epochs", row=1, col=1)
fig.update_xaxes(title_text="share of reviews containing the word", row=1, col=2)
fig.update_yaxes(range=[0, 0.34], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, barmode="group",
                  legend=dict(orientation="h", x=0.62, y=1.16), margin=dict(l=80, r=20, t=80, b=70))
fig.write_image(here / "imdb_lr.png", scale=2)
fig.write_image(here / "imdb_lr.pdf")
