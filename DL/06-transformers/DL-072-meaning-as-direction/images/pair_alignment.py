"""Cosine between each pair's difference (female word - male word) and woman - man, in GloVe and in GPT-2 small's
embedding table, against random word pairs (grey band: 99 percent of random pairs fall inside it).
Data: data/pair_alignment.csv, data/random_pairs.csv (from the Notebook). Run: python pair_alignment.py"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
al = pd.read_csv(HERE.parent / "data" / "pair_alignment.csv")
rnd = pd.read_csv(HERE.parent / "data" / "random_pairs.csv")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=["GloVe (100 numbers per word)", "GPT-2 small embedding table (768)"])
for col, (model, c) in enumerate((("GloVe", BLUE), ("GPT-2", ORANGE)), 1):
    a = al[al.model == model].iloc[::-1]
    band = np.percentile(abs(rnd[rnd.model == model].cosine), 99)
    fig.add_vrect(x0=-band, x1=band, fillcolor=GREY, opacity=0.18, line_width=0, row=1, col=col)
    fig.add_trace(go.Bar(x=a.cosine, y=a.pair, orientation="h", marker_color=c, text=a.cosine.round(2),
                         textposition="outside", showlegend=False), row=1, col=col)
    fig.add_annotation(x=0, y=-0.9, text=f"random pairs<br>(99% inside ±{band:.2f})", showarrow=False,
                       font=dict(size=14, color=GREY), row=1, col=col)
fig.update_xaxes(range=[-0.35, 0.85], title_text="cosine with woman − man")
fig.update_yaxes(range=[-1.6, 11.6])
fig.update_layout(template="simple_white", width=1200, height=620, font=FONT, margin=dict(l=180, r=20, t=50, b=60))
fig.write_image(HERE / "pair_alignment.png", scale=2)
fig.write_image(HERE / "pair_alignment.pdf")
