"""How sparse VGG16's feature maps are, layer by layer, over 500 photos of cats and dogs (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, FONT

here = Path(__file__).parent
s = pd.read_csv(here.parent / "data" / "sparsity.csv")
labels = [f"{p}<br>{n.replace('block', 'b').replace('_conv', '.')}" for p, n in zip(s.position, s.layer)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=labels, y=100 * s.zero_values, mode="lines+markers", name="values that are exactly 0",
                         line=dict(color=BLUE, width=3), marker=dict(size=9)))
fig.add_trace(go.Scatter(x=labels, y=100 * s.blank_maps, mode="lines+markers", name="maps that are blank (all 0)",
                         line=dict(color=RED, width=3), marker=dict(size=9)))
fig.update_layout(template="simple_white", width=950, height=430, font=FONT,
                  xaxis=dict(title="convolution layer (position in VGG16; block.layer)"),
                  yaxis=dict(title="share of the output (%)", range=[0, 100]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=20, b=90))
fig.write_image(here / "sparsity.png", scale=2)
fig.write_image(here / "sparsity.pdf")
