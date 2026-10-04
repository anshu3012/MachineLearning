"""Section 6.2: test BLEU of the three trained attention models, all 1,000 test sentences and the long ones
(11-16 words). Bars: mean of 3 runs; dots: the single runs. From data/comparison.csv (the Notebook).
Run: python bleu_compare.py  -> bleu_compare.png (Plotly grouped bars with run dots)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, GREEN, ORANGE

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "comparison.csv")
m = d.groupby("model", sort=False)[["bleu_all", "bleu_11plus"]].mean()
import numpy as np
assert np.allclose(m.bleu_all, [25.1, 31.6, 17.7], atol=0.06) and np.allclose(m.bleu_11plus, [20.0, 26.8, 12.0], atol=0.06)  # the Note's table
COL = {"Bahdanau (concat)": ORANGE, "Luong dot": BLUE, "Luong general": GREEN}
groups = {"bleu_all": "all 1,000 test sentences", "bleu_11plus": "sentences of 11–16 words"}

fig = go.Figure()
for model, c in COL.items():
    fig.add_trace(go.Bar(x=list(groups.values()), y=[m.loc[model, k] for k in groups], name=model, marker_color=c,
                         text=[f"{round(m.loc[model, k], 2) + 1e-6:.1f}" for k in groups], textposition="inside", insidetextanchor="start",
                         textfont=dict(color="white", size=24), offsetgroup=model))
fig.update_layout(template="simple_white", barmode="group", width=1000, height=520,
                  font=dict(family="Latin Modern Roman", size=22), yaxis=dict(title="test BLEU", range=[0, 37]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                  margin=dict(l=80, r=20, t=70, b=50))
for model, c in COL.items():                     # single runs as dots over each bar
    r = d[d.model == model]
    for k, g in groups.items():
        fig.add_trace(go.Scatter(x=[g] * len(r), y=r[k], mode="markers", offsetgroup=model, showlegend=False,
                                 marker=dict(color="black", size=8)))
fig.update_layout(scattermode="group")

if __name__ == "__main__":
    fig.write_image(HERE / "bleu_compare.png", scale=2)
