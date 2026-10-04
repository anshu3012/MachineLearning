"""The symmetry problem on the Note's classification network (2-2-1, sigmoid, binary cross-entropy, learning rate 0.1,
2,000 epochs) (Plotly frames). Left: every weight starts at 0.1; the two hidden nodes get identical updates and never
separate. Right: one weight starts at 0.11 instead; the two nodes drift apart and the loss falls much further.
Run: python symmetry.py -> symmetry.gif, symmetry_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, save_gif

HERE = Path(__file__).parent
s = lambda z: 1 / (1 + np.exp(-z))
Yc = np.array([1, 1, 0, 0], float)
Xc = np.array([[8, 8], [7, 9], [6, 10], [5, 5]], float)
EPOCHS = 2000


def run(first_weight):
    W1, b1, W2, b2 = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0
    W1[0, 0] = first_weight
    hist, losses = [], []
    for _ in range(EPOCHS):
        l = []
        for x, y in zip(Xc, Yc):
            a1 = s(W1.T @ x + b1)
            yh = s(W2 @ a1 + b2)
            l.append(-y * np.log(yh) - (1 - y) * np.log(1 - yh))
            d = -(y - yh)
            dh = d * W2 * a1 * (1 - a1)
            W1, b1, W2, b2 = W1 - 0.1 * np.outer(x, dh), b1 - 0.1 * dh, W2 - 0.1 * d * a1, b2 - 0.1 * d
        hist.append(W1[0].copy())                       # the CGPA weight of hidden node 1 and of hidden node 2
        losses.append(np.mean(l))
    preds = [float(s(W2 @ s(W1.T @ x + b1) + b2)) for x in Xc]
    return np.array(hist), np.array(losses), preds


RUNS = [run(0.1), run(0.11)]
assert (RUNS[0][0][:, 0] == RUNS[0][0][:, 1]).all() and round(RUNS[0][1][-1], 2) == 0.49      # twins: never separate
assert abs(RUNS[1][0][-1, 0] - RUNS[1][0][-1, 1]) > 4 and RUNS[1][1][-1] < 0.05               # one weight 0.11: they separate
assert RUNS[0][2][3] > 0.5 and RUNS[1][2][3] < 0.05                                          # student 4: wrong, then right
ep = np.arange(1, EPOCHS + 1)


def frame(k):
    fig = make_subplots(2, 2, vertical_spacing=0.16, horizontal_spacing=0.1,
                        subplot_titles=["all weights start at 0.1", "one weight starts at 0.11", "", ""])
    for c, (h, l, _) in enumerate(RUNS, start=1):
        fig.add_trace(go.Scatter(x=ep[:k], y=h[:k, 0], mode="lines", line=dict(color=BLUE, width=7), name="CGPA weight of hidden node 1", showlegend=(c == 1)), 1, c)
        fig.add_trace(go.Scatter(x=ep[:k], y=h[:k, 1], mode="lines", line=dict(color=ORANGE, width=3, dash="dash"), name="CGPA weight of hidden node 2", showlegend=(c == 1)), 1, c)
        fig.add_trace(go.Scatter(x=ep[:k], y=l[:k], mode="lines", line=dict(color=RED, width=4), showlegend=False), 2, c)
        fig.add_annotation(x=EPOCHS, y=l[k - 1], text=f"loss {l[k - 1]:.2f}", xanchor="right", yshift=22, showarrow=False, row=2, col=c,
                           font=dict(color=RED, size=22))
        fig.update_xaxes(range=[0, EPOCHS], row=1, col=c)
        fig.update_xaxes(range=[0, EPOCHS], title="epoch", row=2, col=c)
        fig.update_yaxes(range=[-5.5, 1], row=1, col=c)
        fig.update_yaxes(range=[0, 0.8], row=2, col=c)
    fig.update_yaxes(title="weight", row=1, col=1)
    fig.update_yaxes(title="average loss", row=2, col=1)
    fig.update_annotations(selector=dict(text="all weights start at 0.1"), font=dict(size=24))
    fig.update_annotations(selector=dict(text="one weight starts at 0.11"), font=dict(size=24))
    fig.update_layout(template="simple_white", width=1100, height=700, font=dict(family="Latin Modern Roman", size=20),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.14), margin=dict(l=70, r=20, t=110, b=60))
    return fig


if __name__ == "__main__":
    ks = list(range(80, EPOCHS + 1, 80))
    save_gif([frame(k) for k in ks], "symmetry", [len(ks) // 4, len(ks) - 1], HERE, fps=5, hold=10, cols=1)
    for h, l, p in RUNS:
        print("final weights", h[-1].round(2), "loss", l[-1].round(3), "predictions", np.round(p, 2))
