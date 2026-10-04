"""Section 5.2: the 4 x 3 cross-attention weights computed by hand in the Notebook (random stand-in vectors, untrained
W_Q, W_K, W_V), from data/by_hand_weights.csv. Left: the weight matrix, rows = French positions (queries),
columns = English words (keys). Right: the row of "nous" built from its three scaled scores.
Run: python by_hand.py  -> by_hand.png (Plotly heat map + bars)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREY, ORANGE

HERE = Path(__file__).parent
W = pd.read_csv(HERE.parent / "data" / "by_hand_weights.csv", index_col=0)
s = np.array([0.016, 0.505, -0.145])                        # scaled scores of "nous" (the Note, from the Notebook)
w = np.exp(s) / np.exp(s).sum()
assert np.allclose(w.round(3), W.loc["nous"].values) and np.allclose(W.sum(axis=1), 1, atol=0.002)
assert np.allclose(np.exp(s).round(3), [1.016, 1.657, 0.865])

fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.16,
                    subplot_titles=["weights: 4 French rows × 3 English columns", 'row "nous": scores → weights'])
fig.add_trace(go.Heatmap(z=W.values, x=list(W.columns), y=list(W.index), colorscale="Blues", zmin=0, zmax=0.7,
                         text=W.values.round(3), texttemplate="%{text}", textfont=dict(size=22), showscale=False,
                         xgap=3, ygap=3), 1, 1)
fig.add_shape(type="rect", x0=-0.5, x1=2.5, y0=0.5, y1=1.5, line=dict(color=ORANGE, width=5), fillcolor="rgba(0,0,0,0)",
              layer="above", row=1, col=1)
fig.update_yaxes(autorange="reversed", row=1, col=1)
fig.update_xaxes(side="bottom", row=1, col=1)
for vals, name, c in ((s, "scaled score q·k / √8", GREY), (w, "weight (softmax)", ORANGE)):
    fig.add_trace(go.Bar(x=list(W.columns), y=vals, name=name, marker_color=c, text=[f"{v:.3f}" for v in vals],
                         textposition="outside"), 1, 2)
fig.update_yaxes(range=[-0.3, 0.7], zeroline=True, zerolinecolor=GREY, row=1, col=2)
fig.update_layout(template="simple_white", barmode="group", width=1200, height=520,
                  font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(orientation="h", x=0.79, xanchor="center", y=-0.12, yanchor="top"),
                  margin=dict(l=90, r=20, t=70, b=110))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "by_hand.png", scale=2)
