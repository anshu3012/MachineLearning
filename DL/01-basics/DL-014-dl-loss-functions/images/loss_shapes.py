"""MSE, MAE and Huber loss of one row against its error, and the slope of each (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, GREY, FONT

here = Path(__file__).parent
e = np.linspace(-4, 4, 801)
delta = 1.0
huber = np.where(np.abs(e) <= delta, 0.5 * e ** 2, delta * (np.abs(e) - 0.5 * delta))
curves = {"MSE  (y − ŷ)²": (e ** 2, -2 * e, BLUE),
          "MAE  |y − ŷ|": (np.abs(e), -np.sign(e), ORANGE),
          "Huber, δ = 1": (huber, -np.clip(e, -delta, delta), GREEN)}
fig = make_subplots(rows=1, cols=2, subplot_titles=("Loss of one row", "Slope ∂L/∂ŷ: how hard the row pushes"),
                    horizontal_spacing=0.1)
for name, (loss, slope, c) in curves.items():
    fig.add_trace(go.Scatter(x=e, y=loss, name=name, line=dict(color=c, width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=e, y=slope, name=name, line=dict(color=c, width=4), showlegend=False), row=1, col=2)
for col in (1, 2):
    fig.update_xaxes(title_text="error y − ŷ", row=1, col=col)
fig.update_yaxes(range=[0, 8], title_text="loss", row=1, col=1)
fig.update_yaxes(range=[-8, 8], title_text="slope", zeroline=True, row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, font=FONT,
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=30, t=60, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=18))
fig.write_image(here / "loss_shapes.png", scale=2)
fig.write_image(here / "loss_shapes.pdf")
