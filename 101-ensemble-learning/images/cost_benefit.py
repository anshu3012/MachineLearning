"""Section 6: the cost and the benefit of an ensemble, on the two-moons split of why_it_works.py.
A bagging ensemble of full-depth trees with 1 to 200 trees. Left: training time (fastest of 5 runs) grows with the
number of trees. Right: test accuracy, averaged over 5 seeds, rises above the single tree and then levels off.
Run: python cost_benefit.py  -> cost_benefit.png (Plotly)"""
import time
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
X, y = make_moons(n_samples=400, noise=0.35, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
ns = [1, 2, 5, 10, 20, 50, 100, 200]
secs, acc = [], []
BaggingClassifier(DecisionTreeClassifier(), n_estimators=5).fit(X_tr, y_tr)        # warm-up, so run 1 is not slower
for n in ns:
    t, a = [], []
    for s in range(5):
        start = time.perf_counter()
        m = BaggingClassifier(DecisionTreeClassifier(), n_estimators=n, random_state=s).fit(X_tr, y_tr)
        t.append(time.perf_counter() - start)
        a.append(m.score(X_te, y_te))
    secs.append(min(t))
    acc.append(np.mean(a))
single = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr).score(X_te, y_te)
print("seconds", np.round(secs, 4), "accuracy", np.round(acc, 3), "single tree", single)
assert secs[-1] > 20 * secs[0]                                   # cost grows with the number of models
assert min(acc[4:]) > acc[0] + 0.03 and max(acc[4:]) - min(acc[4:]) < 0.01   # gain, then a plateau

fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=("cost: training time", "benefit: test accuracy"))
fig.add_trace(go.Scatter(x=ns, y=np.array(secs) * 1000, mode="lines+markers", line=dict(color="#E45756", width=4),
                         marker=dict(size=10), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=ns, y=acc, mode="lines+markers", line=dict(color="#4C78A8", width=4),
                         marker=dict(size=10), showlegend=False), 1, 2)
fig.add_hline(y=single, line=dict(color="#6B6B6B", dash="dash", width=2), row=1, col=2)
fig.add_annotation(x=np.log10(30), y=single - 0.006, xref="x2", yref="y2", text=f"one full tree: {single:.2f}",
                   showarrow=False, font_size=18)
fig.update_xaxes(type="log", title="number of trees in the ensemble", tickvals=ns)
fig.update_yaxes(type="log", title="milliseconds", tickvals=[10, 30, 100, 300, 1000], col=1)
fig.update_yaxes(title="accuracy", range=[0.8, 0.9], col=2)
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1100, height=500, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=70, r=20, t=50, b=70))
fig.write_image(HERE / "cost_benefit.png", scale=2)
fig.write_image(HERE / "cost_benefit.pdf")
