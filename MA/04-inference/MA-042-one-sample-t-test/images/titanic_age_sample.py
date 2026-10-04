"""Titanic ages: the 1046 known ages (population) and our random sample of 25 (random_state=0), as density
histograms on shared 5-year bins, with the H0 value 40 and the two means marked."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
data = here.parent / "data"
ages = pd.concat([pd.read_csv(data / "titanic_train.csv"), pd.read_csv(data / "titanic_test.csv")]).Age.dropna().reset_index(drop=True)
sample = ages.sample(25, random_state=0)
edges = np.arange(ages.min(), ages.max() + 5, 5)

fig = go.Figure()
for x, name, colour in ((ages, "all 1046 passengers", "#4C78A8"), (sample, "our sample of 25", "#F58518")):
    dens = np.histogram(x, edges, density=True)[0]
    fig.add_bar(x=edges[:-1] + 2.5, y=dens, width=5, name=name, opacity=0.55,
                marker=dict(color=colour, line=dict(color="white", width=1)))
for v, name, dash in ((40, "<i>H</i><sub>0</sub>: <i>μ</i> = 40", "solid"), (ages.mean(), f"true mean {ages.mean():.2f}", "dot"),
                      (sample.mean(), f"sample mean {sample.mean():.2f}", "dash")):
    fig.add_scatter(x=[v, v], y=[0, 0.045], mode="lines", name=name, line=dict(color="black", width=3.5, dash=dash))
fig.update_xaxes(title="Age (years)", dtick=10, range=[-2, 82], showgrid=True)
fig.update_yaxes(title="Density", showgrid=True)
fig.update_layout(template="simple_white", width=1000, height=460, barmode="overlay", bargap=0,
                  font=dict(family="Latin Modern Roman", size=20), legend=dict(x=1.02, y=0.5, yanchor="middle"),
                  margin=dict(l=90, r=20, t=20, b=70))
fig.write_image(here / "titanic_age_sample.png", scale=2)
fig.write_image(here / "titanic_age_sample.pdf")
