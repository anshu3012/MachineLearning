"""Gradient size against distance for a linear SimpleRNN whose W_h is s times an orthogonal matrix (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "linear_scaled_wh.csv")
fig = go.Figure()
for s, c, name in ((1.1, RED, "s = 1.1: grows (explodes)"), (1.0, GREY, "s = 1.0: stays the same"),
                   (0.9, BLUE, "s = 0.9: shrinks (vanishes)")):
    q = d[d.scale == s].sort_values("distance")
    fig.add_trace(go.Scatter(x=q.distance, y=q.grad, name=name, mode="lines", line=dict(color=c, width=4)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT,
                  xaxis=dict(title="distance of the word from the end of the review (time steps)"),
                  yaxis=dict(title="gradient size (log scale)", type="log", exponentformat="power"),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "scaled_wh.png", scale=2)
fig.write_image(here / "scaled_wh.pdf")
