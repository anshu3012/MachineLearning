"""MNIST, AdaGrad vs RMSProp at learning rate 0.001, mean of 3 seeds: training loss (left) and the median
effective learning rate eta / sqrt(v) over all weights (right), per epoch (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREEN, PURPLE, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "mnist_rmsprop.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("training loss", "median effective learning rate η / √v"))
for kind, name, c in (("adagrad", "AdaGrad", GREEN), ("rmsprop", "RMSProp", PURPLE)):
    m = r[r.optimizer == kind].groupby("epoch")[["loss", "eff_lr"]].mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.loss, name=name, line=dict(color=c, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=m.index, y=m.eff_lr, showlegend=False, line=dict(color=c, width=4)), 1, 2)
fig.update_xaxes(title_text="epoch")
fig.update_yaxes(type="log", exponentformat="power")
fig.update_layout(template="simple_white", width=1050, height=430, font=FONT, legend=dict(x=0.3, y=0.95),
                  margin=dict(l=80, r=20, t=40, b=60))
fig.write_image(here / "mnist_rmsprop.png", scale=2)
fig.write_image(here / "mnist_rmsprop.pdf")
