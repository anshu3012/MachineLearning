"""The product-page example of section 5: Binomial(n = 1000, p = 0.1). P(X = 50) = 3.2e-9 (invisible), P(X = 100) =
0.042 (the peak), P(X >= 70) = 0.9996 (shaded)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
b = stats.binom(1000, 0.1)
assert f"{b.pmf(50):.1e}" == "3.2e-09" and round(b.pmf(100), 3) == 0.042 and round(b.sf(69), 4) == 0.9996
k = np.arange(40, 161)
pm = b.pmf(k)
fig = go.Figure(go.Bar(x=k, y=pm, marker_color=["#F58518" if v >= 70 else "#9a9a9a" for v in k], width=0.9))
fig.add_annotation(x=100, y=b.pmf(100), text="P(X = 100) = 0.042", ax=110, ay=-30, font=dict(size=19), arrowwidth=2)
fig.add_annotation(x=50, y=0.0005, text="P(X = 50) = 3.2 × 10<sup>−9</sup>:<br>too small to see", ax=20, ay=-90,
                   font=dict(size=19), arrowwidth=2)
fig.add_annotation(x=135, y=0.03, text="orange: P(X ≥ 70) = 0.9996", showarrow=False, font=dict(size=19, color="#c55a00"))
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="Buyers among 1,000 page views, p = 0.1: Binomial(1000, 0.1)", x=0.5), bargap=0,
                  xaxis=dict(title="number of buyers x"), yaxis=dict(title="P(X = x)", range=[0, 0.05]),
                  margin=dict(l=90, r=30, t=70, b=70))
fig.write_image(here / "buyers_pmf.png", scale=2)
fig.write_image(here / "buyers_pmf.pdf")
