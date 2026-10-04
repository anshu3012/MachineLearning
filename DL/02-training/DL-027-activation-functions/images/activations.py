"""Sigmoid, tanh and ReLU (solid) with their derivatives (dashed), from the Notebook (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "activation_curves.csv")
names = [("sigmoid", "Sigmoid: 0 to 1"), ("tanh", "Tanh: -1 to 1"), ("relu", "ReLU: 0 to infinity")]
fig = make_subplots(rows=1, cols=3, subplot_titles=[t for _, t in names], horizontal_spacing=0.07)
for i, (k, _) in enumerate(names, start=1):
    fig.add_trace(go.Scatter(x=c.z, y=c[k], name="function", line=dict(color=BLUE, width=4, simplify=False), showlegend=i == 1), 1, i)
    fig.add_trace(go.Scatter(x=c.z, y=c["d_" + k], name="derivative", line=dict(color=ORANGE, width=4, dash="dash", simplify=False),
                             showlegend=i == 1), 1, i)
    fig.add_hline(y=0, line=dict(color=GREY, width=1), row=1, col=i)
    fig.update_xaxes(title_text="z", range=[-6, 6], row=1, col=i)
fig.update_yaxes(range=[-1.15, 1.15], row=1, col=1)
fig.update_yaxes(range=[-1.15, 1.15], row=1, col=2)
fig.update_yaxes(range=[-0.3, 3.3], row=1, col=3)
fig.update_layout(template="simple_white", width=1100, height=420, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.22), margin=dict(l=50, r=20, t=50, b=90))
fig.update_annotations(font=dict(family=FONT["family"], size=18))
fig.write_image(here / "activations.png", scale=2)
fig.write_image(here / "activations.pdf")
