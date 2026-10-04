"""Plural direction probe: each word's vector . (unit) plural direction, for 12 held-out singular/plural pairs
(left) and for the number words one ... ten (right), in GloVe and GPT-2 small.
Data: data/plural_probe.csv (from the Notebook). Run: python plural_probe.py"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "plural_probe.csv")
fig = make_subplots(rows=1, cols=3, column_widths=[0.3, 0.3, 0.4], horizontal_spacing=0.07,
                    subplot_titles=["GloVe: held-out nouns", "GPT-2: held-out nouns", "number words"])
for col, model in ((1, "GloVe"), (2, "GPT-2")):
    s = d[(d.model == model) & (d.kind == "singular")].reset_index(drop=True)
    p = d[(d.model == model) & (d.kind == "plural")].reset_index(drop=True)
    for i in range(len(s)):
        fig.add_trace(go.Scatter(x=[s.score[i], p.score[i]], y=[s.word[i]] * 2, mode="lines",
                                 line=dict(color=GREY, width=2), showlegend=False), row=1, col=col)
    fig.add_trace(go.Scatter(x=s.score, y=s.word, mode="markers", marker=dict(color=RED, size=11),
                             name="singular", showlegend=(col == 1)), row=1, col=col)
    fig.add_trace(go.Scatter(x=p.score, y=s.word, mode="markers", marker=dict(color=GREEN, size=11),
                             name="plural (same noun + s)", showlegend=(col == 1)), row=1, col=col)
    fig.update_xaxes(title_text="score = vector · plural direction", row=1, col=col)
for model, c in (("GloVe", BLUE), ("GPT-2", ORANGE)):
    n = d[(d.model == model) & (d.kind == "number")]
    fig.add_trace(go.Scatter(x=n.word, y=n.score, mode="lines+markers", name=model, line=dict(color=c, width=3),
                             marker=dict(size=9)), row=1, col=3)
fig.update_yaxes(title_text="score", row=1, col=3)
fig.update_layout(template="simple_white", width=1400, height=560, font=FONT, margin=dict(l=90, r=20, t=50, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18))
fig.write_image(HERE / "plural_probe.png", scale=2)
fig.write_image(HERE / "plural_probe.pdf")
