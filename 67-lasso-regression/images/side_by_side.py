"""Ridge and Lasso loss curves side by side (Plotly frames -> GIF), on the 100-observation example with the intercept
held at -2.29. Both panels use the same lambda in every frame: 0, 1000, 2000, 3000, 4000, 5000, 8000.
Left: squared error + lambda m^2; the lowest point glides towards 0 and is still 0.30 at lambda = 8000.
Right: squared error + lambda |m|; a corner grows at m = 0 and from lambda = 5000 the lowest point is exactly 0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from gifkit import BLUE, FONT, ORANGE, RED, make_gif

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
SXY, SXX = float((x * (y + 2.29)).sum()), float((x * x).sum())
ms = np.linspace(-10, 35, 901)
sse = np.array([((y - m * x + 2.29) ** 2).sum() for m in ms])
LAMS = [0, 1000, 2000, 3000, 4000, 5000, 8000]
ridge_m = lambda l: SXY / (SXX + l)
lasso_m = lambda l: max(0.0, (SXY - l / 2) / SXX)
assert round(ridge_m(8000), 2) == 0.30 and lasso_m(4000) > 0 and lasso_m(5000) == 0
for l in LAMS:      # the formulas agree with the lowest point of each drawn curve
    assert abs(ms[np.argmin(sse + l * ms ** 2)] - ridge_m(l)) < 0.06 and abs(ms[np.argmin(sse + l * np.abs(ms))] - lasso_m(l)) < 0.06


def frame(l):
    fig = make_subplots(1, 2, subplot_titles=("Ridge: squared error + λm²", "Lasso: squared error + λ|m|"))
    for col, pen, mb, colour in ((1, l * ms ** 2, ridge_m(l), BLUE), (2, l * np.abs(ms), lasso_m(l), ORANGE)):
        tot = (sse + pen) / 1e3
        fig.add_scatter(x=ms, y=tot, mode="lines", line=dict(color=colour, width=5), row=1, col=col)
        fig.add_scatter(x=[mb], y=[np.interp(mb, ms, tot)], mode="markers", marker=dict(size=18, color=RED, line=dict(width=2, color="black")), row=1, col=col)
        word = "exactly 0" if mb == 0 else f"{mb:.2f}"
        fig.add_annotation(x=21, y=395, text=f"lowest point: m = {word}", showarrow=False, font=dict(size=26, color=RED), row=1, col=col)
        fig.add_vline(x=0, line=dict(color="grey", dash="dot", width=2), row=1, col=col)
    fig.update_xaxes(title="slope m", range=[-10, 35])
    fig.update_yaxes(range=[0, 420])
    fig.update_yaxes(title="loss (thousands)", col=1)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"λ = {l:,}", x=0.5, y=0.97), margin=dict(l=80, r=30, t=100, b=70))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    make_gif([frame(l) for l in LAMS], here / "side_by_side", fps=1, holds=[3, 2, 2, 2, 2, 3, 5], keys=[2, 5], cols=1, width=1000)
