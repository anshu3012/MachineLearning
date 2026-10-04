"""Section 8: the full algorithm on the four students. Backpropagation with SGD (one update per student), weights 0.1,
biases 0, learning rate 0.001, for 1,000 epochs. Left: each student's prediction against the real package after each
epoch. Right: the average loss of each epoch. Plotly frames -> epochs.gif + _frames.png"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT, save_gif

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "students.csv")
X, Y = df[["cgpa", "profile_score"]].to_numpy(float), df["lpa"].to_numpy(float)
W1, b1, W2, b2, lr = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0, 0.001
predict = lambda: np.array([W2 @ (W1.T @ x + b1) + b2 for x in X])
preds, losses, first = [predict()], [], None
for ep in range(1, 1001):
    L = []
    for x, y in zip(X, Y):
        O1 = W1.T @ x + b1
        yh = W2 @ O1 + b2
        L.append((y - yh) ** 2)
        g = -2 * (y - yh)
        gO1 = g * W2
        W1, b1, W2, b2 = W1 - lr * np.outer(x, gO1), b1 - lr * gO1, W2 - lr * g * O1, b2 - lr * g
    first = first or L
    preds.append(predict())
    losses.append(np.mean(L))
assert np.allclose(np.round(first, 2), [13.54, 21.29, 30.43, 40.12]) and round(losses[0], 2) == 26.35   # Section 8
assert np.isclose(preds[0][0], 0.32)
assert np.allclose(np.round(preds[1000], 2), [4.18, 4.95, 5.72, 7.12]) and round(losses[-1], 2) == 0.04   # Section 8 text
SHOW = [0, 1, 2, 3, 4, 5, 7, 10, 20, 50, 100, 200, 500, 1000]
print("epoch-1000 predictions", np.round(preds[1000], 2), "loss", round(losses[-1], 3))


def frame(ep):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("prediction vs real package", "average loss per epoch"),
                        horizontal_spacing=0.13)
    names = [f"student {i}" for i in range(1, 5)]
    fig.add_trace(go.Bar(x=names, y=Y, name="real package", marker_color=GREY, opacity=0.45), 1, 1)
    fig.add_trace(go.Bar(x=names, y=preds[ep], name="prediction ŷ", marker_color=BLUE,
                         text=[f"{v:.2f}" for v in preds[ep]], textposition="outside"), 1, 1)
    done = list(range(1, ep + 1))
    if done:
        fig.add_trace(go.Scatter(x=done, y=[losses[e - 1] for e in done], mode="lines+markers", line=dict(color=RED, width=4), marker=dict(size=7),
                                 showlegend=False), 1, 2)
    fig.update_yaxes(title_text="LPA", range=[0, 8.5], row=1, col=1)
    fig.update_xaxes(title_text="epoch", type="log", range=[0, 3.05], dtick=1, row=1, col=2)
    fig.update_yaxes(title_text="loss", type="log", range=[-1.6, 1.6], dtick=1, row=1, col=2)
    lab = f"average loss {losses[ep - 1]:.2f}" if ep else "before training"
    fig.update_layout(template="simple_white", width=1150, height=520, font=dict(FONT, size=20), barmode="group",
                      title=dict(text=f"epoch {ep}: {lab}", x=0.5), legend=dict(x=0.0, y=1.0, bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=70, r=30, t=100, b=60))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    save_gif([frame(e) for e in SHOW], "epochs", [1, len(SHOW) - 1], here, fps=2, cols=1)
