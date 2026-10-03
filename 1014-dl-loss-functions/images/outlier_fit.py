"""A line fitted to data with 25% outliers using MSE, MAE and Huber loss (fits come from the Notebook) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "outlier_fit.npz")
x, y, out = d["x"], d["y"], d["is_out"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=x[~out], y=y[~out], mode="markers", name="75% of points: y = 2x + 1",
                         marker=dict(color=GREY, size=9)))
fig.add_trace(go.Scatter(x=x[out], y=y[out], mode="markers", name="25% outliers (8 higher)",
                         marker=dict(color=RED, size=10, symbol="diamond")))
xs = np.array([0, 10])
for name, c, dash in (("MSE", BLUE, None), ("MAE", ORANGE, "dash"), ("Huber", GREEN, "dot")):
    m, b = d[name]
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", name=f"{name}: ŷ = {m:.2f}x + {b:.2f}",
                             line=dict(color=c, width=4, dash=dash)))
fig.update_layout(template="simple_white", width=950, height=520, font=FONT,
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="x"), yaxis=dict(title="y"), margin=dict(l=70, r=30, t=30, b=60))
fig.write_image(here / "outlier_fit.png", scale=2)
fig.write_image(here / "outlier_fit.pdf")
