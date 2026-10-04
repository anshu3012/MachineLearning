"""The long right tail of the Titanic fares: the 45 highest fares (top 5 percent of the 891 passengers, 113.28 and
above) paid 31.5 percent of all the money; the tail is rare but carries a large share."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv").Fare
top = fare.sort_values(ascending=False).iloc[:45]
share = top.sum() / fare.sum()
assert len(fare) == 891 and round(top.min(), 2) == 113.28 and round(share, 3) == 0.315 and round(fare.skew(), 2) == 4.79
cut = top.min()
fig = go.Figure()
fig.add_histogram(x=fare[fare < cut], xbins=dict(start=0, end=520, size=10), marker_color="rgba(76,120,168,0.7)",
                  name="846 passengers: 68.5 percent of the money")
fig.add_histogram(x=fare[fare >= cut], xbins=dict(start=0, end=520, size=10), marker_color="#E45756",
                  name="45 highest fares (5 percent): 31.5 percent of the money")
fig.add_annotation(x=300, y=1.2, text="the long right tail:<br>few passengers, a large share", showarrow=False,
                   ax=0, ay=-60, font=dict(size=20, color="#E45756"), arrowcolor="#E45756", arrowwidth=2)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=19),
                  barmode="overlay", bargap=0.05, title=dict(text="Titanic fares: skewness 4.79", x=0.5),
                  xaxis=dict(title="fare"), yaxis=dict(title="passengers (log scale)", type="log", range=[-0.1, 2.75], tickvals=[1, 3, 10, 30, 100, 300]),
                  legend=dict(x=0.3, y=0.99, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "fare_tail.png", scale=2)
fig.write_image(here / "fare_tail.pdf")
