"""Anomaly detection: one transaction far from all the normal ones. Example data. Plotly: a scatter."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
rng = np.random.default_rng(5)
amount, dist = rng.gamma(2.0, 1.2, 80), rng.gamma(2.0, 2.5, 80)        # normal: small and close to home

fig = go.Figure()
fig.add_scatter(x=dist, y=amount, mode="markers", name="normal", marker=dict(size=12, color="#4C78A8"))
fig.add_scatter(x=[42.0], y=[14.5], mode="markers", name="anomaly (flagged)", marker=dict(size=16, color="#E45756"))
fig.update_layout(template="simple_white", width=950, height=560, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Anomaly detection: a point far from all the others  (example data)", x=0.5),
                  xaxis=dict(title="Distance from home (km)", showgrid=True),
                  yaxis=dict(title="Amount (thousand rupees)", showgrid=True),
                  legend=dict(title="Type", x=0.7, y=0.5), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "anomaly.png", scale=2)
fig.write_image(here / "anomaly.pdf")
