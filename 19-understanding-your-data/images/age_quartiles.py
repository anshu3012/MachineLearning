"""Titanic ages: histogram with the 25%, 50% and 75% lines that df.describe() reports."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna()
q = age.quantile([0.25, 0.5, 0.75])
ORANGE = "#F58518"
fig = go.Figure(go.Histogram(x=age, xbins=dict(start=0, end=80, size=5),
                             marker=dict(color="#4C78A8", opacity=0.6, line=dict(color="white", width=1))))
# one label per line: 25% to the left, 75% to the right, 50% higher up, so they never overlap
for (p, v), anchor, y in zip(q.items(), ("right", "center", "left"), (130, 142, 130)):
    fig.add_shape(type="line", x0=v, x1=v, y0=0, y1=125, line=dict(color=ORANGE, width=3, dash="dash"))
    fig.add_annotation(x=v, y=y, text=f"{p:.0%}: {v:.1f}".replace(".0", ""), showarrow=False, xanchor=anchor,
                       font=dict(color=ORANGE, size=18))
fig.update_layout(template="simple_white", width=900, height=540, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="714 known ages, split into four equal groups", x=0.5),
                  xaxis=dict(title="Age (years)", range=[0, 82]), yaxis=dict(title="Passengers", range=[0, 150], showgrid=True),
                  margin=dict(l=80, r=20, t=70, b=70))
fig.write_image(here / "age_quartiles.png", scale=2)
fig.write_image(here / "age_quartiles.pdf")
