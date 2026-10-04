"""MNIST training loss per epoch for six optimizers, mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, PURPLE, GREY, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "mnist_all.csv")
style = {"SGD": (GREY, "solid"), "momentum": (ORANGE, "solid"), "NAG": (BLUE, "dash"),
         "AdaGrad": (GREEN, "solid"), "RMSProp": (PURPLE, "solid"), "Adam": (RED, "solid")}
fig = go.Figure()
for name, (c, dash) in style.items():
    m = r[r.optimizer == name].groupby("epoch").loss.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, name=name, line=dict(color=c, width=4, dash=dash)))
fig.update_layout(template="simple_white", width=950, height=470, font=FONT, xaxis=dict(title="epoch"),
                  yaxis=dict(title="training loss (mean of 3 seeds)", type="log", exponentformat="power"),
                  legend=dict(x=1.0, xanchor="right", y=1.0), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "mnist_all.png", scale=2)
fig.write_image(here / "mnist_all.pdf")
