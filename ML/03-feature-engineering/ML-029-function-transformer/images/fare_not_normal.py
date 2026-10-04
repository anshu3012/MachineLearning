"""Real data is rarely normal: the 891 Titanic fares (density histogram) against the normal curve with the same mean
(32.20) and standard deviation (49.69). Most fares are small, a few are huge; the normal curve even puts density
below 0, where no fare can be."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv").Fare
m, s = fare.mean(), fare.std()
assert (round(m, 2), round(s, 2), round(fare.median(), 2), round(fare.max(), 2)) == (32.20, 49.69, 14.45, 512.33)
assert stats.norm(m, s).cdf(0) > 0.2                     # the matching normal puts over 20 percent below 0
x = np.linspace(-150, 520, 500)
fig = go.Figure()
fig.add_histogram(x=fare, histnorm="probability density", xbins=dict(start=0, end=520, size=10),
                  marker_color="rgba(76,120,168,0.6)", name="891 Titanic fares")
fig.add_scatter(x=x, y=stats.norm(m, s).pdf(x), mode="lines", line=dict(color="#E45756", width=4, dash="dash"),
                name="normal curve, same mean and SD")
fig.add_annotation(x=14.45, y=0.032, text="median 14.45", ax=80, ay=-30, font=dict(size=19), arrowwidth=2)
fig.add_annotation(x=512.33, y=0.0006, text="largest fare 512.33", ax=-40, ay=-70, font=dict(size=19), arrowwidth=2)
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text=f"Titanic fares: skewness {fare.skew():.2f}, far from a bell", x=0.5), bargap=0.05,
                  xaxis=dict(title="fare"), yaxis=dict(title="density", range=[0, 0.04]),
                  legend=dict(x=0.45, y=0.95), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "fare_not_normal.png", scale=2)
fig.write_image(here / "fare_not_normal.pdf")
