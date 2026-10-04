"""The 256 first-layer weights after plain SGD with L2 and with L1, grouped by size (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import ORANGE, GREEN, FONT

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "sparsity_weights.csv").abs()
edges = [0, 0.0005, 0.01, 0.1, np.inf]
labels = ["0 (to 3 decimals)", "0.0005 to 0.01", "0.01 to 0.1", "above 0.1"]
fig = go.Figure()
for n, c, name in [("L2", ORANGE, "L2, λ = 0.03"), ("L1", GREEN, "L1, λ = 0.003")]:
    counts = pd.cut(w[n], edges, labels=labels, right=False).value_counts().reindex(labels)
    fig.add_bar(x=labels, y=counts.values, name=name, marker_color=c, text=counts.values, textposition="outside")
fig.update_layout(template="simple_white", width=1000, height=460, font=FONT, barmode="group",
                  xaxis_title="size of the weight", yaxis_title="number of weights (of 256)",
                  legend=dict(x=0.62, y=0.98), yaxis_range=[0, 175], margin=dict(l=60, r=20, t=30, b=60))
fig.write_image(here / "sparsity.png", scale=2)
fig.write_image(here / "sparsity.pdf")
