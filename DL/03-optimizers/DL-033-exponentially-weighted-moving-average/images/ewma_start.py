"""The first 40 days of 2013 with two starting values: V_0 = 0 and V_0 = theta_1, beta = 0.9 (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "delhi_climate.csv").head(40)
theta = d.meantemp.to_numpy()
fig = go.Figure(go.Scatter(x=list(range(1, 41)), y=theta, mode="markers", name="daily temperature",
                           marker=dict(color=GREY, size=8)))
for v0, name, c in ((0.0, "V₀ = 0", ORANGE), (theta[0], "V₀ = θ₁ (first value)", BLUE)):
    v, out = v0, []
    for t in theta:
        v = 0.9 * v + 0.1 * t
        out.append(v)
    fig.add_trace(go.Scatter(x=list(range(1, 41)), y=out, name=name, line=dict(color=c, width=4)))
fig.update_layout(template="simple_white", width=950, height=420, font=FONT,
                  xaxis=dict(title="day t"), yaxis=dict(title="temperature (°C)", range=[0, 17]),
                  legend=dict(x=0.55, y=0.08), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "ewma_start.png", scale=2)
fig.write_image(here / "ewma_start.pdf")
