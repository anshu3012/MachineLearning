"""Predicting with the step function (Plotly), using the Note's line 2x + 3y + 5 = 0, i.e. w = (5, 2, 3) with x0 = 1.
The points (2, 1), (-4, -3) and (5, 2) give w . x = 12, -12 and 21; the step function turns each into a prediction
0 or 1. The point (5, 2) is a negative-class point, so y - y_hat = -1 and the rule subtracts eta x."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, RED

here = Path(__file__).parent
w = np.array([5, 2, 3])
pts = {"(2, 1)": (2, 1), "(−4, −3)": (-4, -3), "(5, 2)": (5, 2)}
z = {k: w @ np.array([1, *p]) for k, p in pts.items()}
assert list(z.values()) == [12, -12, 21]
zs = np.linspace(-25, 25, 501)
fig = go.Figure(go.Scatter(x=zs, y=(zs > 0).astype(int), mode="lines", line=dict(color=BLUE, width=5, shape="hv"),
                           name="step: ŷ = 1 if w·x > 0, else 0"))
for (k, v), c, pos in zip(z.items(), (GREEN, RED, GREEN), ("bottom right", "top right", "top left")):
    fig.add_scatter(x=[v], y=[int(v > 0)], mode="markers+text", text=[f"{k}: w·x = {v}, ŷ = {int(v > 0)}"], textposition=pos,
                    textfont=dict(size=19, color=c), marker=dict(size=15, color=c), showlegend=False)
fig.update_layout(template="simple_white", width=950, height=480, font=FONT,
                  xaxis=dict(title="w · x = w₀ + w₁x₁ + w₂x₂", zeroline=True), yaxis=dict(title="prediction ŷ", range=[-0.35, 1.35], tickvals=[0, 1]),
                  legend=dict(x=0.01, y=0.95), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "step_rule.png", scale=2)
