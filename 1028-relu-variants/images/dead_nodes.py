"""Share of nodes in each hidden layer with z < 0 on every training row, after 200 epochs (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "dead_nodes.csv")
labels = [f"{r}<br>accuracy {a:.0%}" for r, a in zip(d.run, d.accuracy)]
fig = go.Figure()
for col, name, c in (("layer1_after", "hidden layer 1", BLUE), ("layer2_after", "hidden layer 2", ORANGE)):
    fig.add_trace(go.Bar(y=labels, x=d[col] * 100, name=name, orientation="h", marker_color=c,
                         text=[f"{v:.0%}" for v in d[col]], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=560, font=dict(family=FONT["family"], size=19), barmode="group",
                  xaxis=dict(title="nodes with z < 0 on every row (%)", range=[0, 112]),
                  yaxis=dict(autorange="reversed"), legend=dict(orientation="h", x=0.0, y=1.08),
                  margin=dict(l=330, r=30, t=50, b=60))
fig.write_image(here / "dead_nodes.png", scale=2)
fig.write_image(here / "dead_nodes.pdf")
