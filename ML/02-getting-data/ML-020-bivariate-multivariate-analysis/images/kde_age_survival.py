"""Titanic: age density for passengers who died vs survived (the old distplot(hist=False), now a KDE)."""
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from common import load, layout, save_px, RED, GREEN

t = load("titanic_train").dropna(subset=["Age"])
fig = go.Figure()
for value, name, colour, fill in [(0, "died", RED, "rgba(228,87,86,0.15)"), (1, "survived", GREEN, "rgba(84,162,75,0.15)")]:
    age = t.Age[t.Survived == value]
    grid = np.linspace(age.min(), age.max(), 300)          # each curve covers its own group's ages, and has area 1
    fig.add_scatter(x=grid, y=gaussian_kde(age)(grid), mode="lines", name=name, line=dict(color=colour, width=3.5),
                    fill="tozeroy", fillcolor=fill)
layout(fig, "Children survived more often than they died", "Age (years)", "Density", legend=dict(x=0.85, y=0.95))
fig.update_xaxes(dtick=10, showgrid=True, range=[0, 82])
fig.update_yaxes(showgrid=True, rangemode="tozero")
save_px(fig, "kde_age_survival")
