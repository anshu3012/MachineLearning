"""The cost of KNN imputation: time to fit and transform with KNNImputer (k = 5) as the number of rows grows, on
synthetic data with 4 features and 20 percent of one feature missing (seed 0). Every row with a gap needs its distance
to every other row, so the time grows much faster than the data; mean imputation (SimpleImputer) stays near zero.
Best of 3 runs per size; exact times depend on the machine."""
from pathlib import Path
import time
import numpy as np
import plotly.graph_objects as go
from sklearn.impute import KNNImputer, SimpleImputer

here = Path(__file__).parent
NS = [1000, 2000, 4000, 8000, 16000]


def best(imp, X):
    t = []
    for _ in range(3):
        s = time.perf_counter(); imp.fit_transform(X); t.append(time.perf_counter() - s)
    return min(t)


rng = np.random.default_rng(0)
tk, ts = [], []
for n in NS:
    X = rng.normal(size=(n, 4)); X[rng.random(n) < 0.2, 0] = np.nan
    tk.append(best(KNNImputer(n_neighbors=5), X)); ts.append(best(SimpleImputer(), X))
assert tk[-1] > 100 * tk[0] and max(ts) < tk[-1] / 50
fig = go.Figure()
fig.add_scatter(x=NS, y=tk, mode="lines+markers+text", text=[f"{t:.2f} s" for t in tk], textposition="top left",
                line=dict(color="#E45756", width=4), marker=dict(size=11), name="KNNImputer (k = 5)")
fig.add_scatter(x=NS, y=ts, mode="lines+markers", line=dict(color="#4C78A8", width=4), marker=dict(size=11),
                name="SimpleImputer (mean)")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text=f"16 times the rows: {tk[-1] / tk[0]:.0f} times the KNN imputation time", x=0.5),
                  xaxis=dict(title="rows (4 features, 20 percent of one feature missing)"), yaxis=dict(title="seconds"),
                  legend=dict(x=0.03, y=0.95), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "knn_cost.png", scale=2)
fig.write_image(here / "knn_cost.pdf")
