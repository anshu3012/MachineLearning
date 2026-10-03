"""Standard deviation of the activations through 10 layers of 500 nodes for four starting spreads (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, FONT

here = Path(__file__).parent
s = pd.read_csv(here.parent / "data" / "layer_std.csv")
s.loc[s["std"] < 1e-12, "std"] = np.nan                  # exactly 0 cannot be drawn on a log axis
fig = make_subplots(rows=1, cols=2, subplot_titles=["tanh", "ReLU"], horizontal_spacing=0.1)
style = {"0.01 (too small)": (RED, "dot"), "1 (too large)": (ORANGE, "dot"),
         "Xavier: sqrt(1/fan_in)": (BLUE, "solid"), "He: sqrt(2/fan_in)": (GREEN, "solid")}
for i, act in enumerate(("tanh", "relu"), start=1):
    for name, (c, dash) in style.items():
        t = s[(s.activation == act) & (s.start == name)]
        fig.add_trace(go.Scatter(x=t.layer, y=t["std"], name="weights x " + name, showlegend=i == 1,
                                 mode="lines+markers", line=dict(color=c, width=4, dash=dash)), 1, i)
    fig.update_xaxes(title_text="layer", dtick=1, row=1, col=i)
    fig.update_yaxes(type="log", dtick=2, exponentformat="power", row=1, col=i)
fig.update_yaxes(title_text="standard deviation of activations", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=500, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=80, r=20, t=50, b=110))
fig.update_annotations(font=dict(family=FONT["family"], size=18))
fig.write_image(here / "layer_std.png", scale=2)
fig.write_image(here / "layer_std.pdf")
