"""What each approach costs as the training data grows: numbers kept after training, and time to answer 10,000 new
students, for KNN (k = 3, instance-based) and logistic regression (model-based). Data: the Note's placement data
generator with 1,000 to 1,000,000 students. Timings are the best of 3 runs on our machine. Plotly."""
import time
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from placement_data import placement_data

HERE = Path(__file__).parent
ORANGE, PURPLE = "#F58518", "#B279A2"
SIZES = [1_000, 10_000, 100_000, 1_000_000]
Q, _ = placement_data(10_000, seed=99)


def best(f):
    t = []
    for _ in range(3):
        s = time.perf_counter(); f(); t.append(time.perf_counter() - s)
    return 1000 * min(t)


rows = []
for n in SIZES:
    X, y = placement_data(n, seed=1)
    mu, sd = X.mean(0), X.std(0)
    Xs, Qs = (X - mu) / sd, (Q - mu) / sd
    knn, lr = KNeighborsClassifier(3).fit(Xs, y), LogisticRegression().fit(Xs, y)
    kept_knn = Xs.size + y.size                      # every training value is kept
    kept_lr = lr.coef_.size + lr.intercept_.size     # w1, w2 and b
    rows.append((n, kept_knn, kept_lr, best(lambda: knn.predict(Qs)), best(lambda: lr.predict(Qs))))
assert [r[1] for r in rows] == [3 * n for n in SIZES] and all(r[2] == 3 for r in rows)
assert rows[-1][3] > 10 * rows[-1][4]                  # KNN answers far more slowly than the model

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("Numbers kept after training", "Time to answer 10,000 new students (ms)"))
for col, ki, li in ((1, 1, 2), (2, 3, 4)):
    fig.add_scatter(x=SIZES, y=[r[ki] for r in rows], mode="lines+markers", line=dict(color=ORANGE, width=4),
                    marker=dict(size=12), name="instance-based (KNN)", showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=SIZES, y=[r[li] for r in rows], mode="lines+markers", line=dict(color=PURPLE, width=4),
                    marker=dict(size=12), name="model-based (logistic regression)", showlegend=col == 1, row=1, col=col)
fig.update_xaxes(type="log", title_text="training students", tickvals=SIZES,
                 ticktext=["1,000", "10,000", "100,000", "1,000,000"])
fig.update_yaxes(type="log", row=1, col=1, tickvals=[3, 1e3, 1e4, 1e5, 1e6, 3e6],
                 ticktext=["3", "1k", "10k", "100k", "1M", "3M"])
fig.update_yaxes(type="log", row=1, col=2, tickvals=[0.1, 1, 10, 30], ticktext=["0.1", "1", "10", "30"], range=[-1.2, 1.7])
fig.update_layout(template="simple_white", width=1300, height=620, font=dict(family="Latin Modern Roman", size=19),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=70, b=140))
for a in fig.layout.annotations:
    a.font.size = 21
fig.write_image(HERE / "cost_compare.png", scale=2)
for r in rows:
    print(r[0], r[1], r[2], round(r[3], 1), round(r[4], 2))
