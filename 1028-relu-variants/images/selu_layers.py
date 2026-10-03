"""Standard deviation of the activations through 30 layers: SELU stays at 1 (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, PURPLE, GREY, FONT

here = Path(__file__).parent
s = pd.read_csv(here.parent / "data" / "selu_layers.csv")
fig = go.Figure()
for name, c in (("SELU", PURPLE), ("ELU", GREEN), ("ReLU", GREY)):
    t = s[s.activation == name]
    fig.add_trace(go.Scatter(x=t.layer, y=t["std"], name=name, mode="lines+markers", line=dict(color=c, width=4)))
fig.update_layout(template="simple_white", width=900, height=430, font=FONT,
                  xaxis=dict(title="layer"), yaxis=dict(title="standard deviation of activations", type="log", dtick=1,
                                                        exponentformat="power"),
                  legend=dict(x=0.02, y=0.05), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "selu_layers.png", scale=2)
fig.write_image(here / "selu_layers.pdf")
