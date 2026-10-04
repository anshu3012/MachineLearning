"""A fat-tailed Q-Q plot: the Notebook's 1,000 standardized Laplace values (seed 0, drawn after 500 normal values)
against the normal. The middle point is on the line; the ends leave it outwards (-5.41 and 4.82 against -3.20 and
3.20)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
r = np.random.default_rng(0)
r.normal(size=500)                                   # same draws as the Notebook's audit cell
lap = r.laplace(size=1000)
z = (lap - lap.mean()) / lap.std()
(osm, osr), _ = stats.probplot(z)
assert list(osm[[0, 999]].round(2)) == [-3.2, 3.2] and list(osr[[0, 999]].round(2)) == [-5.41, 4.82]
fig = go.Figure()
fig.add_scatter(x=[-3.5, 3.5], y=[-3.5, 3.5], mode="lines", line=dict(color="black", dash="dash", width=2),
                name="y = x (a normal feature)")
fig.add_scatter(x=osm, y=osr, mode="markers", marker=dict(color="#F58518", size=7), name="1,000 Laplace values")
for i, side in ((0, "bottom"), (999, "top")):
    fig.add_annotation(x=osm[i], y=osr[i], text=f"{osr[i]:.2f} vs normal {osm[i]:.2f}", ax=-130 if i else 130,
                       ay=0, font=dict(size=19), arrowwidth=2)
fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text=f"Fat tails (excess kurtosis {stats.kurtosis(lap):.2f}): both ends leave the line outwards", x=0.5),
                  xaxis=dict(title="normal quantiles", range=[-3.6, 3.6]), yaxis=dict(title="data quantiles (z)", range=[-6, 6]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "laplace_qq.png", scale=2)
fig.write_image(here / "laplace_qq.pdf")
