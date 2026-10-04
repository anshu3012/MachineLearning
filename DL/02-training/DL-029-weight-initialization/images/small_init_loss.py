"""Training loss of a 4-layer network started from 0.01 x randn vs Keras' default, plain SGD (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "small_init_loss.csv")
fig = go.Figure()
for name, label, c, dash in (("tanh, 0.01 x randn (SGD)", "tanh, 0.01 x randn", RED, "solid"),
                             ("relu, 0.01 x randn (SGD)", "ReLU, 0.01 x randn", ORANGE, "dash"),
                             ("tanh, Keras default (SGD)", "tanh, Keras default", BLUE, "solid"),
                             ("relu, Keras default (SGD)", "ReLU, Keras default", GREEN, "dash")):
    fig.add_trace(go.Scatter(x=h.epoch + 1, y=h[name], name=label, line=dict(color=c, width=4, dash=dash)))
fig.update_layout(template="simple_white", width=900, height=430, font=FONT, xaxis=dict(title="epoch"),
                  yaxis=dict(title="training loss"), legend=dict(x=0.6, y=0.6), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "small_init_loss.png", scale=2)
fig.write_image(here / "small_init_loss.pdf")
