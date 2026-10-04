"""The OLS line on the 160 training students passes through the point of means (x-bar, y-bar) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import B, M, X_train, y_train

here = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
xb, yb = x.mean(), y.mean()
assert abs(M * xb + B - yb) < 1e-9                               # b = y-bar - m x-bar
xs = np.array([4, 10])
fig = go.Figure([
    go.Scatter(x=x, y=y, mode="markers", marker=dict(size=7, color="#6B6B6B", opacity=0.7)),
    go.Scatter(x=xs, y=M * xs + B, mode="lines", line=dict(color="#4C78A8", width=4)),
    go.Scatter(x=[xb, xb], y=[0.8, yb], mode="lines", line=dict(color="#F58518", dash="dash", width=2)),
    go.Scatter(x=[4, xb], y=[yb, yb], mode="lines", line=dict(color="#F58518", dash="dash", width=2)),
    go.Scatter(x=[xb], y=[yb], mode="markers", marker=dict(size=18, color="#F58518", line=dict(color="white", width=2)))])
fig.add_annotation(x=xb, y=yb, ax=-110, ay=-70, text=f"(x̄, ȳ) = ({xb:.2f}, {yb:.2f})", font=dict(size=22, color="#F58518"),
                   arrowcolor="#F58518")
fig.add_annotation(x=9.0, y=M * 9.0 + B, ax=-30, ay=90, text=f"y = {M:.3f}x − {-B:.3f}", font=dict(size=22, color="#4C78A8"),
                   arrowcolor="#4C78A8")
fig.update_layout(template="simple_white", width=900, height=520, showlegend=False, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="CGPA", range=[4, 10]), yaxis=dict(title="package", range=[0.8, 5]), margin=dict(l=70, r=30, t=20, b=60))
fig.write_image(here / "through_means.png", scale=2)
fig.write_image(here / "through_means.pdf")
