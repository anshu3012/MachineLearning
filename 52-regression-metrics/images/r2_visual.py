"""R2 compares the line's squared errors with those of the average-only 'model' (Plotly, test set)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import x, y, pred, lr, BLUE, ORANGE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
ybar = y.mean()
sst, ssr = float(((y - ybar) ** 2).sum()), float(((y - pred) ** 2).sum())
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=(
    f"Guess the average for everyone<br>squared errors add up to {sst:.2f}",
    f"Regression line<br>squared errors add up to {ssr:.2f}"))
xs = np.array([4.3, 9.4])
for col, yhat, colour in ((1, np.full_like(y, ybar), RED), (2, pred, ORANGE)):
    segx, segy = [], []
    for a, b, c in zip(x, y, yhat):
        segx += [a, a, None]; segy += [b, c, None]
    fig.add_trace(go.Scatter(x=segx, y=segy, mode="lines", line=dict(color=GREY, width=1.5)), 1, col)
    line_y = [ybar, ybar] if col == 1 else lr.coef_[0] * xs + lr.intercept_
    fig.add_trace(go.Scatter(x=xs, y=line_y, mode="lines", line=dict(color=colour, width=4)), 1, col)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=8, color=BLUE)), 1, col)
    fig.update_xaxes(title="CGPA", row=1, col=col)
    fig.update_yaxes(title="Package (LPA)" if col == 1 else None, range=[1.2, 4.6], row=1, col=col)
fig.update_layout(template="simple_white", width=1050, height=480, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=80, b=60))
fig.update_annotations(font_size=17)
print(f"SST {sst:.3f} SSR {ssr:.3f} R2 {1 - ssr / sst:.4f}")
fig.write_image(here / "r2_visual.png", scale=2)
fig.write_image(here / "r2_visual.pdf")
