"""Time to compute the inverse of an m x m matrix (as in (X^T X)^-1) as m grows: roughly m cubed (Plotly).
Real timings on this computer, median of several runs."""
from pathlib import Path
import time
import numpy as np
import plotly.graph_objects as go
from threadpoolctl import threadpool_limits

here = Path(__file__).parent
rng = np.random.default_rng(0)
sizes = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
times = []
for m in sizes:
    A = rng.random((m, m)) + m * np.eye(m)
    runs = []
    with threadpool_limits(limits=1):          # one core, so other programs disturb the timing less
        for _ in range(5):
            t = time.perf_counter(); np.linalg.inv(A); runs.append(time.perf_counter() - t)
    times.append(float(np.median(runs)))
    print(m, round(times[-1], 4))
fig = go.Figure(go.Scatter(x=sizes, y=times, mode="lines+markers", line=dict(color="#4C78A8", width=4),
                           marker=dict(size=9)))
fig.add_annotation(x=sizes[-1], y=times[-1], ax=-120, ay=0, text=f"{sizes[-1]} columns: {times[-1]:.2f} s",
                   font=dict(size=16), arrowcolor="#6B6B6B")
r = times[-1] / times[3]  # 2000 vs 1000 columns
fig.add_annotation(x=1000, y=times[3], ax=0, ay=-60, text=f"1000 columns: {times[3]:.2f} s<br>2× the columns → {r:.1f}× the time",
                   font=dict(size=15), arrowcolor="#6B6B6B")
fig.update_layout(template="simple_white", width=900, height=470, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text="Time to invert an m × m matrix (measured, one CPU core)", x=0.5),
                  xaxis=dict(title="m (number of input columns)"), yaxis=dict(title="Seconds"),
                  margin=dict(l=70, r=30, t=60, b=60))
fig.write_image(here / "inverse_cost.png", scale=2)
fig.write_image(here / "inverse_cost.pdf")
