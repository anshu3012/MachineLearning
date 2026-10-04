"""The z-score outlier rule on the Titanic ages: mean 29.70, sd 14.53, limits mean +- 3 sd = -13.88 and 73.28;
the two passengers aged 74 and 80 lie beyond the upper limit."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv").Age.dropna()
m, s = age.mean(), age.std()
lo, hi = m - 3 * s, m + 3 * s
assert (round(m, 2), round(s, 2), round(lo, 2), round(hi, 2)) == (29.70, 14.53, -13.88, 73.28)
out = sorted(age[age > hi])
assert out == [74, 80]
fig = go.Figure()
fig.add_histogram(x=age, xbins=dict(start=0, end=82, size=2), marker_color="rgba(76,120,168,0.6)")
fig.add_vline(x=m, line=dict(color="black", width=2))
for v, t in ((m + s, "+1σ"), (m + 2 * s, "+2σ"), (hi, "+3σ = 73.28")):
    fig.add_vline(x=v, line=dict(color="#E45756", width=2, dash="dash"))
    fig.add_annotation(x=v, y=62, text=t, showarrow=False, xanchor="left", xshift=4, font=dict(size=18, color="#E45756"))
fig.add_annotation(x=m, y=62, text="mean 29.70", showarrow=False, xanchor="right", xshift=-4, font=dict(size=18))
fig.add_scatter(x=out, y=[2, 2], mode="markers+text", text=[f"age {int(a)}" for a in out], textposition="top center",
                marker=dict(symbol="circle-open", size=22, color="#E45756", line=dict(width=3)), textfont=dict(size=18))
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=19),
                  showlegend=False, bargap=0.05, title=dict(text="714 Titanic ages: only 74 and 80 lie beyond μ + 3σ", x=0.5),
                  xaxis=dict(title="age (years)", range=[-2, 84]), yaxis=dict(title="passengers", range=[0, 68]),
                  margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "age_outliers.png", scale=2)
fig.write_image(here / "age_outliers.pdf")
