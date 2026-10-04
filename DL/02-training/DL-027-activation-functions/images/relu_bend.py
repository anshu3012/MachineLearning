"""Two ReLUs subtracted give a bent, clipped line: ReLU is not linear (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, GREY, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "relu_bend.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=d.x, y=d.a, name="max(0, x + 1)", line=dict(color=BLUE, width=3, dash="dot")))
fig.add_trace(go.Scatter(x=d.x, y=d.b, name="max(0, x - 1)", line=dict(color=ORANGE, width=3, dash="dot")))
fig.add_trace(go.Scatter(x=d.x, y=d["diff"], name="difference", line=dict(color=GREEN, width=5)))
fig.add_hline(y=0, line=dict(color=GREY, width=1))
fig.update_layout(template="simple_white", width=800, height=400, font=FONT, xaxis=dict(title="x"),
                  yaxis=dict(title="output", range=[-0.3, 4.2]), legend=dict(x=0.02, y=0.98),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "relu_bend.png", scale=2)
fig.write_image(here / "relu_bend.pdf")
