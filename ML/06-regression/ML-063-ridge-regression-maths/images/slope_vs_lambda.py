"""Ridge slope for one input: m = sum((x - x_bar)(y - y_bar)) / (sum((x - x_bar)^2) + lambda), on the 100-point example (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
num = float(((x - x.mean()) * (y - y.mean())).sum()); den = float(((x - x.mean()) ** 2).sum())
lam = np.linspace(0, 1000, 400)
fig = go.Figure(go.Scatter(x=lam, y=num / (den + lam), mode="lines", line=dict(color="#4C78A8", width=4)))
for l, c in ((0, "#E45756"), (10, "#54A24B"), (100, "#F58518")):
    m = num / (den + l)
    fig.add_trace(go.Scatter(x=[l], y=[m], mode="markers+text", marker=dict(size=12, color=c), text=[f"λ = {l}: m = {m:.2f}"],
                             textposition="middle right", textfont=dict(size=15, color=c)))
fig.update_layout(template="simple_white", width=900, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=30, t=60, b=60),
                  title=dict(text=f"m = {num:.1f} / ({den:.2f} + λ): the slope shrinks towards 0 but never reaches it", x=0.5),
                  xaxis=dict(title="λ"), yaxis=dict(title="slope m", range=[0, 30]))
print(num, den)
fig.write_image(here / "slope_vs_lambda.png", scale=2)
fig.write_image(here / "slope_vs_lambda.pdf")
