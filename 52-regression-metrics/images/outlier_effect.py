"""Make one test prediction worse and worse: MAE grows slowly, RMSE (and MSE) grow much faster (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import y, pred, BLUE, ORANGE, RED, GREY, FONT

here = Path(__file__).parent
extra = np.linspace(0, 6, 61)
mae, rmse = [], []
for e in extra:
    p = pred.copy()
    p[0] += e                       # one student's prediction is off by e more LPA
    err = y - p
    mae.append(np.abs(err).mean()); rmse.append(np.sqrt((err ** 2).mean()))
fig = go.Figure()
fig.add_trace(go.Scatter(x=extra, y=mae, mode="lines", name="MAE", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=extra, y=rmse, mode="lines", name="RMSE", line=dict(color=RED, width=4)))
for xv, yv, c in ((6, mae[-1], BLUE), (6, rmse[-1], RED)):
    fig.add_annotation(x=xv, y=yv, text=f"{yv:.2f}", showarrow=False, xanchor="left", xshift=6, font=dict(color=c, size=16))
fig.update_layout(template="simple_white", width=900, height=470, font=FONT, legend=dict(x=0.02, y=0.98),
                  title=dict(text="One bad prediction among 40: how much each metric grows", x=0.5),
                  xaxis=dict(title="Extra error on one student (LPA)"), yaxis=dict(title="Metric (LPA)"),
                  margin=dict(l=70, r=60, t=60, b=60))
print(f"start MAE {mae[0]:.3f} RMSE {rmse[0]:.3f}; end MAE {mae[-1]:.3f} RMSE {rmse[-1]:.3f}")
fig.write_image(here / "outlier_effect.png", scale=2)
fig.write_image(here / "outlier_effect.pdf")
