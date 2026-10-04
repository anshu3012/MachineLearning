"""What every regression metric summarises (Plotly): the 40 test students, the regression line, and each student's
error as a vertical stick (blue above the line, red below). The five metrics of the Note turn these 40 sticks into
one number each."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import lr, pred, x, y
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
e = y - pred
assert len(e) == 40 and round(np.abs(e).mean(), 3) == 0.288 and round((e ** 2).mean(), 3) == 0.121
assert round(np.sqrt((e ** 2).mean()), 3) == 0.348 and round(1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(), 3) == 0.781
fig = go.Figure()
for mask, c, name in ((e > 0, BLUE, "actual above prediction"), (e <= 0, RED, "actual below prediction")):
    sx, sy = [], []
    for xi, yi, pi in zip(x[mask], y[mask], pred[mask]):
        sx += [xi, xi, None]; sy += [yi, pi, None]
    fig.add_scatter(x=sx, y=sy, mode="lines", line=dict(color=c, width=3), name=name)
xs = np.array([4.3, 9.3])
fig.add_scatter(x=xs, y=lr.coef_[0] * xs + lr.intercept_, mode="lines", line=dict(color=ORANGE, width=4),
                name="the model's predictions")
fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=10, color=GREY, line=dict(color="white", width=1)),
                name="test students (actual)")
fig.add_annotation(x=0.99, y=0.03, xref="paper", yref="paper", xanchor="right", yanchor="bottom", showarrow=False,
                   align="right", font=dict(size=22),
                   text="40 errors  →  one number<br>MAE 0.288 · MSE 0.121 · RMSE 0.348 · R² 0.781")
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  xaxis=dict(title="CGPA (the feature)"), yaxis=dict(title="package in LPA (the target)"),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "test_errors.png", scale=2)
