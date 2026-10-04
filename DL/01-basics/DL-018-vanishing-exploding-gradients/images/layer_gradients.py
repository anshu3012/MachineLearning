"""Mean |gradient| of each layer's weights at the start of training (from the Notebook): vanishing in a deep sigmoid
network, steady with ReLU, exploding with large weights and no squashing (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, FONT

here = Path(__file__).parent
g = pd.read_csv(here.parent / "data" / "layer_gradients.csv")
e = pd.read_csv(here.parent / "data" / "exploding_gradients.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.6, 0.4],
                    subplot_titles=("Vanishing: sigmoid layers shrink the gradient",
                                    "Exploding: weights with std 1, no squashing"))
for name, c in (("10 sigmoid layers", RED), ("3 sigmoid layers", ORANGE), ("10 ReLU layers", GREEN)):
    d = g[g.network == name]
    fig.add_trace(go.Scatter(x=d.layer, y=d.mean_abs_grad, mode="lines+markers", name=name,
                             line=dict(color=c, width=3), marker=dict(size=9)), row=1, col=1)
fig.add_trace(go.Scatter(x=e.layer, y=e.mean_abs_grad, mode="lines+markers", name="10 linear layers, large weights",
                         line=dict(color=BLUE, width=3), marker=dict(size=9)), row=1, col=2)
for col in (1, 2):
    fig.update_xaxes(title_text="layer (1 = next to the input)", dtick=1, row=1, col=col)
    fig.update_yaxes(title_text="mean |∂L/∂W| (log scale)", type="log", exponentformat="power", row=1, col=col)
fig.update_layout(template="simple_white", width=1150, height=500, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.22), margin=dict(l=80, r=30, t=60, b=110))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=17))
fig.write_image(here / "layer_gradients.png", scale=2)
fig.write_image(here / "layer_gradients.pdf")
