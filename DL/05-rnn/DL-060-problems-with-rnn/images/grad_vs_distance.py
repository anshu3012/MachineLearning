"""Mean size (relative to the last word) of dL/dx_k against the distance of word k from the end of the review,
SimpleRNN trained on IMDB, 5 seeds: mean line and min-max band; the first 15 steps of the window are shaded (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import RED, GREY, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "trained_tanh.csv")
g = d.groupby("distance").rel_grad.agg(["mean", "min", "max"]).reset_index()
fig = go.Figure()
fig.add_vrect(x0=184.5, x1=199.5, fillcolor=GREY, opacity=0.15, line_width=0)
fig.add_annotation(x=192, y=-0.75, text="first 15 steps<br>of the window", showarrow=False, font=dict(family=FONT["family"], size=14))
fig.add_trace(go.Scatter(x=g.distance, y=g["max"], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=g.distance, y=g["min"], mode="lines", line=dict(width=0), fill="tonexty",
                         fillcolor="rgba(228,87,86,0.18)", name="range over 5 runs"))
fig.add_trace(go.Scatter(x=g.distance, y=g["mean"], mode="lines", line=dict(color=RED, width=4), name="mean of 5 runs"))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT,
                  xaxis=dict(title="distance of the word from the end of the review (time steps)", range=[0, 200]),
                  yaxis=dict(title="gradient size, relative to the last word", type="log",
                             tickvals=[0.001, 0.01, 0.1, 1], ticktext=["0.001", "0.01", "0.1", "1"], range=[-2.6, 0.15]),
                  legend=dict(x=0.6, y=0.98), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "grad_vs_distance.png", scale=2)
fig.write_image(here / "grad_vs_distance.pdf")
