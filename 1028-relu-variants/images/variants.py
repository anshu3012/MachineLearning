"""ReLU and its four variants (left) with their derivatives (right), from the Notebook (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, PURPLE, GREY, FONT

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "variant_curves.csv")
fig = make_subplots(rows=1, cols=2, subplot_titles=["Function", "Derivative"], horizontal_spacing=0.08)
for k, name, col, dash in (("relu", "ReLU", GREY, "solid"), ("leaky", "Leaky ReLU / PReLU (a = 0.1)", BLUE, "dash"),
                           ("elu", "ELU (alpha = 1)", GREEN, "solid"), ("selu", "SELU", PURPLE, "dot")):
    for i, col_name in enumerate((k, "d_" + k), start=1):
        fig.add_trace(go.Scatter(x=c.z, y=c[col_name], name=name, showlegend=i == 1,
                                 line=dict(color=col, width=4, dash=dash, simplify=False)), 1, i)
for i in (1, 2):
    fig.add_hline(y=0, line=dict(color=GREY, width=1), row=1, col=i)
    fig.add_vline(x=0, line=dict(color=GREY, width=1), row=1, col=i)
    fig.update_xaxes(title_text="z", row=1, col=i)
fig.update_yaxes(range=[-2, 3.2], row=1, col=1)
fig.update_yaxes(range=[-0.1, 1.9], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=50, r=20, t=50, b=100))
fig.update_annotations(font=dict(family=FONT["family"], size=18))
fig.write_image(here / "variants.png", scale=2)
fig.write_image(here / "variants.pdf")
