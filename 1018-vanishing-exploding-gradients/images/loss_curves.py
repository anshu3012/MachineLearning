"""Training loss over 100 epochs for the three networks of the Note (from the Notebook) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "loss_histories.csv")
fig = go.Figure()
for name, c in (("10 sigmoid layers", RED), ("3 sigmoid layers", ORANGE), ("10 ReLU layers", GREEN)):
    fig.add_trace(go.Scatter(x=h.epoch + 1, y=h[name], name=name, line=dict(color=c, width=4)))
fig.add_hline(y=0.6931, line=dict(color=GREY, dash="dot", width=2))
fig.add_annotation(x=50, y=0.6931, text="0.693: guessing", showarrow=False, yshift=14)
fig.update_layout(template="simple_white", width=950, height=460, font=FONT, legend=dict(orientation="h", x=0.0, y=1.12),
                  xaxis=dict(title="epoch"), yaxis=dict(title="training loss (binary cross-entropy)"),
                  margin=dict(l=80, r=30, t=60, b=60))
fig.write_image(here / "loss_curves.png", scale=2)
fig.write_image(here / "loss_curves.pdf")
