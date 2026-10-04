"""Bernoulli NLL, observation by observation (Plotly). Model 1 of the log loss Note: targets 1, 0, 1, 0 with predicted
probabilities 0.7, 0.6, 0.4, 0.2. The Bernoulli PMF gives each observation's true target the probability 0.7, 0.4,
0.4, 0.8. Left: the curve -log q with the four points (0.357, 0.916, 0.916, 0.223). Right: the four terms stacked,
total NLL 2.41."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
y = np.array([1, 0, 1, 0])
yhat = np.array([0.7, 0.6, 0.4, 0.2])
q = yhat ** y * (1 - yhat) ** (1 - y)                        # Bernoulli PMF at the true target
assert np.allclose(q, [0.7, 0.4, 0.4, 0.8])
terms = -np.log(q)
assert abs(terms.sum() - 2.41) < 0.005
cols = [BLUE, ORANGE, GREEN, PURPLE]

fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.14,
                    subplot_titles=("−log of the probability of the true target", "NLL = sum of the terms"))
g = np.linspace(0.03, 1, 300)
fig.add_trace(go.Scatter(x=g, y=-np.log(g), mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, 1)
for i in range(4):
    lab = f"obs {i + 1}: y = {y[i]}, ŷ = {yhat[i]}"
    fig.add_trace(go.Scatter(x=[q[i]], y=[terms[i]], mode="markers", marker=dict(size=24 if i == 1 else 14, color=cols[i]),
                             name=f"{lab} → q = {q[i]:.1f}, −log q = {terms[i]:.3f}"), 1, 1)
    fig.add_trace(go.Bar(x=["model 1"], y=[terms[i]], marker_color=cols[i], showlegend=False,
                         text=[f"{terms[i]:.3f}"], textposition="inside", textfont=dict(size=19, color="white")), 1, 2)
fig.add_annotation(x="model 1", y=terms.sum(), text=f"total {terms.sum():.2f}", showarrow=False, yshift=18,
                   font=dict(size=21), xref="x2", yref="y2")
fig.update_xaxes(title_text="probability q given to the true target", range=[0, 1.02], row=1, col=1)
fig.update_yaxes(title_text="−log q", range=[0, 2.7], row=1, col=1)
fig.update_yaxes(range=[0, 2.7], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=640, barmode="stack",
                  font=dict(family="Latin Modern Roman", size=20), legend=dict(x=0, y=-0.2, yanchor="top", traceorder="normal"),
                  margin=dict(l=70, r=20, t=50, b=200))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "bernoulli_nll.png", scale=2)
fig.write_image(HERE / "bernoulli_nll.pdf")
