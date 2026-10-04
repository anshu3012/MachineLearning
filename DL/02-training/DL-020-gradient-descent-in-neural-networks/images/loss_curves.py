"""Training loss per epoch for three batch sizes, and the loss after each single update for stochastic and
mini-batch gradient descent (from the Notebook) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, FONT

here = Path(__file__).parent
e = pd.read_csv(here.parent / "data" / "epoch_loss.csv")
u = pd.read_csv(here.parent / "data" / "update_loss.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Loss after each epoch", "Loss after each of the first 320 updates"))
for col_name, label, c in (("batch_size=320", "batch (batch_size=320)", BLUE),
                           ("batch_size=32", "mini-batch (batch_size=32)", ORANGE),
                           ("batch_size=1", "stochastic (batch_size=1)", RED)):
    fig.add_trace(go.Scatter(x=e.epoch + 1, y=e[col_name], name=label, line=dict(color=c, width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=u["update"] + 1, y=u["sgd (batch_size=1)"], name="stochastic", showlegend=False,
                         line=dict(color=RED, width=2)), row=1, col=2)
fig.add_trace(go.Scatter(x=u["update"] + 1, y=u["mini-batch (batch_size=32)"], name="mini-batch", showlegend=False,
                         line=dict(color=ORANGE, width=3)), row=1, col=2)
fig.update_xaxes(title_text="epoch", row=1, col=1)
fig.update_xaxes(title_text="update (stochastic: 1 epoch; mini-batch: 32 epochs)", row=1, col=2)
for col in (1, 2):
    fig.update_yaxes(title_text="training loss", row=1, col=col)
fig.update_layout(template="simple_white", width=1150, height=480, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=70, r=30, t=60, b=110))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=17))
fig.write_image(here / "loss_curves.png", scale=2)
fig.write_image(here / "loss_curves.pdf")
