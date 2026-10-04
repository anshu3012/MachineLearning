"""Coefficient of variation: Titanic ages and fares, each divided by its own mean, so both are on one scale."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
edges = np.arange(0, 5.01, 0.25)
panels = []
for col, colour in (("Age", "#4C78A8"), ("Fare", "#F58518")):
    v = df[col].dropna()
    cv = v.std() / v.mean() * 100
    rel = (v / v.mean()).clip(upper=4.99)          # fares above 5x the mean go in the last bin
    pct = np.histogram(rel, edges)[0] / len(rel) * 100
    panels.append((f"{col}: CV = {cv:.0f}%", pct, colour))

fig = make_subplots(2, 1, shared_xaxes=True, vertical_spacing=0.12, subplot_titles=[p[0] for p in panels])
for r, (_, pct, colour) in enumerate(panels, start=1):
    fig.add_trace(go.Bar(x=edges[:-1] + 0.125, y=pct, width=0.25, marker=dict(color=colour, line=dict(color="white", width=1)),
                         opacity=0.8), r, 1)
    fig.update_yaxes(title="% of passengers", showgrid=True, row=r, col=1)
fig.update_xaxes(range=[0, 5], dtick=0.5, showgrid=True)
fig.update_xaxes(title="value ÷ column mean  (1 = the mean)", row=2, col=1)
fig.update_layout(template="simple_white", width=800, height=550, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=80, r=20, t=40, b=60))
fig.update_annotations(font_size=19)
fig.write_image(here / "cv_compare.png", scale=2)
fig.write_image(here / "cv_compare.pdf")
