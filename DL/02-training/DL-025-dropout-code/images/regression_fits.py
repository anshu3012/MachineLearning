"""Regression: the fitted curve for dropout rates 0, 0.2, 0.5 and 0.75 (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, RED, FONT

here = Path(__file__).parent
d = here.parent / "data"
pts, cur, sc = (pd.read_csv(d / f) for f in ("regression_points.csv", "regression_curves.csv", "regression_scores.csv"))
ps = [0, 0.2, 0.5, 0.75]
titles = [f"p = {p}: train MSE {r.train_mse:.3f}, test MSE {r.test_mse:.3f}" for p, r in zip(ps, sc.itertuples())]
fig = make_subplots(2, 2, subplot_titles=titles, horizontal_spacing=0.08, vertical_spacing=0.14)
for k, p in enumerate(ps):
    r, c = k // 2 + 1, k % 2 + 1
    fig.add_scatter(x=pts.x, y=pts.y_train, mode="markers", name="training points", marker=dict(color="black", size=8),
                    showlegend=k == 0, row=r, col=c)
    fig.add_scatter(x=pts.x, y=pts.y_test, mode="markers", name="test points", marker=dict(color=RED, size=8),
                    showlegend=k == 0, row=r, col=c)
    fig.add_scatter(x=cur.x, y=cur[f"p={p}"], mode="lines", name="network's prediction", line=dict(color=BLUE, width=3),
                    showlegend=k == 0, row=r, col=c)
fig.update_xaxes(title="x", row=2)
fig.update_yaxes(title="y", col=1)
fig.update_layout(template="simple_white", width=1150, height=820, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.1), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "regression_fits.png", scale=2)
fig.write_image(here / "regression_fits.pdf")
