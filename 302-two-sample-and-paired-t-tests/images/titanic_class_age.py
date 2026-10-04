"""Titanic: random samples of 40 first-class and 40 third-class ages (random_state=5), each dot one passenger
(jittered sideways), with the sample mean and its 95% bootstrap confidence interval (10000 resamples, seed 0)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
data = here.parent / "data"
t = pd.concat([pd.read_csv(data / "titanic_train.csv"), pd.read_csv(data / "titanic_test.csv")])
first = t[t.Pclass == 1].Age.dropna().reset_index(drop=True).sample(40, random_state=5)
third = t[t.Pclass == 3].Age.dropna().reset_index(drop=True).sample(40, random_state=5)
jit = np.random.default_rng(0)

fig = go.Figure()
for i, (ages, colour) in enumerate(((first, "#4C78A8"), (third, "#F58518"))):
    x = ages.to_numpy(float)
    fig.add_scatter(x=i + jit.uniform(-0.175, 0.175, len(x)), y=x, mode="markers",
                    marker=dict(color=colour, size=10, opacity=0.6))
    rng = np.random.default_rng(0)
    boots = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(10000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    fig.add_scatter(x=[i, i], y=[lo, hi], mode="lines", line=dict(color="black", width=4))
    fig.add_scatter(x=[i], y=[x.mean()], mode="markers", marker=dict(color="black", size=15))
fig.update_xaxes(tickvals=[0, 1], ticktext=["first class", "third class"], range=[-0.5, 1.5])
fig.update_yaxes(title="Age (years)", showgrid=True)
fig.update_layout(template="simple_white", width=600, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=20, b=50))
fig.write_image(here / "titanic_class_age.png", scale=2)
fig.write_image(here / "titanic_class_age.pdf")
