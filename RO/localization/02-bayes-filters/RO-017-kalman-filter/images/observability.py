"""Observability in numbers: the variance of the position estimate over ten steps, for a filter that reads
position (it stays small) and one that reads only speed (it keeps growing: position cannot be rebuilt from speed).
Run: python observability.py -> observability.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED
from kfsim import H, Z, kf2d

here = Path(__file__).parent
a = [r["P"][0, 0] for r in kf2d()]
b = [r["P"][0, 0] for r in kf2d(z=np.full(10, 0.5), Hm=np.array([[0.0, 1.0]]))]
print("position sensor", round(a[-1], 3), "speed sensor", round(b[-1], 3))
t = np.arange(1, 11)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=a, mode="lines+markers", line=dict(color=BLUE, width=4), name="reads position: H = [1, 0]"))
fig.add_trace(go.Scatter(x=t, y=b, mode="lines+markers", line=dict(color=RED, width=4), name="reads speed only: H = [0, 1]"))
fig.update_layout(template="simple_white", font=FONT, width=950, height=500, margin=dict(l=90, r=30, t=40, b=70),
                  legend=dict(x=0.01, y=0.99, font=dict(size=18)),
                  xaxis=dict(title="step", dtick=1), yaxis=dict(title="variance of the position estimate (m²)"))
fig.write_image(here / "observability.png")
