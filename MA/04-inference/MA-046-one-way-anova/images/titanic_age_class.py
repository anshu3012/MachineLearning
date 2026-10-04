"""Age of Titanic passengers by class (714 with a known age): every passenger as a jittered dot, with the class mean
and one standard deviation either side in black."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
titanic = pd.read_csv(here.parent / "data" / "titanic_train.csv").dropna(subset=["Age"])
jit = np.random.default_rng(0)

fig = go.Figure()
for i, cls in enumerate((1, 2, 3)):
    age = titanic.loc[titanic.Pclass == cls, "Age"]
    fig.add_scatter(x=i + jit.uniform(-0.3, 0.3, len(age)), y=age, mode="markers",
                    marker=dict(color="#4C78A8", size=6, opacity=0.35))
    m, s = age.mean(), age.std()
    fig.add_scatter(x=[i, i], y=[m - s, m + s], mode="lines", line=dict(color="black", width=4.5))
    fig.add_scatter(x=[i], y=[m], mode="markers", marker=dict(color="black", size=16))
fig.update_xaxes(tickvals=[0, 1, 2], ticktext=["class 1", "class 2", "class 3"], range=[-0.5, 2.5])
fig.update_yaxes(title="age (years)", showgrid=True)
fig.update_layout(template="simple_white", width=800, height=450, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=80, r=20, t=20, b=50))
fig.write_image(here / "titanic_age_class.png", scale=2)
fig.write_image(here / "titanic_age_class.pdf")
