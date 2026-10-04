"""Titanic ages: a density histogram with the smooth KDE curve on top (what seaborn's old distplot drew)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna()
grid = np.linspace(age.min(), age.max(), 300)
fig = go.Figure(go.Histogram(x=age, xbins=dict(start=0, end=80, size=5), histnorm="probability density",
                             marker=dict(color="#4C78A8", opacity=0.45, line=dict(color="white", width=1))))
fig.add_scatter(x=grid, y=gaussian_kde(age)(grid), mode="lines", line=dict(color="#F58518", width=4))
fig.update_layout(template="simple_white", width=900, height=520, showlegend=False, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="Histogram (bars) and KDE curve (line) of 714 ages", x=0.5),
                  xaxis=dict(title="Age (years)", range=[0, 82]), yaxis=dict(title="Density", showgrid=True),
                  margin=dict(l=80, r=20, t=70, b=70))
fig.write_image(here / "density.png", scale=2)
fig.write_image(here / "density.pdf")
