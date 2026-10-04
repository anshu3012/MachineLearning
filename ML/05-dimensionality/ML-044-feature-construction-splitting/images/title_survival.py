"""Plotly chart for Note ML-044: survival rate for each title split out of the Name column."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv")
title = df["Name"].str.split(", ").str[1].str.split(".").str[0]
rate = df.groupby(title)["Survived"].agg(["mean", "size"]).sort_values(["size", "mean"])
colour = ["#F58518" if n >= 10 else "#BBBBBB" for n in rate["size"]]

fig = go.Figure(go.Bar(y=rate.index, x=rate["mean"], orientation="h", marker_color=colour,
                       text=[f"{m:.0%} of {n}" for m, n in zip(rate["mean"], rate["size"])],
                       textposition="outside"))
fig.update_layout(template="simple_white", width=800, height=640, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=21),
                  xaxis=dict(title="Survival rate (grey: fewer than 10 passengers)", tickformat=".0%", tickvals=[0, .2, .4, .6, .8, 1], range=[0, 1.25]),
                  yaxis=dict(title=None), margin=dict(l=120, r=20, t=20, b=60))
fig.write_image(here / "title_survival.png", scale=2)
fig.write_image(here / "title_survival.pdf")
