"""Each student's inputs are a point in 3D space: a 3-dimensional vector, stored as a 1D tensor. Example data."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
rng = np.random.default_rng(8)
n = 40
cgpa, iq, state = rng.uniform(5.5, 9.5, n).round(1), rng.uniform(80, 130, n).round(), rng.integers(0, 2, n)
cgpa[0], iq[0], state[0] = 8.1, 91, 0                     # the highlighted student

fig = go.Figure()
fig.add_trace(go.Scatter3d(x=cgpa[1:], y=iq[1:], z=state[1:], mode="markers", name="other students",
                           marker=dict(size=5, color="#4C78A8", opacity=0.7)))
fig.add_trace(go.Scatter3d(x=cgpa[:1], y=iq[:1], z=state[:1], mode="markers+text", name="student [8.1, 91, 0]",
                           text=["[8.1, 91, 0]"], textposition="top center",
                           marker=dict(size=9, color="#E45756", symbol="diamond")))
fig.update_layout(template="simple_white", width=900, height=650, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="Each student is a point in 3D space (CGPA, IQ, State)  (example data)", x=0.5),
                  scene=dict(xaxis_title="CGPA", yaxis_title="IQ", zaxis_title="State (0 or 1)",
                             zaxis=dict(tickvals=[0, 1]), camera=dict(eye=dict(x=1.9, y=-1.9, z=1.1)), aspectmode="cube",
                             xaxis=dict(tickfont=dict(size=12)), yaxis=dict(tickfont=dict(size=12))),
                  legend=dict(x=0.02, y=0.95), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "student_space.png", scale=2)
