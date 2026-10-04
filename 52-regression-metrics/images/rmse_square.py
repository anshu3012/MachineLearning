"""RMSE as a picture (Plotly). Each test error drawn as a square with side |error| (grey outlines, all from one
corner). MSE is the average area of these squares; the orange square has that area, 0.121 LPA², so its side is
RMSE = 0.348 LPA. The blue square has side MAE = 0.288 LPA, the average side. The big squares pull the average area
up, so RMSE is longer than MAE."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import pred, y
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
a = np.abs(y - pred)
MAE, MSE = a.mean(), (a ** 2).mean()
RMSE = np.sqrt(MSE)
assert (round(MAE, 3), round(MSE, 3), round(RMSE, 3)) == (0.288, 0.121, 0.348)
fig = go.Figure()
for s in a:
    fig.add_shape(type="rect", x0=0, y0=0, x1=s, y1=s, line=dict(color=GREY, width=1.5), fillcolor="rgba(0,0,0,0)", layer="below")
fig.add_shape(type="rect", x0=0, y0=0, x1=RMSE, y1=RMSE, line=dict(color=ORANGE, width=6), opacity=1,
              fillcolor="rgba(245,133,24,0.18)")
fig.add_shape(type="rect", x0=0, y0=0, x1=MAE, y1=MAE, line=dict(color=BLUE, width=5, dash="dash"), fillcolor="rgba(0,0,0,0)", opacity=1)
fig.add_annotation(x=RMSE, y=RMSE, text=f"area = MSE = {MSE:.3f} LPA²<br>side = RMSE = {RMSE:.3f} LPA", ax=150,
                   ay=-60, font=dict(size=22, color=ORANGE), arrowcolor=ORANGE)
fig.add_annotation(x=MAE, y=MAE / 2, text=f"side = MAE = {MAE:.3f} LPA", ax=200, ay=-10, font=dict(size=22, color=BLUE),
                   arrowcolor=BLUE)
fig.add_annotation(x=a.max(), y=a.max(), text=f"largest error: {a.max():.2f}", ax=-40, ay=-30, font=dict(size=18))
fig.add_scatter(x=[None], y=[None], mode="lines", line=dict(color=GREY), name="one square per test error")
fig.update_layout(template="simple_white", width=900, height=820, font=FONT, showlegend=True,
                  legend=dict(x=0.55, y=0.99),
                  xaxis=dict(title="LPA", range=[0, 1.0], constrain="domain"),
                  yaxis=dict(title="LPA", range=[0, 1.0], scaleanchor="x"), margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "rmse_square.png", scale=2)
