"""MNIST training loss per epoch, plain SGD vs SGD with momentum 0.9, learning rate 0.01, mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "mnist_loss.csv")
fig = go.Figure()
for mom, name, c in ((0.0, "plain SGD", BLUE), (0.9, "SGD with momentum 0.9", ORANGE)):
    s = r[r.momentum == mom]
    for _, g in s.groupby("seed"):
        fig.add_trace(go.Scatter(x=g.epoch, y=g.loss, showlegend=False, opacity=0.35, line=dict(color=c, width=1.5)))
    m = s.groupby("epoch").loss.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, name=name + " (mean of 3)", line=dict(color=c, width=5)))
fig.update_layout(template="simple_white", width=950, height=430, font=FONT, xaxis=dict(title="epoch"),
                  yaxis=dict(title="training loss", type="log"), legend=dict(x=0.55, y=0.95),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "mnist_momentum.png", scale=2)
fig.write_image(here / "mnist_momentum.pdf")
