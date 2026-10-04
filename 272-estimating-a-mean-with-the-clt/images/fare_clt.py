"""Titanic fares: the population of 1308 known fares (right-skewed) against the means of 100 samples of 50
passengers (close to a bell). Same sampling as the Notebook. Density histograms (bins 5 pounds wide) with a
KDE curve (scipy gaussian_kde, Scott's bandwidth) drawn over the range of the data."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
data = here.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
fare = df["Fare"].dropna()
rng = np.random.default_rng(42)
means = np.array([fare.sample(50, random_state=rng).mean() for _ in range(100)])
panels = [("population: 1308 fares", fare.to_numpy(float), "#F58518"),
          ("100 sample means, n = 50", means, "#54A24B")]

fig = make_subplots(1, 2, subplot_titles=[p[0] for p in panels], horizontal_spacing=0.08)
for c, (_, x, colour) in enumerate(panels, start=1):
    edges = np.arange(x.min(), x.max() + 5, 5)
    dens, edges = np.histogram(x, edges, density=True)
    fig.add_trace(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=dens, width=5, opacity=0.45,
                         marker=dict(color=colour, line=dict(color="white", width=1))), 1, c)
    grid = np.linspace(x.min(), x.max(), 600)
    fig.add_trace(go.Scatter(x=grid, y=stats.gaussian_kde(x)(grid), mode="lines",
                             line=dict(color=colour, width=3.5, shape="spline")), 1, c)
    fig.update_xaxes(title="fare (pounds); fares above 150 not shown", range=[0, 150], showgrid=True, row=1, col=c)
    fig.update_yaxes(showgrid=True, row=1, col=c)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=400, showlegend=False, bargap=0,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=90, r=20, t=50, b=70))
fig.update_annotations(font_size=21)
fig.write_image(here / "fare_clt.png", scale=2)
fig.write_image(here / "fare_clt.pdf")
