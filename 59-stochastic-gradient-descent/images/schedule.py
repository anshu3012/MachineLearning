"""The learning schedule eta_t = t0 / (t + t1) with t0 = 5, t1 = 50, against a constant rate (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
t = np.arange(0, 10001)
eta = 5 / (t + 50)
assert np.allclose(eta[[0, 100, 1000, 10000]], [0.1, 0.0333, 0.00476, 0.000498], atol=1e-4)   # the Note's table
fig = go.Figure([go.Scatter(x=t + 1, y=eta, mode="lines", line=dict(color="#54A24B", width=4), name="schedule 5 / (t + 50)"),
                 go.Scatter(x=[1, 10001], y=[0.05, 0.05], mode="lines", line=dict(color="#F58518", width=3, dash="dash"),
                            name="constant 0.05")])
for tt in (0, 100, 1000, 10000):
    fig.add_annotation(x=np.log10(tt + 1), y=np.log10(5 / (tt + 50)), text=f"t = {tt:,}: {5 / (tt + 50):.4f}".rstrip("0"),
                       ax=0, ay=-40 if tt < 10000 else -45, font=dict(size=18), arrowcolor="#6B6B6B")
fig.update_layout(template="simple_white", width=900, height=480, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="update t + 1 (log scale)", type="log", dtick=1), yaxis=dict(title="learning rate (log scale)", type="log",
                  range=[-3.6, -0.5], dtick=1), legend=dict(x=0.02, y=0.05), margin=dict(l=80, r=40, t=20, b=70))
fig.write_image(here / "schedule.png", scale=2)
fig.write_image(here / "schedule.pdf")
