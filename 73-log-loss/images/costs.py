"""Note 73 figures (Plotly): the cost −log(p) of one point; per-point costs of the two toy models."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)

p = np.linspace(0.005, 1, 400)
fig = go.Figure(go.Scatter(x=p, y=-np.log(p), mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False))
for v in (0.1, 0.4, 0.7, 0.9):
    fig.add_trace(go.Scatter(x=[v], y=[-np.log(v)], mode="markers+text", marker=dict(size=11, color="#E45756"),
                             text=[f"p = {v}: cost {-np.log(v):.2f}"], textposition="top right",
                             textfont=dict(color="#E45756", size=15), showlegend=False))
fig.update_layout(template="simple_white", width=900, height=450, font=font, margin=dict(l=70, r=20, t=50, b=60),
                  title=dict(text="Cost of one point: −log(probability the model gave to its true class)", x=0.5),
                  xaxis=dict(title="probability given to the true class", range=[0, 1.02]),
                  yaxis=dict(title="cost  −log p", range=[0, 5]))
fig.write_image(here / "neg_log.png", scale=2); fig.write_image(here / "neg_log.pdf")

pts = ["point 1 (green)", "point 2 (red)", "point 3 (green)", "point 4 (red)"]
m1, m2 = np.array([0.7, 0.4, 0.4, 0.8]), np.array([0.7, 0.6, 0.7, 0.6])
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("Probability given to the true class", "Cost −log p of each point"))
for m, name, c in ((m1, "model 1", "#F58518"), (m2, "model 2", "#B279A2")):
    fig.add_trace(go.Bar(x=pts, y=m, name=f"{name}: likelihood {m.prod():.3f}", marker_color=c,
                         text=[f"{v:.1f}" for v in m], textposition="outside"), 1, 1)
    fig.add_trace(go.Bar(x=pts, y=-np.log(m), name=f"{name}: cross entropy {-np.log(m).sum():.2f}", marker_color=c,
                         opacity=0.6, text=[f"{v:.2f}" for v in -np.log(m)], textposition="outside"), 1, 2)
fig.update_yaxes(range=[0, 1.1], row=1, col=1)
fig.update_yaxes(range=[0, 1.1], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, font=font, barmode="group",
                  margin=dict(l=60, r=20, t=50, b=110), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(here / "two_models.png", scale=2); fig.write_image(here / "two_models.pdf")
