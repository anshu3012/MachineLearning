"""The three variants as paths on one loss surface (Plotly frames). Model: one sigmoid neuron on the Note's data
(Social Network Ads, standardized age and salary, the first 320 rows), with two free weights w1 (age) and w2 (salary);
the bias is held at its best value so the loss can be drawn over (w1, w2). All three start at the same point and use
learning rate 0.3 for 15 epochs: batch makes 15 updates, mini-batch (32) 150, stochastic 4,800.
Run: python paths.py -> paths.gif, paths_frames.png"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, save_gif

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "Social_Network_Ads.csv")
Z = df[["Age", "EstimatedSalary"]].to_numpy(float)
Z = ((Z - Z.mean(0)) / Z.std(0))[:320]
y = df.Purchased.to_numpy(float)[:320]
sig = lambda t: 1 / (1 + np.exp(-t))

# best weights and bias by long batch gradient descent
w, b = np.zeros(2), 0.0
for _ in range(20000):
    p = sig(Z @ w + b)
    w, b = w - 0.5 * Z.T @ (p - y) / len(y), b - 0.5 * (p - y).mean()
W_BEST, B = w, b
loss = lambda w: float(-(y * np.log(sig(Z @ w + B)) + (1 - y) * np.log(1 - sig(Z @ w + B))).mean())
START, LR, EPOCHS = np.array([-1.5, 3.5]), 0.3, 15


def run(batch, seed=0):
    rng, w, path, marks = np.random.default_rng(seed), START.copy(), [START.copy()], [0]
    for _ in range(EPOCHS):
        order = rng.permutation(len(y))
        for i in range(0, len(y), batch):
            idx = order[i:i + batch]
            w = w - LR * Z[idx].T @ (sig(Z[idx] @ w + B) - y[idx]) / len(idx)
            path.append(w.copy())
        marks.append(len(path) - 1)                        # index of the last update of each epoch
    return np.array(path), marks


RUNS = [("batch: 1 update per epoch", 320, BLUE), ("mini-batch of 32: 10 per epoch", 32, ORANGE), ("stochastic: 320 per epoch", 1, RED)]
PATHS = {n: run(bs) for n, bs, _ in RUNS}
dist = {n: np.linalg.norm(PATHS[n][0][-1] - W_BEST) for n in PATHS}
ups = {n: int((np.diff([loss(w) for w in PATHS[n][0]]) > 0).sum()) for n in PATHS}
names = [n for n, _, _ in RUNS]
assert dist[names[0]] > dist[names[1]] > 0 and dist[names[0]] > dist[names[2]]     # batch is furthest from the minimum after 15 epochs
assert ups[names[0]] == 0 and ups[names[2]] > 100                                    # batch never goes uphill, stochastic often does
g1, g2 = np.linspace(-2.2, 4.2, 70), np.linspace(-0.6, 4.2, 60)
LL = np.array([[loss(np.array([a, c])) for a in g1] for c in g2])


def frame(ep):
    fig = make_subplots(1, 3, horizontal_spacing=0.04, shared_yaxes=True, subplot_titles=[n for n in names])
    for c, (n, bs, col) in enumerate(RUNS, start=1):
        path, marks = PATHS[n]
        k = marks[ep]
        fig.add_trace(go.Contour(x=g1, y=g2, z=LL, colorscale="Greys", showscale=False, contours=dict(coloring="lines"), line=dict(width=1.2), ncontours=14), 1, c)
        fig.add_trace(go.Scatter(x=path[:k + 1, 0], y=path[:k + 1, 1], mode="lines", line=dict(color=col, width=2.5)), 1, c)
        fig.add_trace(go.Scatter(x=[path[k, 0]], y=[path[k, 1]], mode="markers", marker=dict(color=col, size=14)), 1, c)
        fig.add_trace(go.Scatter(x=[W_BEST[0]], y=[W_BEST[1]], mode="markers", marker=dict(color="black", size=16, symbol="star")), 1, c)
        fig.add_annotation(x=2.6, y=3.5, text=f"{k} update{'s' if k > 1 else ''}<br>loss {loss(path[k]):.2f}", showarrow=False, row=1, col=c, font=dict(size=22, color=col))
        fig.update_xaxes(title="w₁ (age)", range=[-2.2, 4.2], row=1, col=c)
    fig.update_yaxes(title="w₂ (salary)", range=[-0.6, 4.2], row=1, col=1)
    fig.update_annotations(selector=lambda a: a.text in names, font=dict(size=22))
    fig.update_layout(template="simple_white", width=1300, height=560, showlegend=False, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"after <b>{ep}</b> epochs (star: lowest loss)", x=0.5, font=dict(size=28)), margin=dict(l=70, r=20, t=110, b=70))
    return fig


if __name__ == "__main__":
    from surftilt import tilt_gif                              # the same loss surface, tilting down to the map of paths.gif
    sub = [(PATHS[n][0][::max(1, len(PATHS[n][0]) // 40)], c) for n, _, c in RUNS]
    tilt_gif("loss_surface", HERE, dict(x=g1, y=g2, Z=LL, xlab="w₁ (age)", ylab="w₂ (salary)", zlab="loss", cscale="Greys",
             reverse=True, contours=dict(start=float(LL.min()), end=float(LL.max()), size=float((LL.max() - LL.min()) / 14)), marks=[dict(x=p[:, 0], y=p[:, 1], z=[loss(q) for q in p], color=c, size=3) for p, c in sub]
             + [dict(x=[W_BEST[0]], y=[W_BEST[1]], z=[loss(W_BEST)], color="black", size=9, symbol="diamond", line=False),
                dict(x=[START[0]], y=[START[1]], z=[loss(START)], color="black", size=7, line=False)]), zasp=0.6, floor=0.3)
    save_gif([frame(e) for e in range(EPOCHS + 1)], "paths", [1, 5, EPOCHS], HERE, fps=2, hold=6, cols=1)
    print("best", W_BEST.round(2), B.round(2), "loss", round(loss(W_BEST), 3), "start loss", round(loss(START), 2))
    for n in names:
        print(n, "end", PATHS[n][0][-1].round(2), "loss", round(loss(PATHS[n][0][-1]), 3), "distance", dist[n].round(2), "uphill steps", ups[n])
