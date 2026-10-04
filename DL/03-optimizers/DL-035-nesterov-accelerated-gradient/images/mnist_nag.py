"""MNIST training loss per epoch, momentum vs NAG at beta 0.9 (left) and 0.99 (right), mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import ORANGE, PURPLE, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "mnist_nag.csv")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=("β = 0.9", "β = 0.99"))
for col, beta in enumerate((0.9, 0.99), start=1):
    for nag, name, c in ((False, "momentum", ORANGE), (True, "NAG", PURPLE)):
        m = r[(r.beta == beta) & (r.nag == nag)].groupby("epoch").loss.mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, name=name, showlegend=col == 1,
                                 line=dict(color=c, width=4)), 1, col)
fig.update_xaxes(title_text="epoch")
fig.update_yaxes(title_text="training loss (mean of 3)", type="log", col=1)
fig.update_yaxes(type="log", col=2)
fig.update_layout(template="simple_white", width=1050, height=430, font=FONT, legend=dict(x=0.35, y=0.95),
                  margin=dict(l=80, r=20, t=40, b=60))
fig.write_image(here / "mnist_nag.png", scale=2)
fig.write_image(here / "mnist_nag.pdf")
