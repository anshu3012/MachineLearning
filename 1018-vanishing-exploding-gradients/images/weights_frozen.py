"""The 20 first-layer weights over 100 epochs (Plotly frames), from data/first_layer_weights.csv (written by the
Notebook). Left: 10 sigmoid layers, every weight stays on its starting value. Right: 10 ReLU layers, the weights move.
Run: python weights_frozen.py -> weights_frozen.gif, weights_frozen_frames.png"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, GREEN, save_gif

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "first_layer_weights.csv")
NETS = [("10 sigmoid layers", RED), ("10 ReLU layers", GREEN)]
W = {n: d[d.network == n].sort_values("epoch").filter(regex=r"^w\d+$").to_numpy() for n, _ in NETS}
move = {n: np.abs(W[n][-1] - W[n][0]).mean() for n in W}
assert W["10 sigmoid layers"].shape == (101, 20)
assert move["10 sigmoid layers"] < 1e-6 and round(move["10 ReLU layers"], 2) == 0.62      # the Note's numbers
LIM = max(np.abs(w).max() for w in W.values()) * 1.08


def frame(k):
    fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=[
        f"{n}: mean change {np.abs(W[n][k] - W[n][0]).mean():.1e}" if n.startswith("10 s") else
        f"{n}: mean change {np.abs(W[n][k] - W[n][0]).mean():.2f}" for n, _ in NETS])
    for c, (n, col) in enumerate(NETS, start=1):
        for j in range(20):
            fig.add_trace(go.Scatter(x=np.arange(k + 1), y=W[n][:k + 1, j], mode="lines", line=dict(color=col, width=2)), 1, c)
        fig.update_xaxes(range=[0, 100], title="epoch", row=1, col=c)
        fig.update_yaxes(range=[-LIM, LIM], row=1, col=c)
    fig.update_yaxes(title="value of each first-layer weight", row=1, col=1)
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"the 20 weights of the first layer after <b>{k}</b> epochs", x=0.5, font=dict(size=28)),
                      margin=dict(l=80, r=20, t=110, b=70))
    return fig


if __name__ == "__main__":
    ks = list(range(0, 101, 4))
    save_gif([frame(k) for k in ks], "weights_frozen", [len(ks) // 4, len(ks) - 1], HERE, fps=5, hold=10, cols=1)
    print(move)
