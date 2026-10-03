"""Titanic fares cut into 8 bins: equal-width bins against quantile bins (Plotly)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
fare = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Fare"]
edges = {"(a) 8 equal-width bins": np.linspace(fare.min(), fare.max(), 9),
         "(b) 8 quantile bins": np.quantile(fare, np.linspace(0, 1, 9))}
fig = make_subplots(1, 2, subplot_titles=list(edges), horizontal_spacing=0.08)
for i, (name, e) in enumerate(edges.items(), start=1):
    fig.add_trace(go.Histogram(x=fare[fare <= 150], xbins=dict(start=0, end=150, size=2), marker_color="#4C78A8",
                               showlegend=False), 1, i)
    for x in e[e <= 150]:
        fig.add_vline(x=x, line=dict(color="#E45756", width=3), opacity=1, layer="above", row=1, col=i)
    counts = np.histogram(fare, e)[0]
    print(name, np.round(e, 1), counts)
fig.update_xaxes(title="fare (passengers above 150 not drawn)", range=[0, 150])
fig.update_yaxes(title="passengers", col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1300, height=550, font=FONT, margin=dict(l=70, r=20, t=50, b=70))
fig.write_image(HERE / "bins.png", scale=2)
fig.write_image(HERE / "bins.pdf")
