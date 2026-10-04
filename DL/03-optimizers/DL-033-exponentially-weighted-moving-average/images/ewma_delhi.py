"""Delhi daily mean temperature (2013-2016) with its simple mean and its EWMA, beta = 0.9 (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "delhi_climate.csv", parse_dates=["date"])
theta = d.meantemp.to_numpy()
v, beta = theta[0], 0.9                       # start: V_0 = theta_1
ewma = []
for t in theta:
    v = beta * v + (1 - beta) * t
    ewma.append(v)

fig = go.Figure()
fig.add_trace(go.Scatter(x=d.date, y=theta, mode="markers", name="daily mean temperature",
                         marker=dict(color=GREY, size=4, opacity=0.5)))
fig.add_trace(go.Scatter(x=d.date, y=[theta.mean()] * len(d), name=f"simple mean ({theta.mean():.1f} °C)",
                         line=dict(color=RED, width=3)))
fig.add_trace(go.Scatter(x=d.date, y=ewma, name="EWMA, β = 0.9", line=dict(color=BLUE, width=3)))
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT,
                  yaxis=dict(title="temperature (°C)"), xaxis=dict(title="date"),
                  legend=dict(orientation="h", x=0, y=1.12), margin=dict(l=70, r=20, t=40, b=60))
fig.write_image(here / "ewma_delhi.png", scale=2)
fig.write_image(here / "ewma_delhi.pdf")
