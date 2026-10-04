"""How the penalty moves the minimum (Plotly frames -> GIF), on the 100-observation example. For each slope m the
intercept is set to its best value b = y-bar - m x-bar; the loss is then the squared error (blue, the same for every
lambda) plus the penalty lambda m^2 (orange). As lambda grows from 0 to 100, the bottom of the total (green) slides
from m = 27.83 towards 0, reaching 12.93 at lambda = 100: num / (den + lambda)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
num, den = ((x - x.mean()) * (y - y.mean())).sum(), ((x - x.mean()) ** 2).sum()
ms = np.linspace(-5, 40, 451)
sse = np.array([((y - m * x - (y.mean() - m * x.mean())) ** 2).sum() for m in ms])
LAMS = [0, 5, 10, 20, 40, 60, 80, 100]
for l in LAMS:
    tot = sse + l * ms ** 2
    assert abs(ms[np.argmin(tot)] - num / (den + l)) < 0.1


def frame(l):
    tot = sse + l * ms ** 2
    mb = num / (den + l)
    fig = go.Figure([go.Scatter(x=ms, y=sse / 1e3, mode="lines", line=dict(color=BLUE, width=3), name="squared error"),
                     go.Scatter(x=ms, y=l * ms ** 2 / 1e3, mode="lines", line=dict(color=ORANGE, width=3, dash="dash"), name="penalty λm²"),
                     go.Scatter(x=ms, y=tot / 1e3, mode="lines", line=dict(color=GREEN, width=5), name="Ridge loss = sum")])
    fig.add_scatter(x=[mb], y=[(sse[np.argmin(np.abs(ms - mb))] + l * mb ** 2) / 1e3], mode="markers+text",
                    text=[f"minimum at m = {mb:.2f}"], textposition="top center", textfont=dict(size=20, color=GREEN),
                    marker=dict(size=14, color=GREEN), showlegend=False)
    fig.add_vline(x=num / den, line=dict(color=BLUE, dash="dot", width=2), opacity=1)
    fig.update_layout(template="simple_white", width=1000, height=580, font=FONT,
                      title=dict(text=f"λ = {l}", x=0.5), xaxis=dict(title="slope m (intercept at its best value)"),
                      yaxis=dict(title="loss (thousands)", range=[0, 260]), legend=dict(x=0.01, y=0.99),
                      margin=dict(l=80, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(l) for l in LAMS], here / "loss_shift", fps=1, holds=[3] + [1] * (len(LAMS) - 2) + [4],
             keys=[0, len(LAMS) - 1], cols=1)
