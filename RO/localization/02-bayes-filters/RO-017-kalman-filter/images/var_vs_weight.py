"""Choosing the weight of the reading: the variance of the blended estimate w z + (1 - w) x_pred, for the first
step's numbers (prediction variance 1.01, reading variance 0.16). w = 0 keeps the prediction (1.01), w = 1 takes the
reading (0.16); the lowest point is w = 1.01 / 1.17 = 0.863, variance 0.138. Run: python var_vs_weight.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
pb, r = 1.01, 0.16
w = np.linspace(0, 1, 400)
v = w ** 2 * r + (1 - w) ** 2 * pb
k = pb / (pb + r)
vk = k ** 2 * r + (1 - k) ** 2 * pb
assert abs(k - 0.8632) < 1e-4 and abs(vk - 0.1381) < 1e-4
fig = go.Figure(go.Scatter(x=w, y=v, line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=[k], y=[vk], mode="markers", marker=dict(color=RED, size=16)))
fig.add_annotation(x=k, y=vk, text=f"lowest: w = {k:.3f}, variance {vk:.3f}", ax=-160, ay=-120, arrowcolor=RED,
                   font=dict(size=19, color=RED))
fig.add_annotation(x=0, y=pb, text="w = 0: keep the prediction, 1.01", showarrow=False, xanchor="left", yanchor="bottom",
                   font=dict(size=18))
fig.add_annotation(x=1, y=r, text="w = 1: take the reading, 0.16", showarrow=False, xanchor="right", yanchor="bottom",
                   yshift=40, font=dict(size=18))
fig.update_layout(template="simple_white", font=FONT, width=950, height=520, showlegend=False,
                  margin=dict(l=90, r=30, t=40, b=70),
                  xaxis=dict(title="weight w given to the reading"),
                  yaxis=dict(title="variance of the estimate (m²)", range=[0, 1.15]))
fig.write_image(here / "var_vs_weight.png")
