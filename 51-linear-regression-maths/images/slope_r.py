"""The slope as r * s_y / s_x on the 160 training students. Start at the point of means, step right by one standard
deviation of CGPA (s_x); the line rises r * s_y. Dashed: the line for r = 1 (rises a full s_y) and for r = 0 (flat).
Plotly (a chart). Idea after Khan Academy, "Calculating the equation of a regression line"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import B, M, X_train, y_train

here = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#9a9a9a"
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
xb, yb, sx, sy = x.mean(), y.mean(), x.std(ddof=1), y.std(ddof=1)
r = np.corrcoef(x, y)[0, 1]
print(f"r = {r:.3f}, s_x = {sx:.3f}, s_y = {sy:.3f}, r*s_y/s_x = {r * sy / sx:.3f}, s_y/s_x = {sy / sx:.3f}, r*s_y = {r * sy:.3f}")
assert abs(r * sy / sx - M) < 1e-9 and (round(r, 3), round(sx, 3), round(sy, 3)) == (0.879, 1.068, 0.678)
assert round(r * r, 3) == 0.773                                  # equals the training R-squared quoted in Note 52
xs = np.array([4, 10])
fig = go.Figure()
fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=7, color=GREY, opacity=0.6))
fig.add_scatter(x=xs, y=yb + (sy / sx) * (xs - xb), mode="lines", line=dict(color=GREY, width=2, dash="dash"))
fig.add_scatter(x=xs, y=[yb, yb], mode="lines", line=dict(color=GREY, width=2, dash="dash"))
fig.add_scatter(x=xs, y=M * xs + B, mode="lines", line=dict(color=BLUE, width=4))
fig.add_scatter(x=[xb, xb + sx], y=[yb, yb], mode="lines", line=dict(color=GREEN, width=6))
fig.add_scatter(x=[xb + sx, xb + sx], y=[yb, yb + r * sy], mode="lines", line=dict(color=ORANGE, width=6))
fig.add_scatter(x=[xb], y=[yb], mode="markers", marker=dict(size=16, color="black"))
fig.add_annotation(x=xb, y=yb, ax=-80, ay=-70, text="(x̄, ȳ)", font=dict(size=22))
fig.add_annotation(x=xb + sx / 2, y=yb, yshift=-22, showarrow=False, text=f"right s<sub>x</sub> = {sx:.2f}", bgcolor="white",
                   font=dict(size=21, color=GREEN))
fig.add_annotation(x=xb + sx, y=yb + r * sy / 2, xshift=10, xanchor="left", showarrow=False, bgcolor="white",
                   text=f"up r × s<sub>y</sub> = {r * sy:.2f}", font=dict(size=21, color=ORANGE))
fig.add_annotation(x=9.6, y=yb + (sy / sx) * (9.6 - xb), ax=-70, ay=-25, text="r = 1", font=dict(size=20, color="#555"))
fig.add_annotation(x=9.6, y=yb, ax=0, ay=40, text="r = 0", font=dict(size=20, color="#555"))
fig.add_annotation(x=4.9, y=M * 4.9 + B, ax=40, ay=60, text=f"r = {r:.2f}: slope {M:.3f}", font=dict(size=21, color=BLUE),
                   arrowcolor=BLUE)
fig.update_layout(template="simple_white", width=900, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), xaxis=dict(title="CGPA", range=[4, 10]),
                  yaxis=dict(title="package", range=[0.8, 5.2]), margin=dict(l=70, r=30, t=20, b=60))
fig.write_image(here / "slope_r.png", scale=2)
