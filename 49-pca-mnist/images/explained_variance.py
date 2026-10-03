"""Cumulative explained variance of MNIST's principal components, with the 90% rule of thumb (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
ev = pd.read_csv(here.parent / "data" / "explained_variance.csv")
cum = np.cumsum(ev.ratio)
k90 = int(np.searchsorted(cum, 0.90) + 1)
fig = go.Figure(go.Scatter(x=ev.component, y=cum, mode="lines", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=[0, k90, k90], y=[0.9, 0.9, 0], mode="lines", line=dict(color=ORANGE, dash="dash", width=2)))
fig.add_annotation(x=k90, y=0.9, ax=80, ay=60, text=f"<b>{k90} components</b><br>explain 90%", font=dict(size=17, color=ORANGE),
                   arrowcolor=ORANGE)
fig.add_annotation(x=3, y=cum[2], ax=60, ay=-10, text=f"first 3: {cum[2]:.0%}", font=dict(size=16), arrowcolor=GREY)
fig.update_layout(template="simple_white", width=950, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=80, r=30, t=60, b=60),
                  title=dict(text="MNIST: share of the variance kept by the first k components", x=0.5),
                  xaxis=dict(title="Number of principal components k", range=[0, 784]),
                  yaxis=dict(title="Cumulative explained variance", tickformat=".0%", range=[0, 1.02]))
fig.write_image(here / "explained_variance.png", scale=2)
fig.write_image(here / "explained_variance.pdf")
