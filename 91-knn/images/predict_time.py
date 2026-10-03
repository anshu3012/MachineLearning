"""Lazy learning: fit time vs prediction time of brute-force KNN as the training set grows (Plotly)."""
import time
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsClassifier

here = Path(__file__).parent
rng = np.random.default_rng(0)
sizes = [10_000, 50_000, 100_000, 200_000, 500_000]
queries = rng.random((1000, 30))
csv = here / "predict_time.csv"                            # measured once; delete it to re-measure
if csv.exists():
    fit_ms, pred_ms = np.loadtxt(csv, delimiter=",", unpack=True)
else:
  fit_ms, pred_ms = [], []
  for n in sizes:
      X, y = rng.random((n, 30)), rng.integers(0, 2, n)     # n rows, 30 columns
      model = KNeighborsClassifier(n_neighbors=5, algorithm="brute")
      fit_t, pred_t = [], []
      for _ in range(3):                                      # best of 3 runs, to ignore warm-up noise
          t0 = time.perf_counter(); model.fit(X, y); t1 = time.perf_counter()
          model.predict(queries); t2 = time.perf_counter()
          fit_t.append(t1 - t0); pred_t.append(t2 - t1)
      fit_ms.append(min(fit_t) * 1000); pred_ms.append(min(pred_t) * 1000)
  np.savetxt(csv, np.c_[fit_ms, pred_ms], delimiter=",", fmt="%.2f")
print("fit ms", np.round(fit_ms, 1)); print("predict 1000 rows ms", np.round(pred_ms, 1))
fig = go.Figure()
fig.add_trace(go.Bar(x=[f"{n:,}" for n in sizes], y=fit_ms, name="fit (store the data)", marker_color="#54A24B"))
fig.add_trace(go.Bar(x=[f"{n:,}" for n in sizes], y=pred_ms, name="predict 1,000 new rows", marker_color="#E45756"))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(family="Latin Modern Roman", size=17), barmode="group",
                  xaxis=dict(title="training rows (30 columns each)"), yaxis=dict(title="time (milliseconds)"),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(here / "predict_time.png", scale=2); fig.write_image(here / "predict_time.pdf")
