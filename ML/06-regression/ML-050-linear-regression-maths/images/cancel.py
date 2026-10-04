"""Why raw errors cannot measure a line: on the 160 training students, a flat line at the average package and the
best line both have errors that add up to exactly 0, yet their sums of squared errors are 73.02 and 16.55 (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import B, M, X_train, y_train
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
lines = [("a flat line at the average package", 0.0, y.mean()), ("the best line", M, B)]
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=[t for t, _, _ in lines])
fig.update_annotations(font_size=24)
for col, (_, m, b) in enumerate(lines, 1):
    d = y - (m * x + b)
    assert abs(d.sum()) < 1e-9                                   # the errors cancel exactly for both lines
    up = d > 0
    for mask, col_ in ((up, BLUE), (~up, RED)):
        sx, sy = [], []
        for xi, yi, di in zip(x[mask], y[mask], d[mask]):
            sx += [xi, xi, None]; sy += [yi, yi - di, None]
        fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=col_, width=1.6)), 1, col)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=6, color=GREY)), 1, col)
    xs = np.array([4, 10])
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=ORANGE, width=4)), 1, col)
    sse = (d ** 2).sum()
    fig.add_annotation(x=4.2, y=5.6, xref=f"x{col}", yref=f"y{col}", xanchor="left", yanchor="top", showarrow=False,
                       align="left", font=dict(size=22),
                       text=f"sum of errors = {abs(d.sum()):.2f}<br>sum of squared errors = <b>{sse:.2f}</b>")
    assert abs(sse - (73.02 if col == 1 else 16.55)) < 0.005, sse
    fig.update_xaxes(title="CGPA", range=[4, 10], row=1, col=col)
    fig.update_yaxes(title="package" if col == 1 else None, range=[0.5, 5.7], row=1, col=col)
fig.add_annotation(x=0.5, y=-0.3, xref="paper", yref="paper", showarrow=False, font=dict(size=20),
                   text="<span style='color:#4C78A8'>blue: point above the line (positive error)</span>   "
                        "<span style='color:#E45756'>red: point below (negative error)</span>")
fig.update_layout(template="simple_white", width=1200, height=560, showlegend=False, font=FONT,
                  margin=dict(l=70, r=30, t=60, b=140))
fig.write_image(here / "cancel.png", scale=2)
