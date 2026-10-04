"""Why patience matters: Keras' EarlyStopping rule (improvement = val_loss below the best so far by more than
min_delta = 0.00001; stop after `patience` epochs without one) replayed on the Note's 3,500-epoch history
(data/history_3500.csv). With patience 20 the early bump stops training at epoch 21; with patience 50 training
continues to epoch 503. Plotly."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREY, ORANGE, RED

HERE = Path(__file__).parent
H = pd.read_csv(HERE.parent / "data" / "history_3500.csv")
v = H.val_loss.values


def stop_epoch(patience, min_delta=1e-5):
    best, wait = float("inf"), 0
    for e, x in enumerate(v, start=1):
        if x < best - min_delta:
            best, wait = x, 0
        else:
            wait += 1
            if wait >= patience:
                return e
    return len(v)


S20, S50 = stop_epoch(20), stop_epoch(50)
assert (S20, S50) == (21, 503), (S20, S50)
assert round(v[0], 4) == 0.6892 and round(v[9], 4) == 0.6947 and round(H.val_accuracy[S20 - 1], 2) == 0.5
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, column_widths=[0.45, 0.55],
                    subplot_titles=("Epochs 1 to 60: a short bump", "Epochs 1 to 600"))
for col, n in ((1, 60), (2, 600)):
    fig.add_scatter(x=H.epoch[:n], y=v[:n], mode="lines", line=dict(color=ORANGE, width=3), showlegend=False,
                    row=1, col=col)
fig.add_vline(x=S20, line=dict(color=RED, width=3, dash="dash"), opacity=1, row=1, col=1)
fig.add_annotation(x=S20, y=0.6965, text=f"patience 20<br>stops at epoch {S20}<br>(accuracy 50%)", showarrow=False,
                   xanchor="left", xshift=6, font=dict(size=17, color=RED), row=1, col=1)
fig.add_vline(x=S50, line=dict(color=BLUE, width=3, dash="dash"), opacity=1, row=1, col=2)
fig.add_annotation(x=S50, y=0.66, text=f"patience 50<br>stops at {S50}", showarrow=False, xanchor="right", xshift=-6,
                   font=dict(size=17, color=BLUE), row=1, col=2)
b = int(H.val_loss.idxmin())
fig.add_scatter(x=[H.epoch[b]], y=[v[b]], mode="markers", marker=dict(size=13, color="black"), showlegend=False,
                row=1, col=2)
fig.add_annotation(x=H.epoch[b], y=v[b], text=f"best: epoch {H.epoch[b]}", showarrow=True, ay=40, ax=-50,
                   font=dict(size=16), row=1, col=2)
fig.update_yaxes(title_text="validation loss", range=[0.685, 0.70], row=1, col=1)
fig.update_yaxes(range=[0.4, 0.72], row=1, col=2)
fig.update_xaxes(title_text="epoch")
fig.update_layout(template="simple_white", width=1250, height=560, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=90, r=30, t=70, b=70))
for a in fig.layout.annotations[:2]:
    a.font.size = 21
fig.write_image(HERE / "patience.png", scale=2)
