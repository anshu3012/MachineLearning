"""Gaussian Naive Bayes on 8 people (Plotly): a normal curve per class and column, and the density at the new person's value."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "people.csv")
q = {"height_cm": 185, "weight_lb": 170}
cols = {"male": "#4C78A8", "female": "#E45756"}


def pdf(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=("Height (cm)", "Weight (pounds)"))
for k, (col, rng) in enumerate((("height_cm", (140, 200)), ("weight_lb", (60, 230)))):
    xs = np.linspace(*rng, 400)
    for g, c in cols.items():
        v = df.loc[df.gender == g, col]
        mu, sd = v.mean(), v.std()          # sample standard deviation (divides by n - 1)
        d = pdf(q[col], mu, sd)
        print(g, col, "mean", round(mu, 2), "sd", round(sd, 2), "density at query", d)
        fig.add_trace(go.Scatter(x=xs, y=pdf(xs, mu, sd), mode="lines", line=dict(color=c, width=3),
                                 name=g, legendgroup=g, showlegend=(k == 0)), 1, k + 1)
        fig.add_trace(go.Scatter(x=v, y=np.zeros(len(v)), mode="markers", marker=dict(color=c, size=10, symbol="line-ns-open",
                                 line=dict(width=3)), showlegend=False), 1, k + 1)
        fig.add_trace(go.Scatter(x=[q[col]], y=[d], mode="markers", marker=dict(color=c, size=11), showlegend=False), 1, k + 1)
    fig.add_trace(go.Scatter(x=[q[col]] * 2, y=[0, 0.075 if k == 0 else 0.03], mode="lines", line=dict(color="black", dash="dash"),
                             showlegend=False), 1, k + 1)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=450, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=60, r=20, t=50, b=90))
fig.write_image(here / "gaussians.png", scale=2); fig.write_image(here / "gaussians.pdf")
