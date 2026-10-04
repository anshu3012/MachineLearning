"""Mean size (relative to the last word) of dL/dx_k against the distance of word k from the end of the review, SimpleRNN trained on IMDB (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import RED, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "trained_tanh.csv").sort_values("distance")
fig = go.Figure(go.Scatter(x=d.distance, y=d.grad / d.grad.iloc[0], mode="lines", line=dict(color=RED, width=4)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, showlegend=False,
                  xaxis=dict(title="distance of the word from the end of the review (time steps)"),
                  yaxis=dict(title="gradient size, relative to the last word", type="log", tickvals=[0.1, 0.2, 0.5, 1, 2], range=[-1.05, 0.35]),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "grad_vs_distance.png", scale=2)
fig.write_image(here / "grad_vs_distance.pdf")
