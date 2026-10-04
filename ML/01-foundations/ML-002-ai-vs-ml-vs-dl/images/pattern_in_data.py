"""A pattern in data: marks rise with hours studied. Example data, not real. Plotly: a scatter with its fitted line."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
rng = np.random.default_rng(7)
hours = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7])
marks = np.clip(10 * hours + 15 + rng.normal(0, 5, hours.size), 0, 100).round()
m, b = np.polyfit(hours, marks, 1)
xs = np.array([hours.min(), hours.max()])

fig = go.Figure()
fig.add_scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color="#F58518", width=5), showlegend=False)
fig.add_scatter(x=hours, y=marks, mode="markers", marker=dict(size=15, color="#4C78A8"), showlegend=False)
fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Pattern found: about 10 extra marks per hour studied", x=0.5),
                  xaxis=dict(title="Hours studied", showgrid=True), yaxis=dict(title="Exam marks", showgrid=True),
                  margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "pattern_in_data.png", scale=2)
fig.write_image(here / "pattern_in_data.pdf")
