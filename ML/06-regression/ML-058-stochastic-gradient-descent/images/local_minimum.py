"""SGD's noise can carry it out of a shallow local minimum (Plotly frames -> GIF). A made-up loss with one parameter w:
the average loss has a narrow, shallow dip at w = -1.49 and a wide, deep minimum at w = 1.92. Observation i has the
loss f(w) + a_i w, the average curve tilted a little (a_i: 100 random numbers, standard deviation 2, mean exactly 0),
so the average of the 100 losses is f. Both methods start at w = -3 with learning rate 0.05. Batch gradient descent
takes one step per epoch on the average loss; SGD takes 100 steps, one random observation each.
The script also counts the result over 200 seeds: after 300 epochs SGD is in the deep minimum in all 200, and with half the noise (standard deviation 1) in only 6."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
LR, SIG, N, START, EPOCHS = 0.05, 2.0, 100, -3.0, 300
f = lambda w: 0.02 * w ** 2 - np.exp(-(w - 2) ** 2 / 2) - 0.3 * np.exp(-(w + 1.5) ** 2 / 0.08)
df = lambda w: 0.04 * w + (w - 2) * np.exp(-(w - 2) ** 2 / 2) + 7.5 * (w + 1.5) * np.exp(-(w + 1.5) ** 2 / 0.08)


def sgd(seed, epochs, sig=SIG):
    """Positions after every update; row e holds the 100 positions of epoch e."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0, sig, N)
    a -= a.mean()
    w, out = START, []
    for _ in range(epochs):
        row = []
        for i in rng.integers(0, N, N):
            w -= LR * (df(w) + a[i])
            row.append(w)
        out.append(row)
    return np.array(out)


batch = [START]
for _ in range(EPOCHS):
    batch.append(batch[-1] - LR * df(batch[-1]))
deep = sum(sgd(s, EPOCHS)[-1, -1] > 0 for s in range(200))
deep_half = sum(sgd(s, EPOCHS, sig=1.0)[-1, -1] > 0 for s in range(200))
assert (deep, deep_half) == (200, 6), (deep, deep_half)
assert abs(batch[-1] + 1.49) < 0.01
path = sgd(0, EPOCHS)
assert path[-1, -1] > 0
ws = np.linspace(-3.6, 4.2, 600)


def frame(e):
    s_now = START if e == 0 else path[e - 1, -1]
    fig = go.Figure(go.Scatter(x=ws, y=f(ws), mode="lines", line=dict(color=GREY, width=4), showlegend=False))
    if e:
        fig.add_scatter(x=path[e - 1], y=f(path[e - 1]), mode="markers", marker=dict(size=7, color=ORANGE, opacity=0.35),
                        showlegend=False)
    fig.add_scatter(x=[batch[e]], y=[f(batch[e])], mode="markers", marker=dict(size=24, color=RED, line=dict(width=2, color="black")),
                    name="batch: 1 step per epoch")
    fig.add_scatter(x=[s_now], y=[f(s_now)], mode="markers", marker=dict(size=20, color=ORANGE, symbol="diamond", line=dict(width=2, color="black")),
                    name="SGD: 100 noisy steps per epoch")
    fig.add_annotation(x=-1.49, y=-0.26, ay=45, ax=0, text="shallow local minimum", showarrow=True, arrowhead=2, font=dict(size=20))
    fig.add_annotation(x=1.92, y=-0.92, ay=35, ax=0, text="deep minimum", showarrow=True, arrowhead=2, font=dict(size=20))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                      title=dict(text=f"epoch {e}:  batch at w = {batch[e]:.2f},  SGD at w = {s_now:.2f}".replace("-", "−"), x=0.5),
                      xaxis=dict(title="coefficient w", range=[-3.6, 4.2]), yaxis=dict(title="average loss", range=[-1.25, 0.45]),
                      legend=dict(x=0.99, y=0.99, xanchor="right"), margin=dict(l=80, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    hop = int(np.argmax(path[:, -1] > 0)) + 1          # first epoch that ends in the deep basin
    print("SGD hops out in epoch", hop)
    es = list(range(0, 13)) + list(range(20, EPOCHS + 1, 20))     # every epoch at first, then every 20th
    make_gif([frame(e) for e in es], here / "local_minimum", fps=3, holds=[4] + [1] * (len(es) - 2) + [10],
             keys=[0, es.index(hop) if hop in es else 1, es.index(100), len(es) - 1])
